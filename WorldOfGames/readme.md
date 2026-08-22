# World of Games 🎮

A tiny website with three games (Memory, Guess-the-Number, Currency Roulette) and a
score counter. It also comes with its own robot helper (Jenkins) that automatically
tests and packages the app every time the code changes.

This readme explains everything like you've never touched Docker or Jenkins before.

## What's actually in here?

- **The website** (`MainScores.py` + `template/`): shows your score and lets you pick
  a game. Built with Flask (a small Python web framework).
- **The games** (`games/`, run via `MainGame.py`): play them in your terminal, not the
  browser. Winning adds points to your score.
- **The score** (`Score.py`): lives in a Postgres database, so it survives restarts and
  can be read/written by more than one copy of the website at once.
- **Jenkins** (`Jenkinsfile`, `values.yaml`): a robot that watches this GitHub repo. Every
  time someone pushes code, it automatically: checks for leaked passwords, checks the
  code style, checks for known security bugs in dependencies, builds the website into a
  package (a "Docker image"), runs the tests, and — if everything passes — publishes
  that package so it's ready to run anywhere.

## Running the website on your own computer

You need [Docker](https://docs.docker.com/get-docker/) installed. Then:

```bash
cd WorldOfGames
docker compose up -d --build
```

That single command builds the website and starts it. Open the URL it prints
(something like `http://localhost:5000`) in your browser.

To stop it:

```bash
docker compose down
```

## Playing the games

The games run in your terminal (not the browser) and use the same score:

```bash
docker exec -it score_flask python MainGame.py
```

Follow the prompts — pick a game, pick a difficulty, play. Winning updates your score,
which you can then see on the website.

## Setting up the Jenkins robot (optional, only if you want CI/CD)

This part is for running your own Jenkins on Kubernetes (via [minikube](https://minikube.sigs.k8s.io/)
for local testing, or any real cluster). Skip this if you just want to play the games.

```bash
helm install jenkins jenkins/jenkins -f values.yaml --namespace=jenkins
```

This installs Jenkins with everything pre-configured: it already knows about this
GitHub repo, already has the pipeline set up, and already has security settings
turned on (login required, no anonymous admin access). Once it's running:

1. Get to the Jenkins web UI (see "How do I actually open Jenkins?" below).
2. Log in as `admin` (get the password with the command in the same section).
3. Click the `world-of-games` job → **Build Now**. Or just push a commit to `main` —
   Jenkins checks for new commits automatically and builds on its own.

### How do I actually open Jenkins?

```bash
kubectl port-forward -n jenkins svc/jenkins 8090:8080
```

Then open `http://localhost:8090` in your browser. Leave that command running in its
own terminal while you use Jenkins.

### Admin password

```bash
kubectl exec -n jenkins jenkins-0 -- cat /run/secrets/additional/chart-admin-password
```

(This can change if you re-run `helm upgrade`. Re-run the command above if login
stops working.)

## What does the Jenkins robot actually check?

In plain English, every build goes through these steps in order:

1. **Secrets Scan** — makes sure nobody accidentally committed a password or API key.
2. **Lint** — makes sure the Python code follows good style rules.
3. **Format Check** — makes sure the code is formatted consistently.
4. **Dependency Audit** — checks if any library the app uses has a known security bug.
5. **Build** — packages the website into a Docker image.
6. **Image Scan** — checks that package for known security bugs too (this one just
   reports what it finds, it doesn't block the build — see `TASKS.md` for why).
7. **Run + Test** — starts the website and runs a real test against it.
8. **Finalize** — if everything above passed, publishes the image to Docker Hub.

If any step (except Image Scan) fails, the whole thing stops there — nothing broken
gets published.

## Where to look next

- **`CLAUDE.md`** — a deeper technical map of the codebase, for anyone (human or AI)
  making changes.
- **`TASKS.md`** — a running list of what's been fixed, what's deliberately left alone
  and why, and what's still open.
- **`SECURITY.md`** — what's scanned, what isn't, and the one known architecture risk
  (the Jenkins agent needs access to Docker itself to build images, which is a common
  but real security tradeoff — explained there in more detail).
- **`ARGOCD.md`** — how the website actually gets deployed to Kubernetes: Jenkins builds
  and pushes the image, then ArgoCD (not Jenkins) is the one that puts it live, by
  watching this repo's `manifests/` folder.
