# Devops_Expert

Course work from the DevOps Expert course: weekly lesson exercises plus the final
project, **World of Games**, which I have since extended with a security-gated
Jenkins pipeline, Postgres, and a GitOps deployment to Kubernetes with ArgoCD.

The lesson folders are learning exercises and are kept as written during the
course. `WorldOfGames/` is the maintained part of the repository.

## World of Games (final project)

A Flask web app that shows a player's score, CLI games that add to it, and the
pipeline that ships it.

```text
Jenkins (Kubernetes agent)
  Secrets Scan (gitleaks) → Lint (ruff) → Format (black) → Dependency Audit (pip-audit)
  → Build image → Image Scan (Trivy, report-only) → Run with docker compose → Test (pytest)
  → Push to Docker Hub → Bump image tag in manifests/ and push
ArgoCD
  watches WorldOfGames/manifests/ and syncs the cluster (namespace world-of-games)
```

- **App** — `MainScores.py` (Flask), `Score.py` (score in Postgres, atomic
  increments), `games/` and `MainGame.py` (terminal games).
- **Containers** — `Dockerfile` (non-root, pinned `python:3.13-alpine`),
  `docker-compose.yml` (Postgres, app, and a tester service).
- **CI/CD** — `Jenkinsfile`; `values.yaml` installs Jenkins on Kubernetes with
  the job preconfigured; `jenkinsslave/` builds the pipeline's agent image.
- **Deployment** — `manifests/` (namespace, Postgres, app, ArgoCD
  `Application`); see `WorldOfGames/ARGOCD.md`.
- **Security notes** — `WorldOfGames/SECURITY.md` (including the known
  Docker-socket risk of the Jenkins agent) and `WorldOfGames/TASKS.md`.

Run it locally (needs Docker):

```bash
cd WorldOfGames
docker compose up -d --build              # Postgres + app on http://localhost:5000
docker compose run --rm tester            # integration test against the running app
docker exec -it score_flask python MainGame.py   # play; wins add to the score
docker compose down
```

Example test output:

```text
test.py::test_scores_service PASSED                                      [100%]
============================== 1 passed in 0.05s ===============================
```

`WorldOfGames/readme.md` is a step-by-step guide, including Jenkins setup.

## Lessons

| Folder | Topic |
| --- | --- |
| `lesson_1` | Python basics: variables, lists, dictionaries |
| `lesson_2` | Python functions and conditionals |
| `lesson_3` | File I/O and a minimal Flask app |
| `lesson_4` | Selenium test of an HTML/JS tip calculator |
| `lesson_10` | Kubernetes Deployments and Services for Airflow, Jenkins, Superset, Weave Scope |
| `lesson_11` | A Helm chart with values files for Airflow and Superset |
| `lesson_12` | Launching EC2 instances with boto3 |
