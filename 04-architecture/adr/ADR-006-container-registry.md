# ADR-006: Docker Hub as Container Registry

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

The Docker image built by CI/CD needs to be pullable from all 3 clouds. We need a container registry strategy.

## Decision

Use **Docker Hub** (public repository) for storing the application image.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Docker Hub (public)** | Free; accessible from all clouds; simple; no auth needed for pull | Public — anyone can pull image |
| Docker Hub (private) | Private; 1 free private repo | Auth needed per cloud; token management |
| AWS ECR | Integrated with AWS; private | Not accessible from Azure/GCP without cross-cloud auth |
| Azure ACR | Integrated with Azure | Not accessible from other clouds easily |
| GCP GCR/Artifact Registry | Integrated with GCP | Not accessible from other clouds easily |
| Build on each VM | No registry needed | Slow; requires build tools on VM; wastes time on deploy |

## Consequences

**Positive:**
- `docker pull teamname/health-monitor:latest` works on any cloud without credentials
- CI/CD pushes once; all clouds pull the same image
- Zero configuration for image access
- Free (within Docker Hub limits)

**Negative:**
- Image is public — anyone can pull it
- Docker Hub rate limits (200 pulls/6h for anonymous) could theoretically be hit

**Acceptable because:**
- Application has no secrets baked into the image (all config via env vars)
- Academic project — no competitive or proprietary concern
- Rate limits won't be hit with 3 clouds pulling occasionally
- Documents this as explicit trade-off for simplicity

---

*AI Assisted Engineering Framework v1.0*
