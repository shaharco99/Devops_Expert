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

## Quick wins (S, do first)

- [ ] Remove `debug=True` in `MainScores.py:58`. Gate via env var, default off. RCE risk (Werkzeug debugger).
- [ ] Add `.gitignore` (`__pycache__`, `.venv`, `*.pyc`, `.env`).
- [ ] Add `LICENSE`.
- [ ] Pin all deps in `requirements` and `jenkinsslave/requirements` (exact versions).
- [ ] Add gitleaks/trufflehog: pre-commit hook + CI stage.
- [ ] Fix `jenkinsslave/Dockerfile`: delete bare `RUN telnet` line (dead/hangs build). Drop `telnet` from `packages` arg.
- [ ] Add input validation in `MainScores.py` `process_input` route (`int(request.form['game_chosen'])` uncaught ValueError today).
- [ ] Add non-root `USER` to `Dockerfile` and `jenkinsslave/Dockerfile` (both run root now).

## Priority list (ordered, risk/effort)

- [ ] Remove Docker socket mount from Jenkins agent pod (`Jenkinsfile` kubernetes yaml, `/var/run/docker.sock`). Replace w/ Kaniko/BuildKit-in-pod or dedicated build node. [M] Container-escape risk, biggest item, needs ADR (architecture decision).
- [ ] CI stages: lint (`ruff`/`flake8`), format check (`black`), `pip-audit`/`safety`, gate merge. [S/M]
- [ ] Add Dependabot or Renovate. [S]
- [ ] Trivy scan both images (app `Dockerfile` + `jenkinsslave/Dockerfile`) in pipeline. [S]
- [ ] Move `Scores.txt` flat-file state (`Score.py`) to real datastore (SQLite min) if multi-replica/durability ever needed. [M]
- [ ] Strip unneeded packages from `jenkinsslave/Dockerfile` (`wget`, `telnet`, `iputils-ping` not needed at runtime). [S]
- [ ] Add `SECURITY.md` + threat-model note covering Jenkins docker-socket exposure + credential scope. [S]

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
