# MVP Scope Definition — Multi-Cloud Resource Health Monitor

**Document Version:** 1.0  
**Status:** Draft — Pending Approval  
**Last Updated:** 2026-06-17  
**Framework Stage:** 2 — Requirements Scoping

---

## Effort Allocation Strategy

| Focus Area | Effort % | Rationale |
|-----------|----------|-----------|
| **Infrastructure (Terraform, LB, DNS, DR)** | 50% | Core capstone deliverable; team strength |
| **Application (Flask, DB, templates)** | 20% | Minimal viable workload to prove infra works |
| **Monitoring (Prometheus, Grafana)** | 15% | Required by capstone; demonstrates observability |
| **CI/CD + Documentation** | 15% | Required by capstone; evaluation criterion |

---

## Sprint Plan

### Sprint 1: Foundation + Application (40 hours team)

**Objective:** Working application locally; Terraform provider setup for all 3 clouds

| Task | Owner Skill | Effort | Deliverable |
|------|-------------|--------|-------------|
| Project repo + structure + .gitignore + branch protection | DevOps | 2h | GitHub repo ready |
| Flask application skeleton (routes, templates, health endpoint) | Python | 8h | App runs locally, /health returns JSON |
| PostgreSQL schema + migrations (health_checks table) | DBA | 4h | DB ready with migration |
| Docker Compose (app + db + prometheus + grafana) | DevOps | 6h | `docker-compose up` works end-to-end |
| Jinja2 dashboard template (health status page) | Python | 8h | Dashboard displays data from DB |
| Prometheus metrics endpoint + Grafana dashboard config | DevOps | 6h | Monitoring working locally |
| Terraform provider configs (AWS + Azure + GCP) initialized | Infra | 6h | `terraform init` succeeds for all 3 |

**Exit Criteria:** `docker-compose up` → app accessible → health checks recording → Grafana dashboard live

---

### Sprint 2: AWS Deployment (40 hours team)

**Objective:** Complete application deployed to AWS via Terraform

| Task | Owner Skill | Effort | Deliverable |
|------|-------------|--------|-------------|
| Terraform module: VPC + subnets + security groups | Infra | 8h | Networking module reusable |
| Terraform module: EC2 (or ECS) + Docker deployment | Infra | 10h | App container running on AWS |
| Terraform module: ALB + health check + target group | Infra | 8h | LB forwards traffic; health check passes |
| Terraform module: PostgreSQL container on EC2 | Infra | 4h | DB accessible from app |
| Terraform module: Prometheus + Grafana on EC2 | DevOps | 4h | Monitoring running alongside app |
| CI/CD: GitHub Actions (lint + test + docker build + terraform validate) | DevOps | 6h | Pipeline passes |

**Exit Criteria:** `terraform apply` on AWS → app accessible via ALB → monitoring live → CI pipeline green

---

### Sprint 3: Azure + GCP Deployment (40 hours team)

**Objective:** Same application deployed to Azure and GCP via Terraform

| Task | Owner Skill | Effort | Deliverable |
|------|-------------|--------|-------------|
| Terraform Azure: Resource Group + VNet + NSG | Infra | 6h | Azure networking ready |
| Terraform Azure: VM + Docker + app deployment | Infra | 8h | App running on Azure |
| Terraform Azure: Load Balancer + health check | Infra | 6h | Azure LB forwards traffic |
| Terraform GCP: VPC + firewall rules | Infra | 6h | GCP networking ready |
| Terraform GCP: Compute Engine + Docker + app deployment | Infra | 8h | App running on GCP |
| Terraform GCP: Load Balancer + health check | Infra | 6h | GCP LB forwards traffic |

**Exit Criteria:** All 3 clouds have working deployments via Terraform; app accessible on each

---

### Sprint 4: DNS Failover + DR (40 hours team)

**Objective:** Route53 failover working; DR procedure tested

| Task | Owner Skill | Effort | Deliverable |
|------|-------------|--------|-------------|
| Route53 hosted zone + health checks (AWS, Azure, GCP endpoints) | Infra | 6h | Health checks active |
| Route53 failover routing policy (primary AWS → secondary Azure) | Infra | 6h | Failover routing configured |
| Failover testing: stop AWS → verify DNS routes to Azure | Infra | 4h | Failover demonstrated |
| DB backup script (pg_dump → S3) | DBA | 4h | Backup script working |
| DB restore script (S3 → Azure PostgreSQL) | DBA | 4h | Restore script working |
| DR full procedure test (backup → Azure deploy → restore → verify) | Team | 8h | DR complete in < 15 min |
| DR runbook documentation | Docs | 4h | Step-by-step runbook |
| Update app to check/display health of all 3 cloud endpoints | Python | 4h | Dashboard shows multi-cloud status |

