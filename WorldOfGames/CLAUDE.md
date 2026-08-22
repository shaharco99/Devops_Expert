# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Flask app (`MainScores.py`) serving a score-tracking web UI for "World of Games" (WoG), plus standalone CLI game scripts under `games/` played via `MainGame.py`. The Flask app is the piece that gets containerized and deployed through Jenkins; `MainGame.py` and `games/*.py` are a separate console-based entry point (not wired into the Flask app).

## Running

Flask app locally:
```bash
flask --app MainScores.py run
```

Full stack via Docker:
```bash
docker-compose up -d
```
This builds and runs `score_flask` on port 5000 and defines a `tester` service that installs `requirements` and runs `pytest test.py` against the running `score` service (`http://score:5000/`, docker-compose network alias — tests are not meant to run standalone against localhost).

Run the CLI game menu inside the container:
```bash
docker exec -it score_flask python MainGame.py
```

## Testing

Single integration test in `test.py`, run against the live `score` service inside the compose network:
```bash
docker-compose run --rm tester
```
There is no unit-test suite decoupled from the running Flask service — `test.py` scrapes the rendered `index.html` for `id="score"` and asserts it's parseable as int.

## Architecture

- `MainScores.py` — Flask routes: `/` (renders current score from `Score.py`), `/gamepicker`, `/memorygame`, `/guessgame`, `/currency`, `/savegame`, and `/process_input` (POST form dispatch that redirects to the chosen game route by `game_chosen` int). 500 errors render `template/err500.html`.
- `Score.py` — reads/writes an integer score to `Scores.txt` (`add_score(diff)` computes `score += diff*3 + 5`). This is flat-file state, not a database — score persistence lives in `Scores.txt` at repo root and must be present in the container/volume for reads to succeed.
- `template/*.html` — one template per route above.
- `games/` — standalone CLI game logic (`CurrencyRouletteGame.py`, `GuessGame.py`, `MemoryGame.py`, `Live.py` for prompts/menu). Driven by `MainGame.py`, independent of the Flask routes/templates — the web UI does not currently call into these implementations.

## Deployment (Jenkins)

`Jenkinsfile` runs on a Kubernetes Jenkins agent using the `shaharco1804/world_of_game` image (built from `jenkinsslave/Dockerfile`) with the host's docker socket mounted, so `docker`/`docker-compose` commands inside the pipeline control the host's Docker daemon. Pipeline stages: verify `requirements` exists, remove any existing `score_flask` container, `docker build` the app image tagged `${DOCKER_HUB_REPO}:v<YYYYMMDD>`, bring the stack up with `docker-compose up -d --build`, run tests via `docker-compose run --rm tester`, then push the image to Docker Hub (`dockerhub` credentials) and tear the stack down. `docker-compose down` also runs in `post { always / failure }` for cleanup/debugging.

`jenkinsslave/` builds the Jenkins agent image itself (`world_of_game`) — separate from the app image (`score_flask`) built by the root `Dockerfile`. `values.yaml` / `init_jenkins.yaml` are Helm values for installing Jenkins on Kubernetes (`helm install jenkins jenkins/jenkins -f values.yaml --namespace=jenkins`).

## Notes

- Both `Dockerfile` (image `shaharco1804/score_flask`) and `docker-compose.yml` accept build args/env overrides (`image_name`, `image_version`, `DOCKER_HUB_REPO`, `imageVersion`) — don't hardcode these when editing.
- `requirements` (no `.txt` extension) is the dependency file used by both the app image and the Jenkins pipeline's existence check — keep the name as-is if touching build steps.
