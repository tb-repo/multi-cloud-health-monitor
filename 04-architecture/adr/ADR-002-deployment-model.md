# ADR-002: Single VM with Docker Compose per Cloud

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

We need to deploy the application stack (app, database, monitoring) on each of the three clouds. We must choose between managed container services (ECS, AKS, Cloud Run) and running Docker on a VM.

## Decision

Use a **single VM per cloud** running Docker Compose to host all containers (Nginx, Flask, PostgreSQL, Prometheus, Grafana).

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Single VM + Docker Compose** | Free-tier eligible, simple, portable, familiar | No auto-scaling; single point of failure within cloud |
| AWS ECS / Azure ACI / GCP Cloud Run | Managed, scalable, production-grade | Costs beyond free-tier; different per cloud; complex Terraform |
| Kubernetes (EKS/AKS/GKE) | Industry standard for containers | Massive overkill; expensive; complex; learning curve |
| Bare containers (no orchestration) | Minimal | Hard to manage multi-container dependencies |

## Consequences

**Positive:**
- Free-tier VMs available on all 3 clouds (t2.micro, B1s, e2-micro)
- Identical Docker Compose file works everywhere (true portability)
- Team already knows Docker and VM management
- Simple Terraform: just provision a VM and run docker-compose
- Easy local-to-cloud parity

**Negative:**
- No auto-scaling (acceptable — demo with minimal traffic)
- Single VM failure takes down all containers (acceptable — DR across clouds compensates)
- VM patching responsibility (acceptable — short-lived demo)

**Trade-off:** We sacrifice intra-cloud HA for simplicity and cost. Cross-cloud DR compensates for this at the infrastructure level.

---

*AI Assisted Engineering Framework v1.0*