**Exit Criteria:** DNS failover works; DR procedure documented and tested; dashboard shows all 3 clouds

---

### Sprint 5: Monitoring + Integration Testing (40 hours team)

**Objective:** Full monitoring across all clouds; integration testing; hardening

| Task | Owner Skill | Effort | Deliverable |
|------|-------------|--------|-------------|
| Prometheus + Grafana deployed on Azure (same pattern as AWS) | DevOps | 4h | Azure monitoring live |
| Prometheus + Grafana deployed on GCP (same pattern as AWS) | DevOps | 4h | GCP monitoring live |
| Grafana dashboard: multi-cloud health overview | DevOps | 6h | Dashboard shows all clouds |
| Integration testing: full failover scenario end-to-end | Team | 8h | Scripted test passes |
| Load balancer verification on all 3 clouds | Infra | 4h | LBs handling traffic correctly |
| Security verification: SG/firewall rules, no public DB access | Security | 4h | Security audit passes |
| Cost verification: all resources within free-tier | FinOps | 2h | Cost estimate documented |
| Bug fixes and stabilization | Team | 8h | All issues resolved |

**Exit Criteria:** All 3 clouds fully operational with monitoring; failover tested; security verified

---

### Sprint 6: Documentation + Final Demo Prep (40 hours team)

**Objective:** Production-ready documentation; DR rehearsed; evaluation-ready

| Task | Owner Skill | Effort | Deliverable |
|------|-------------|--------|-------------|
| Architecture Blueprint document | Arch | 6h | Full architecture documented |
| ADRs (minimum 5: tech stack, multi-cloud pattern, failover approach, DR strategy, monitoring) | Team | 6h | ADRs complete |
| Setup guide + deployment documentation | Docs | 6h | Setup docs complete |
| DR rehearsal #1 | Team | 3h | Successful DR |
| DR rehearsal #2 | Team | 3h | Successful DR |
| DR rehearsal #3 | Team | 3h | Successful DR |
| Video recording of successful DR | Team | 2h | Backup video exists |
| Presentation preparation | Team | 6h | Slides ready |
| Final cleanup + teardown scripts verified | DevOps | 3h | Clean teardown works |
| Lessons learned + reusable patterns | Team | 2h | 08-intelligence populated |

**Exit Criteria:** All documentation complete; DR rehearsed 3x; presentation ready; team confident

---

## Team Capability Alignment

| Sprint | Primary Skills Needed | Team Readiness |
|--------|----------------------|---------------|
| Sprint 1 | Python, Docker, SQL | ✅ Strong (Python scripting + Docker + DB) |
| Sprint 2 | Terraform AWS | ✅ Strong (AWS is team's core competency) |
| Sprint 3 | Terraform Azure + GCP | ⚠️ Moderate (learning new providers) |
| Sprint 4 | DNS, DR, scripting | ✅ Strong (operational/infra skills) |
| Sprint 5 | Monitoring, testing | ✅ Strong (ops background) |
| Sprint 6 | Documentation | ✅ Strong (writing, presenting) |

**Highest Risk Sprint:** Sprint 3 (Azure + GCP Terraform) — mitigated by doing AWS first and porting patterns.

---

## Minimum Viable Capstone (If Time Runs Short)

If the team falls behind, this is the absolute minimum for a passing capstone:

| Component | Status |
|-----------|--------|
| App running on AWS via Terraform | Non-negotiable |
| App running on Azure via Terraform | Non-negotiable |
| App running on GCP via Terraform | Can be shown via `terraform plan` if deploy fails |
| DNS failover (AWS → Azure) | Non-negotiable |
| DR demonstration | Non-negotiable (even if simplified) |
| Monitoring on at least one cloud | Non-negotiable |
| Documentation | Non-negotiable (15% of grade) |
| Load balancers on all 3 clouds | Can simplify to direct IP if LB is problematic |

---

## Document Approval

| Role | Status | Date |
|------|--------|------|
| Project Team | Pending | 2026-06-17 |

---

*Produced under AI Assisted Engineering Framework v1.0*
