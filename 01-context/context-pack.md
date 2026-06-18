# Context Pack — Multi-Cloud Resource Health Monitor

**Document Version:** 1.0  
**Status:** Draft — Pending Approval  
**Last Updated:** 2026-06-17  
**Framework Stage:** 2 — Requirements & Context Definition

---

## 1. Vision & Strategic Intent

### Vision Statement

A lightweight, cloud-agnostic web application deployed across AWS, Azure, and GCP that provides real-time visibility into multi-cloud deployment health, demonstrates automated failover, and serves as the workload for a Terraform-based multi-cloud infrastructure system.

### Strategic Alignment

This project is a Hero Vired Capstone Project demonstrating:

- Multi-cloud deployment using Terraform across AWS, Azure, and GCP
- Automated infrastructure creation and configuration management
- Load balancing and failover mechanisms across cloud providers
- Disaster recovery with data backup and restoration across clouds
- Monitoring and observability across all environments

### What This Project Delivers

Two complementary layers:

**Layer 1 — Infrastructure (Primary Capstone Deliverable):**
- Terraform modules that deploy consistently to AWS, Azure, and GCP
- Load balancers on each cloud fronting the application
- DNS-based health checking and failover routing
- Database backup/restore across cloud providers
- Prometheus + Grafana monitoring across all deployments
- CI/CD pipeline for infrastructure automation

**Layer 2 — Application (The Workload That Proves Infrastructure Works):**
- Multi-Cloud Resource Health Monitor web application
- Displays deployment health across all 3 clouds
- Records health check history in database (proves DR data recovery)
- Shows which cloud is currently serving requests
- Provides a compelling visual demo for evaluation

### What This Is NOT

- Not a production SaaS platform
- Not a cloud management tool for external users
- Not an inventory/discovery platform (simplified from earlier scope)
- Not an active-active multi-cloud system with real-time replication

---

## 2. Problem Statement

### Capstone Problem (Original)

In multi-cloud environments, managing resources across multiple cloud providers is complex and error-prone. Traditional deployment methods lack scalability, are prone to human error, and do not offer high availability across providers.

### How This Project Solves It

By building a Terraform-based infrastructure system that:
1. Deploys the same application to all 3 clouds consistently
2. Provides load balancing per cloud
3. Enables DNS-based failover when one cloud fails
4. Supports database backup/restore for DR
5. Monitors all deployments centrally

The Health Monitor application provides the visual proof that this infrastructure works.

---

## 3. Stakeholders & Team

| Role | Responsibility |
|------|---------------|
| Project Team (4–5 members) | Design, implement, demonstrate |
| Hero Vired Evaluator | Assess deliverables, conduct viva |

### Team Profile

- **Strong:** AWS, infrastructure, databases, operations, architecture
- **Moderate:** Terraform (basic to intermediate)
- **Learning:** Azure, GCP
- **Limited:** Software development (frontend/backend)

### Design Implications

