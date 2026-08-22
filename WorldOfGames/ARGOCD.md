# ArgoCD & GitOps Deployment

## Overview

This project deploys to Kubernetes using ArgoCD, a declarative GitOps
continuous-delivery controller. Git is the single source of truth for
cluster state; ArgoCD continuously reconciles the live cluster against the
manifests in this repository and corrects drift automatically.

This supersedes the previous deployment model, in which Jenkins ran
`docker-compose up` directly against the target environment. That model
coupled the CI pipeline to deployment authority and left cluster state with
no audit trail independent of Jenkins' own logs.

## GitOps Model

GitOps applies three properties to deployment:

1. **Declarative** — desired state is expressed as data (Kubernetes YAML),
   not as a sequence of imperative commands.
2. **Versioned and auditable** — desired state lives in Git. Every change to
   what runs in the cluster has a commit, an author, and a diff.
3. **Pulled, not pushed** — the deployment agent (ArgoCD) runs inside the
   target cluster and pulls changes from Git. No external CI system holds
   direct write credentials to the cluster.

ArgoCD's reconciliation loop compares two states — Git (desired) and the
live cluster (actual) — and converges the latter toward the former. It does
not build artifacts, run tests, or make deployment decisions; its sole
responsibility is convergence.

## Architecture

```
developer commit
      │
      ▼
Jenkins CI  ── build, test, scan, push image to Docker Hub
      │
      ▼
Jenkins bumps the image tag in manifests/score-flask.yaml, commits, pushes
      │
      ▼
Git (main)  ── source of truth
      │
      ▼  (polled continuously)
ArgoCD  ── diffs live cluster state against manifests/
      │
      ▼  (on drift)
Kubernetes cluster reconciled to match Git
```

Jenkins' write access is scoped to the Git repository only. It never
authenticates against the Kubernetes API and holds no cluster credentials.
ArgoCD is the sole actor with apply/delete authority over the
`world-of-games` namespace.

## Repository Layout

| Path | Resource | Notes |
|---|---|---|
| `manifests/namespace.yaml` | `Namespace` | `world-of-games` |
| `manifests/postgres.yaml` | `Deployment`, `PersistentVolumeClaim`, `Service` | Single replica by design — the PVC is `ReadWriteOnce`, so only one pod may mount it concurrently. `Recreate` deployment strategy avoids a two-pod overlap during rollout. |
| `manifests/postgres-secret.yaml` | `Secret` | Placeholder credentials committed for demo/local-cluster use only. Replace with sealed-secrets, SOPS, or an external secret manager before use against any non-ephemeral environment. |
| `manifests/score-flask.yaml` | `Deployment`, `Service` | Two replicas. Statelessness is a direct consequence of the Postgres migration (`Score.py`) — prior SQLite-file storage made horizontal scaling unsafe. |
| `manifests/argocd-application.yaml` | ArgoCD `Application` | The control object, not application state. Applied once, manually, into the `argocd` namespace. Excluded from ArgoCD's own sync scope (`spec.source.directory.exclude`) to prevent the controller from managing its own definition. |

## Sync Policy

The `Application` resource (`manifests/argocd-application.yaml`) is
configured with:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
```

- **`automated`** — sync runs on detected drift without manual approval.
- **`prune: true`** — resources removed from Git are deleted from the
  cluster on the next sync, keeping cluster state a strict mirror of Git.
- **`selfHeal: true`** — out-of-band changes to live resources (e.g. a
  manual `kubectl scale` or `kubectl edit`) are reverted on the next
  reconciliation pass. This was verified directly against the running
  cluster: scaling `score-flask` from 2 to 5 replicas via `kubectl scale`
  was reverted by ArgoCD within one reconciliation interval, with no manual
  intervention.

## Operational Notes

**Installation.** ArgoCD runs in-cluster, installed via the Argo Helm chart
into its own `argocd` namespace — consistent with how Jenkins itself is
installed (`values.yaml`, `helm install jenkins jenkins/jenkins`). Chart
defaults are in effect; no values file is currently checked into this repo.

**Deploy path.** The `Deploy (bump manifest)` stage in `Jenkinsfile` is the
only point at which the pipeline touches deployment state, and it does so
by editing a single line (the image tag) in `manifests/score-flask.yaml`
and pushing to `main`. It does not invoke `kubectl`, `helm`, or the
Kubernetes API in any form.

**Rollback.** Because deploy state is a Git history, rollback is a Git
operation. ArgoCD's History and Rollback view exposes every prior sync,
keyed to its commit SHA, and can revert the live cluster to any of them
without a corresponding Git revert — though a Git revert is the
recommended path to keep desired state and applied state consistent for
future syncs.

**Access.**

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

Authenticate as `admin` at `https://localhost:8080`. The initial admin
secret should be deleted after a real login mechanism (SSO/Dex, or a
rotated local user) is configured, per the Argo project's own guidance.

## References

- `readme.md` — project overview.
- `manifests/` — the desired-state manifests ArgoCD reconciles against.
- `CLAUDE.md` — codebase architecture reference.
