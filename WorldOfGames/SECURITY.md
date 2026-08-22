# Security

This is a personal/learning DevOps project (T0/T1 tier), not a project with a formal
disclosure program. If you find a security issue, open a GitHub issue or contact the
repo owner directly.

## Known architecture risk: Jenkins agent Docker socket mount

The Jenkins agent pod (`Jenkinsfile`, `kubernetes` cloud spec) mounts the host's
`/var/run/docker.sock` into the build container so pipeline steps can run `docker`/
`docker-compose` directly against the node's daemon. This is a well-known
container-escape risk: any code that runs inside that agent pod (including a
compromised dependency pulled in during `pip install`/`docker build`) has effective
root access to the host's Docker daemon, and therefore the host itself.

This is accepted as a known limitation for now, not something silently overlooked -
see `TASKS.md` for the tracked follow-up (replacing it with Kaniko/BuildKit-in-pod or
a dedicated build node, which removes the host socket dependency entirely).

## Credential scope

- Docker Hub push credentials (`dockerhub` Jenkins credential ID) are scoped to the
  `Finalize` stage only, via `withDockerRegistry`.
- The Jenkins agent pod inherits whatever the mounted host Docker socket can do (see
  above) - broader than the Docker Hub credential alone.
- No application-level secrets exist today (the Flask app has no auth, no API keys).

## What's scanned

- **Secrets**: `gitleaks` runs in CI (`Secrets Scan` stage) before every build, plus
  `.pre-commit-config.yaml` for local commits.
- **Dependencies**: `pip-audit` runs in CI (`Dependency Audit` stage) against
  `requirements`.
- **Container image**: `trivy` runs in CI (`Image Scan` stage) against the built
  `score_flask` image, report-only for now (see the comment in `Jenkinsfile` for why
  it isn't a hard gate yet - a Trivy false-positive on pip's own vendored deps).
- **Code quality**: `ruff` (lint) and `black` (format) gate every build.

None of this is exhaustive - it's what's practical to run for a project at this tier.
See `TASKS.md` for what's still open.
