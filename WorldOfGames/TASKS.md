# DevSecOps Tasks

Source: devsecops audit 2026-08-22. Tier: T0 actual, T1 target.
Status: `[ ]` todo `[x]` done `[~]` in progress. Update status inline as work happens.

## RESOLVED — Jenkins /manage/ warnings + broken login, 2026-08-22

`values.yaml` changes (commit `cd0cf7b`): bumped `controller.image.tag` to 2.568.2 (fixes 2 published core CVE bulletins); added `authorizationStrategy` (instance was fully unsecured - anyone could launch processes); set `unclassified.location.url` (was empty, breaks BUILD_URL/notifications); removed `blueocean` + `docker-slaves` from `additionalPlugins` (deprecated/broken against 2.568.2, docker-slaves also unused - Jenkinsfile agent uses the standard Kubernetes plugin cloud) and purged their already-installed `.jpi` files from the PVC (`jenkins-design-language` too - a blueocean sub-plugin, easy to miss since it doesn't match a `blueocean*` glob); enabled default `DirectoryBrowserSupport` CSP.

Found mid-fix: `controller.JCasC.securityRealm`/`.security` are chart convenience fields only rendered when `controller.sidecars.configAutoReload.enabled` is true - it's false here (untouched default), so securityRealm was silently a no-op the entire time this project has existed (`config.xml` showed `SecurityRealm$None`, nobody could actually log in, password was irrelevant). Moved securityRealm into `configScripts.jenkins`, which the chart always applies. This also fixed a nasty side effect: enabling `authorizationStrategy` without a real realm made every anonymous-denied request crash with an uncaught 500 instead of redirecting to login.

Remaining/accepted: reverse-proxy-config warning on `/manage/` is expected when accessing via `kubectl port-forward` (URL mismatch vs. the correct in-cluster `unclassified.location.url`) - not a real bug, resolves when accessed normally. Full site-wide CSP enforcement (separate from the `DirectoryBrowserSupport` CSP already enabled) intentionally left off - higher risk of breaking page rendering, Jenkins itself frames it as optional hardening.

## RESOLVED — pipeline fixed 2026-08-22, build #6 SUCCESS end-to-end

Chain of 4 separate bugs found and fixed, one build failure at a time:

- [x] `jenkinsslave/Dockerfile`: bundled Docker CLI (API v1.41) too old for host daemon (min 1.44, host is v1.53) → `client version 1.41 is too old`. Fixed: replaced dead base `linuxserver:docker-compose` (confirmed unpullable) with `ubuntu:22.04`; added missing `ARG packages` re-declaration after `FROM` (was silently expanding empty — `python3`/`pip`/`wget`/`unzip`/`telnet`/`iputils-ping` never actually installed); fixed apt package name `pip`→`python3-pip` + `pip install`→`pip3 install`; removed dead `RUN telnet` line; installed pinned Docker CLI 27.3.1 + Compose v2.29.7. Rebuilt + pushed `shaharco1804/world_of_game` to Docker Hub.
- [x] `Jenkinsfile`: `Run`/`Test`/`Finalize` stages + `post` blocks called `docker-compose` without `cd`-ing into `WorldOfGames/` (repo checks out at parent-repo root, compose file lives in the subfolder) → `no configuration file provided`. Fixed: added `cd ${WORKSPACE_DIR}` to each affected `sh` block.
- [x] `docker-compose.yml` `tester` service: bind-mounted `./:/WorldOfGames`, but the Jenkins agent shares the *host's* Docker socket (sibling-container pattern) rather than running its own daemon — bind-mount source path only exists in the agent pod's filesystem, not the host's, so the daemon silently mounted an empty dir → `Could not open requirements file`. Fixed: added `Dockerfile.tester` that `COPY`s `test.py`+`requirements` into the tester image at build time instead of mounting.
- [x] Missing `dockerhub` Jenkins credential (user added manually via Jenkins UI — Finalize stage's `withDockerRegistry` needs it to push).

All changes committed + pushed to `origin/main` (commits `f6c625e`, `a251975`). Confirmed via live pipeline run: Clean→Build→Run→Test(pytest PASSED)→Finalize(image pushed)→cleanup, `Finished: SUCCESS`.

**Still true / not addressed**: the underlying architecture flaw (Jenkins agent mounts host's `/var/run/docker.sock`) still exists — it's what caused the tester bind-mount bug above, and it's still the security risk flagged below (container-escape risk). Today's fix worked around it (bake-in instead of bind-mount) rather than removing the host-socket dependency. That item is still open.

## Quick wins (S, do first) — ALL DONE 2026-08-22

- [x] Removed `debug=True` in `MainScores.py`. Now gated via `FLASK_DEBUG=1` env var, off by default.
- [x] Added `.gitignore`.
- [x] Added `LICENSE` (MIT).
- [x] Pinned all deps in `requirements` and `jenkinsslave/requirements` to exact versions verified working in CI.
- [x] Added gitleaks: `.pre-commit-config.yaml` locally + `Secrets Scan` Jenkinsfile stage (before Clean/Build). Needed `git` binary added to the agent image (gitleaks shells out to it) and `git config --global --add safe.directory` (workspace UID mismatch made it silently no-op a "clean" scan otherwise — caught via commit-count sanity check, confirmed real scan on build #10: 54 commits, no leaks).
- [x] Removed dead `RUN telnet` line from `jenkinsslave/Dockerfile` (done earlier, during pipeline-fix work).
- [x] Added input validation to `MainScores.py` `process_input` (was uncaught `ValueError` on non-digit input, now clean 400).
- [x] Non-root `USER` added to app `Dockerfile` (verified: runs as `appuser`, score read/write still works). `jenkinsslave/Dockerfile` intentionally left root — needs the mounted host Docker socket to function; tied to the socket-mount architecture item below.

All verified via live pipeline run (build #10, SUCCESS) and local `docker build`/`docker run` tests before pushing.

## Priority list (ordered, risk/effort)

- [ ] Remove Docker socket mount from Jenkins agent pod (`Jenkinsfile` kubernetes yaml, `/var/run/docker.sock`). Replace w/ Kaniko/BuildKit-in-pod or dedicated build node. [M] Container-escape risk, biggest item, needs ADR (architecture decision). Skipped intentionally 2026-08-22 - needs your sign-off, not a unilateral call.
- [x] CI stages 2026-08-22: `Lint` (`ruff check`, gate), `Format Check` (`black --check`, gate), `Dependency Audit` (`pip-audit -r requirements`, gate) added to `Jenkinsfile`. Pre-existing lint/format debt across the whole codebase (`MainGame.py`, `Score.py`, `games/*.py`, `test.py`, `MainScores.py`) auto-fixed first (`ruff --fix` + `black`, plus 2 manual fixes: `exit()`→`sys.exit()`, bare `open()`→context manager in `Score.py`) so the gates could go in clean rather than immediately red. `pip-audit`/`ruff`/`black` installed via `uv` (swapped from `pip3`, faster) in `jenkinsslave/Dockerfile`; needed `python3-venv` added too (`pip-audit` creates its own scan venv internally). Verified: both `requirements` files clean, no known CVEs.
- [x] Add Dependabot. `.github/dependabot.yml` (repo root, since GitHub config lives at the `Devops_Expert` root, not `WorldOfGames/`) - weekly pip + docker ecosystem updates for both `WorldOfGames/` and `WorldOfGames/jenkinsslave/`.
- [x] Trivy scan added 2026-08-22 - `Image Scan` stage in `Jenkinsfile`, runs after Build. **Report-only, not gating**: found 2 real HIGH findings (`msgpack`, `setuptools`) baked into the `python:alpine`/`python:3.13-alpine` base image's own vendored pip internals - confirmed not fixable via our `requirements` pins or `pip install --upgrade pip` (already latest). A hard `--exit-code` gate would permanently block builds on something we can't actually fix from our side. Revisit if upstream resolves it. Also scanned `jenkinsslave` agent image manually (not wired into CI, since that image isn't rebuilt by the pipeline) - real findings in the statically-downloaded `docker`/`docker-compose` Go binaries (numerous Go-toolchain CVEs), out of scope for today, tracked here as follow-up: consider building those from a Go base with `go install` instead of grabbing prebuilt release tarballs, or pin to whatever release was built with the newest Go toolchain.
- [x] Moved `Scores.txt` to SQLite 2026-08-22 (`Score.py`) - one-time migration from the old flat file, same `add_score`/`read_score` interface so no other file needed changes. Also found + fixed a real lost-update race in the process (read-then-write across two separate DB transactions lost most concurrent updates - verified: 20 concurrent wins should've added 160, only 8 landed; fixed with a single atomic `UPDATE ... SET value = value + ?`, re-verified 160/160). Investigated the `monogodb` branch first per request - not merged, it was broken as committed and predates today's other fixes; SQLite chosen over Postgres/finishing Mongo since this is a single-integer-counter workload, no separate service justified. Still file-based, so still not safe for multiple replicas without a shared volume - that's an explicit, accepted scope boundary (task said "if multi-replica ever needed", not needed today).
- [x] Strip unneeded packages from `jenkinsslave/Dockerfile` 2026-08-22: dropped `wget`, `telnet`, `iputils-ping` (unused - docker/docker-compose calls use curl, nothing pings/telnets). Kept `unzip` (webdriver_manager needs it) and added `git` (gitleaks needs it for history-mode scans) + `python3-venv` (pip-audit needs it internally).
- [x] Add `SECURITY.md` 2026-08-22 - covers the Docker-socket-mount risk (links back here), credential scope, and what's actually scanned in CI.

All of the above verified live on build #13 (SUCCESS) - Secrets Scan → Lint → Format Check → Dependency Audit → Clean → Build → Image Scan → Run → Test → Finalize, every gate actually ran and passed (not skipped/cached). Two build-fixing detours along the way, both fixed and re-verified: gitleaks needed `git config --global --add safe.directory` (was silently no-op'ing on a UID mismatch, gave a false "clean" pass); ruff/black/pip-audit needed to run `cd`'d into `WorldOfGames/` like the other stages, not from the parent checkout root (CWD changes ruff's import-sort heuristics).

## Base image versions bumped 2026-08-22 (LTS preference)

- App `Dockerfile`: `python:alpine` (floating, was resolving to 3.14) → pinned `python:3.13-alpine` (mature, long support runway, explicit not floating).
- `jenkinsslave/Dockerfile`: `ubuntu:22.04` → `ubuntu:24.04` (current Ubuntu LTS, longer remaining support window). Needed one fix: Ubuntu 24.04's Python is PEP-668 "externally managed" - added `--break-system-packages` to the `uv pip install --system` call (fine here, this container's only job is being a disposable CI agent).
- Both verified: full local build + `docker run` functional test + ruff/black/pip-audit re-run clean on the new bases before pushing.

## Longer-term / needs decision first

- [ ] TLS termination (ingress/reverse proxy) if exposed beyond local/lan.
- [ ] Auth layer if app goes multi-user.
- [ ] SBOM + image signing if distributing image beyond own Docker Hub.

## Local Jenkins access

Cluster: minikube. Namespace: `jenkins`. Pod `jenkins-0` (StatefulSet).

Access, 2 ways:
1. Port-forward: `kubectl port-forward -n jenkins svc/jenkins 8080:8080` then open `http://localhost:8080`.
2. NodePort direct: `http://$(minikube ip):30893` (port may change on redeploy, check `kubectl get svc -n jenkins`).

Admin password: `kubectl exec -n jenkins jenkins-0 -- cat /run/secrets/chart-admin-password`

## Reference (don't re-derive, just recall)

- Full audit findings + scores + risk writeup: see conversation 2026-08-22, or re-run `/devsecops` audit if this file goes stale.
- Key risk chain: Jenkins agent pod mounts host docker.sock (`Jenkinsfile`) + unpinned deps (`requirements`, `jenkinsslave/requirements`) = supply-chain compromise path to host root.
- App = Flask (`MainScores.py`) + flat-file score state (`Score.py`/`Scores.txt`); CLI games (`MainGame.py`, `games/`) are separate, unrelated to web routes. See `CLAUDE.md` for architecture.

<!-- pollSCM trigger test 1787389699 -->
