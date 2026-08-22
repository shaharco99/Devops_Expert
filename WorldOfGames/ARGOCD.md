# ArgoCD, explained like you've never touched Kubernetes before

## The problem it solves

Old way (what this project used to do): Jenkins builds the Docker image, then
Jenkins itself runs `docker-compose up` to put the new version live. Jenkins is
both the builder *and* the one pushing the button to deploy.

Problem with that: nobody else can see what's actually running without asking
Jenkins. If someone changes something on the live server by hand, there's no
record of it. And Jenkins needs deep access to the production environment just
to do its job.

## The GitOps idea

ArgoCD flips it around: **a Git repo is the single source of truth for what
should be running.** Not a Jenkins log, not someone's memory of what they
typed — a folder of YAML files in Git.

ArgoCD's whole job is to sit there, watch that folder, and constantly check
one thing: *"does the cluster match what's in Git?"* If it doesn't match, it
fixes the cluster to match. That's it. It never asks "what should I build" —
it only asks "does reality match the file."

## How it works, mechanically

1. You write Kubernetes YAML files describing what you want running
   (`manifests/postgres.yaml`, `manifests/score-flask.yaml` in this repo).
2. You tell ArgoCD "watch this repo, this folder, this branch" — that's the
   `manifests/argocd-application.yaml` file.
3. ArgoCD polls the repo (every few minutes, or instantly via webhook) and
   compares the YAML there against what's actually deployed.
4. Mismatch → ArgoCD applies the YAML from Git to the cluster automatically
   (this project has `selfHeal: true`, so it also undoes any manual changes
   someone makes directly on the cluster — Git always wins).

Jenkins' job shrinks to: build the image, push it to Docker Hub, then edit
*one line* in a YAML file (the image tag) and push that to Git. Jenkins never
touches the cluster. ArgoCD notices the file changed and does the actual
deploying.

```
you push code → Jenkins builds+tests+pushes image → Jenkins bumps the
image tag in manifests/score-flask.yaml and pushes to Git → ArgoCD notices
the file changed → ArgoCD applies it to the cluster
```

## How it's wired up in this project

- **`manifests/`** — the "desired state" folder ArgoCD watches. Contains:
  - `namespace.yaml` — the `world-of-games` namespace everything lives in.
  - `postgres.yaml` — the score database (Deployment + PVC + Service).
    Single replica only — SQLite-style single-writer isn't the reason here,
    it's that a plain PVC can only attach to one pod at a time.
  - `postgres-secret.yaml` — DB credentials. **Placeholder values, not real
    secrets** — see the warning comment in that file before using this
    against anything that matters.
  - `score-flask.yaml` — the website itself (Deployment + Service). Two
    replicas, because the score now lives in Postgres instead of a local
    file, so any replica can serve any request.
  - `argocd-application.yaml` — the ArgoCD `Application` object. This is the
    one file that isn't "app state," it's "instructions telling ArgoCD what
    to watch." Applied once, by hand, into the `argocd` namespace — it's not
    itself synced by ArgoCD (see its `directory.exclude`).
- **Jenkinsfile, `Deploy (bump manifest)` stage** — after a successful
  build+test+push, `sed`-replaces the image tag in `manifests/score-flask.yaml`
  and pushes that single-line change to `main`. This is the *only* deploy
  action Jenkins takes; everything after that is ArgoCD's job.
- **ArgoCD itself** — installed with Helm into the `argocd` namespace,
  same pattern as the Jenkins install (`helm install argocd argo/argo-cd -n
  argocd`). Not checked into this repo as a values file yet — it was
  installed with chart defaults.

## Seeing it for yourself

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open `https://localhost:8080`, log in as `admin` with:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

You'll see the `world-of-games` Application, its sync status, and a live
diagram of every resource it manages.

## Where to look next

- **`readme.md`** — the plain-English overview of the whole project.
- **`manifests/`** — the actual YAML ArgoCD watches.
- **`CLAUDE.md`** — deeper technical map of the codebase.
