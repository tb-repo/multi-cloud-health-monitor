# Risk Register — Multi-Cloud Resource Health Monitor

**Document Version:** 1.0  
**Status:** Initial  
**Last Updated:** 2026-06-17  
**Framework Stage:** 3 — Governance & Risk Evaluation  
**Review Cadence:** Per sprint

---

## Risk Scoring

- Likelihood: 1 (Very Low) to 5 (Very High)
- Impact: 1 (Minimal) to 5 (Critical)
- Score = Likelihood × Impact
- Critical: 16–25 | High: 10–15 | Medium: 5–9 | Low: 1–4

---

## Active Risks

### R1 — Azure/GCP Terraform Learning Curve

| Attribute | Detail |
|-----------|--------|
| **Category** | Skills / Delivery |
| **Description** | Team is strong with AWS but learning Azure and GCP Terraform providers. Different resource naming, configuration patterns, and networking models may cause delays in Sprint 3. |
| **Likelihood** | 4 (High) |
| **Impact** | 3 (Medium) |
| **Risk Score** | 12 (High) |
| **Mitigation** | 1. AWS deployment completed first (Sprint 2) as reference pattern. 2. Map AWS concepts to Azure/GCP equivalents in team documentation. 3. Use AI-assisted Terraform generation. 4. Start with simplest resources (VM, VNet) before LB. |
| **Fallback** | Simplify Azure/GCP to minimal deployment (VM + Docker, skip LB if needed). |
| **Owner** | Infra Lead |

---

### R2 — DNS Failover Doesn't Work as Expected