- Application must be simple — team's strength is infrastructure, not development
- Maximum effort goes to Terraform, deployment, DR, monitoring (team's comfort zone)
- Application is minimal viable — just enough to demonstrate the infrastructure
- Prefer Python (scripting familiarity) over complex frameworks

---

## 4. Scope & Boundaries

### In Scope

| Category | Items |
|----------|-------|
| **Infrastructure (Primary Focus)** | |
| Terraform Modules | Reusable modules for AWS, Azure, GCP deployment |
| Cloud Resources | VMs/containers, load balancers, networking, security groups, DNS |
| Load Balancing | Per-cloud load balancer (ALB, Azure LB, GCP LB) |
| DNS Failover | Route53 (or equivalent) health checks + failover routing |
| Disaster Recovery | Database backup (pg_dump), cross-cloud restore, failover procedure |
| Monitoring | Prometheus + Grafana deployed alongside application on each cloud |
| CI/CD | GitHub Actions for Terraform validation and Docker image building |
| Credential Management | IAM Roles (AWS), Service Principal (Azure), Service Account (GCP) |
| **Application (Secondary Focus)** | |
| Health Monitor App | Python (Flask/FastAPI) + simple HTML/JS frontend |
| Health Dashboard | Shows cloud status, current serving cloud, uptime |
| Health History | Records health checks in PostgreSQL (proves DR data recovery) |
| Health Endpoint | /health for load balancer integration |
| Database | PostgreSQL (containerized) for health history storage |

### Explicitly Out of Scope

- Cloud resource inventory/discovery (moved to separate project)
- Cost management / FinOps
- Active-active multi-cloud (simultaneous traffic splitting)
- Real-time database replication across clouds
- Zero-downtime failover
- Complex UI (React/TypeScript — too much dev effort)
- Enterprise secret management (Vault)
- RBAC / multi-user authentication
- Scheduled jobs / background workers

---

## 5. Constraints

### Budget

| Provider | Budget | Approach |
|----------|--------|----------|
| AWS | ~USD $20 | Free-tier, t2.micro, teardown after demo |
| Azure | Free-tier/credits | Minimal resources for DR + deployment demo |
| GCP | Free-tier | Minimal resources for deployment demo |

### Timeline

- 6 sprints × 20 hours = 120 hours total
- Team of 4–5 members
- Primary effort on infrastructure (70%), application (20%), documentation (10%)

### Technology

| Layer | Choice | Reason |
|-------|--------|--------|
| IaC | Terraform (HCL) | Project requirement |
| Application | Python (Flask or FastAPI) | Team familiarity, simple |
| Frontend | Plain HTML + vanilla JS (or minimal Jinja2 templates) | No React — too complex for team |
| Database | PostgreSQL (container) | Simple, portable, familiar |
| Monitoring | Prometheus + Grafana | Project requirement |
| CI/CD | GitHub Actions | Team decision |
| DNS | Route53 (AWS) or CloudFlare | Failover routing |

### Skill Constraints

- Frontend: **Avoid React/TypeScript** — use server-rendered HTML or minimal vanilla JS
- Focus: Infrastructure and Terraform is where team excels
- Learning: Azure and GCP deployment patterns needed

---

## 6. Assumptions

| # | Assumption | Risk if Wrong |
|---|-----------|---------------|
| A1 | Free-tier accounts available on all 3 clouds | Budget exceeded |
| A2 | Route53 health checks work with external (Azure/GCP) endpoints | Failover mechanism broken |
| A3 | Same Docker image runs on all 3 clouds without modification | Portability claim fails |
| A4 | pg_dump/pg_restore works cross-cloud without issues | DR demonstration fails |
| A5 | Team can learn Azure + GCP Terraform providers within timeline | Multi-cloud deployment blocked |
| A6 | Simple Flask/FastAPI app is achievable in 20–30 hours | Application delivery delayed |
| A7 | DNS propagation is fast enough for live failover demo | Demo takes too long |

---

## 7. Key Risks (Summary)

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | Azure/GCP Terraform learning curve | Medium | High | AWS-first, then port to other clouds |
| R2 | DNS failover doesn't work as expected | Medium | High | Test early; have manual failover backup |
| R3 | Budget exceeded across 3 clouds | Medium | Medium | Free-tier only; immediate teardown |
| R4 | Load balancer config complexity | Medium | Medium | Simple LB config; single target per cloud |
| R5 | DR demo fails during viva | Low | High | Script everything; rehearse 3+ times; video backup |
| R6 | Application takes too long to build | Low | Medium | Keep app minimal; fallback to static page with health endpoint |

---

## 8. Decisions Made

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Health Monitor app instead of full Inventory Platform | Reduces application complexity by 70%; shifts focus to infrastructure |
| D2 | No React/TypeScript | Team cannot learn React + deliver infra in 120 hours; plain HTML sufficient |
| D3 | Flask/FastAPI over complex frameworks | Minimal, familiar, fast to build |
| D4 | DNS-based failover (not active-active) | Realistic for budget and timeline; demonstrates the concept |
| D5 | Backup/restore DR (not real-time replication) | Simpler, achievable, proves data recovery |
| D6 | Infrastructure is 70% of effort | Aligns with what capstone actually evaluates |

---

## 9. Evaluation Alignment

| Criterion | Weight | How We Address It |
|-----------|--------|-------------------|
| **Implementation** | 75% | Terraform multi-cloud deployment + LB + failover + DR + monitoring + working app |
| **Documentation** | 15% | Context Pack, Architecture Blueprint, ADRs, Runbooks, DR procedures, setup guides |
| **Cost Optimization** | 10% | Free-tier design, teardown scripts, Grafana cost awareness, documented decisions |

---

## 10. Project Structure

```
Multi-Cloud_Resource_Health_Monitor/
├── AGENTS.md
├── METADATA.md
├── 01-context/
│   └── context-pack.md
├── 02-requirements/
│   ├── requirements-specification.md
│   └── mvp-scope.md
├── 03-governance/
│   ├── risk-register.md
│   └── decision-register.md
├── 04-architecture/
│   ├── architecture-blueprint.md
│   └── adr/
├── 05-engineering/
│   ├── app/                    ← Application source code
│   ├── terraform/              ← Multi-cloud Terraform modules
│   │   ├── modules/
│   │   ├── environments/
│   │   │   ├── aws/
│   │   │   ├── azure/
│   │   │   └── gcp/
│   │   └── global/            ← DNS, cross-cloud config
│   ├── docker/                 ← Dockerfiles, compose
│   └── ci-cd/                  ← GitHub Actions workflows
├── 06-validation/
│   └── validation-report.md
├── 07-operations/
│   ├── runbooks/
│   ├── monitoring/
│   └── dr-procedures/
├── 08-intelligence/
│   ├── lessons-learned/
│   └── reusable-patterns/
└── AI_Interaction_Artifacts/   ← AI session logs
```

---

## Document Approval

| Role | Status | Date |
|------|--------|------|
| Project Team | Pending Review | 2026-06-17 |
| Framework Compliance | Aligned | 2026-06-17 |

---

*Produced under AI Assisted Engineering Framework v1.0*