| Attribute | Detail |
|-----------|--------|
| **Category** | Architecture / Delivery |
| **Description** | Route53 health checks against external (non-AWS) endpoints may have delays, DNS propagation may be slow, or failover routing may not work cleanly for the demonstration. |
| **Likelihood** | 3 (Medium) |
| **Impact** | 4 (High) |
| **Risk Score** | 12 (High) |
| **Mitigation** | 1. Set TTL to 60 seconds for quick failover. 2. Test failover early in Sprint 4 (don't leave to last minute). 3. Use Route53 failover routing policy (not latency or weighted). 4. Document expected failover time. |
| **Fallback** | If DNS failover is unreliable, demonstrate manual failover with documented procedure + show Route53 configuration as evidence of intent. |
| **Owner** | Infra Lead |

---

### R3 — Budget Exceeded Across 3 Clouds

| Attribute | Detail |
|-----------|--------|
| **Category** | Cost |
| **Description** | Running infrastructure on 3 clouds simultaneously (even briefly) can accumulate costs. Load balancers, public IPs, and compute instances all have costs beyond free tier on some providers. |
| **Likelihood** | 3 (Medium) |
| **Impact** | 3 (Medium) |
| **Risk Score** | 9 (Medium) |
| **Mitigation** | 1. Deploy and teardown in same session. 2. Never leave resources running overnight. 3. Set billing alerts on all 3 clouds. 4. Use smallest instance sizes (t2.micro, B1s, e2-micro). 5. Document cost of each deployment for Cost Optimization section. |
| **Fallback** | Keep only AWS running long-term; deploy Azure/GCP only for demo, teardown immediately. |
| **Owner** | Team Lead |

---

### R4 — Load Balancer Configuration Complexity

| Attribute | Detail |
|-----------|--------|
| **Category** | Architecture / Skills |
| **Description** | Each cloud has different LB concepts (ALB vs Azure LB vs GCP HTTP LB). Configuration, health checks, and target management differ significantly. |
| **Likelihood** | 3 (Medium) |
| **Impact** | 2 (Low) |
| **Risk Score** | 6 (Medium) |
| **Mitigation** | 1. Use simplest LB type per cloud. 2. AWS: ALB (well-documented). 3. Azure: Standard LB. 4. GCP: HTTP(S) LB. 5. Single backend target per LB (no complex routing). |
| **Fallback** | If LB on one cloud is problematic, use direct IP access for demo and document the LB configuration as "implemented but encountered X issue." |
| **Owner** | Infra Lead |

---

### R5 — DR Demonstration Fails During Viva

| Attribute | Detail |
|-----------|--------|
| **Category** | Delivery / Evaluation |
| **Description** | DR involves multiple steps (backup, deploy, restore, verify). Network issues, credential expiry, or Terraform state problems during live demo could cause failure. |
| **Likelihood** | 2 (Low) |
| **Impact** | 4 (High) |
| **Risk Score** | 8 (Medium) |
| **Mitigation** | 1. Script the entire DR procedure. 2. Rehearse 3+ times. 3. Record video backup of successful DR. 4. Keep Azure deployment pre-created (only do DB restore live). 5. Have all credentials verified day-of. |
| **Fallback** | Show video recording + walk through runbook + explain architecture. |
| **Owner** | Team Lead |

---

### R6 — Flask Application Takes Longer Than Expected

| Attribute | Detail |
|-----------|--------|
| **Category** | Delivery / Skills |
| **Description** | Although Flask is simpler than React, building a dashboard with cross-cloud health checking, database integration, and Prometheus metrics still requires development work the team isn't experienced with. |
| **Likelihood** | 2 (Low) |
| **Impact** | 3 (Medium) |
| **Risk Score** | 6 (Medium) |
| **Mitigation** | 1. Keep app extremely simple (1 page, 1 table, health endpoint). 2. Use AI-assisted development. 3. Use Flask-SQLAlchemy for DB access. 4. Use prometheus-flask-instrumentator for metrics. 5. Limit to Sprint 1 scope — don't add features. |
| **Fallback** | Reduce to: /health endpoint + static HTML page showing environment variables. Sufficient to prove infrastructure. |
| **Owner** | Python Lead |

---

### R7 — Terraform State Management Issues

| Attribute | Detail |
|-----------|--------|
| **Category** | Operations |
| **Description** | Managing Terraform state for 3 separate cloud deployments, especially with a team of 4-5, can lead to state conflicts, lock issues, or orphaned resources. |
| **Likelihood** | 3 (Medium) |
| **Impact** | 2 (Low) |
| **Risk Score** | 6 (Medium) |
| **Mitigation** | 1. Separate state per environment (aws/azure/gcp each have own state). 2. Use remote state backend (S3 + DynamoDB lock). 3. One person owns Terraform apply per environment. 4. Document who applies where. |
| **Fallback** | Use local state files if remote state setup is too complex. Accept risk of conflicts by coordinating verbally. |
| **Owner** | Infra Lead |

---

### R8 — Route53 Cost for Health Checks

| Attribute | Detail |
|-----------|--------|
| **Category** | Cost |
| **Description** | Route53 health checks cost $0.50/month each. 3 health checks + hosted zone ($0.50/month) = ~$2/month. Small but adds to tight budget. |
| **Likelihood** | 5 (Very High — certain cost) |
| **Impact** | 1 (Minimal) |
| **Risk Score** | 5 (Medium) |
| **Mitigation** | 1. Accept as necessary cost. 2. Teardown health checks after demo. 3. Document as part of Cost Optimization section (show awareness). |
| **Fallback** | None needed — cost is acceptable. |
| **Owner** | Team Lead |

---

### R9 — Docker Image Registry Access Across Clouds

| Attribute | Detail |
|-----------|--------|
| **Category** | Operations / Architecture |
| **Description** | The same Docker image needs to be pullable from AWS, Azure, and GCP. Using Docker Hub is simplest but public. Using per-cloud registries (ECR, ACR, GCR) adds complexity. |
| **Likelihood** | 2 (Low) |
| **Impact** | 2 (Low) |
| **Risk Score** | 4 (Low) |
| **Mitigation** | 1. Use Docker Hub (free tier, public repo) for simplicity. 2. Application is not sensitive — public image is acceptable for academic project. 3. Document as architecture decision. |
| **Fallback** | Build image directly on each cloud VM during Terraform provisioning (slower but eliminates registry dependency). |
| **Owner** | DevOps Lead |

---

## Risk Summary

| Priority | Count | Risks |
|----------|-------|-------|
| Critical (16–25) | 0 | — |
| High (10–15) | 2 | R1, R2 |
| Medium (5–9) | 6 | R3, R4, R5, R6, R7, R8 |
| Low (1–4) | 1 | R9 |

---

## Top 3 Risks Requiring Immediate Attention

| Rank | Risk | Score | Key Action |
|------|------|-------|-----------|
| 1 | R1 — Azure/GCP Terraform learning | 12 | Start learning in Sprint 1; use AWS patterns as template |
| 2 | R2 — DNS failover reliability | 12 | Test early in Sprint 4; don't leave to Sprint 6 |
| 3 | R3 — Budget across 3 clouds | 9 | Set billing alerts immediately; document deploy/teardown process |

---

## Key Observation

**No Critical (16+) risks exist in this project.** This is because:
1. The application is intentionally simple (Flask, not React)
2. Infrastructure is the team's core competency
3. The scope is tightly bounded
4. Fallbacks exist for every major risk

This is a significant improvement over the original Inventory Platform scope which had two Critical risks (R1, R14) related to development experience.

---

*Produced under AI Assisted Engineering Framework v1.0*
