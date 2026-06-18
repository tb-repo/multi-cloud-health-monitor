# Validation Strategy — Multi-Cloud Resource Health Monitor

**Document Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-06-17  
**Framework Stage:** 6 — Validation & Verification

---

## Validation Approach

Validation is organized by sprint exit criteria. Each sprint must pass its validation checks before the next begins.

---

## Sprint 1 Validation (Foundation + Application)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| V1.1 | Docker Compose starts all containers | `docker-compose up -d` + `docker ps` | 5 containers running (nginx, app, db, prometheus, grafana) |
| V1.2 | Health endpoint responds | `curl http://localhost/health` | Returns 200 with JSON: status=healthy, db_connected=true |
| V1.3 | Dashboard renders | Open http://localhost in browser | Page loads with deployment info |
| V1.4 | Metrics endpoint works | `curl http://localhost/metrics` | Prometheus-format output |
| V1.5 | Prometheus scraping | Open http://localhost:9090/targets | Flask target shows "UP" |
| V1.6 | Grafana accessible | Open http://localhost:3000 | Dashboard loads with data |
| V1.7 | Database stores health checks | Query: `SELECT count(*) FROM health_checks` | Count > 0 after app runs for 1 minute |
| V1.8 | Lint passes | `ruff check .` + `terraform fmt -check` | Zero errors |

---

## Sprint 2 Validation (AWS Deployment)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| V2.1 | Terraform plan clean | `terraform plan` in aws/ | No errors; resources listed |
| V2.2 | Terraform apply succeeds | `terraform apply` | All resources created |
| V2.3 | ALB responds | `curl http://<alb-dns>/health` | Returns 200 with cloud_provider=aws |
| V2.4 | App accessible via ALB | Browser → ALB DNS | Dashboard loads |
| V2.5 | Prometheus running on AWS | `curl http://<ec2-ip>:9090` | Prometheus UI accessible |
| V2.6 | Grafana running on AWS | `curl http://<ec2-ip>:3000` | Grafana dashboard shows data |
| V2.7 | CI pipeline passes | Push code → GitHub Actions | Green pipeline |
| V2.8 | Terraform destroy clean | `terraform destroy` | All resources removed; $0 cost |

---

## Sprint 3 Validation (Azure + GCP)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| V3.1 | Azure terraform apply | `terraform apply` in azure/ | All resources created |
| V3.2 | Azure LB responds | `curl http://<azure-lb-ip>/health` | Returns 200 with cloud_provider=azure |
| V3.3 | Azure app functional | Browser → Azure LB IP | Dashboard loads |
| V3.4 | GCP terraform apply | `terraform apply` in gcp/ | All resources created |
| V3.5 | GCP LB responds | `curl http://<gcp-lb-ip>/health` | Returns 200 with cloud_provider=gcp |
| V3.6 | GCP app functional | Browser → GCP LB IP | Dashboard loads |
| V3.7 | Same Docker image on all 3 | Check image tag on each VM | Identical image running |
| V3.8 | All 3 teardowns clean | `terraform destroy` per cloud | All removed |

---

## Sprint 4 Validation (DNS Failover + DR)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| V4.1 | Route53 health checks active | AWS Console → Route53 → Health Checks | 3 health checks showing "Healthy" |
| V4.2 | DNS resolves to AWS (primary) | `nslookup app.domain.example` | Returns AWS ALB IP |
| V4.3 | Failover works | Stop AWS app → wait 90s → `nslookup` | Returns Azure LB IP |
| V4.4 | Failback works | Restart AWS app → wait 90s → `nslookup` | Returns AWS ALB IP again |
| V4.5 | DB backup created | Run backup script | pg_dump file exists in S3 |
| V4.6 | DB restore works | Restore on Azure + verify data | `SELECT count(*) FROM health_checks` matches |
| V4.7 | Full DR procedure | Execute runbook end-to-end | Complete in < 15 minutes |
| V4.8 | App shows multi-cloud status | Dashboard checks all 3 endpoints | Green/red indicators accurate |

---

## Sprint 5 Validation (Monitoring + Hardening)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| V5.1 | Monitoring on Azure | Access Grafana on Azure VM | Dashboard with data |
| V5.2 | Monitoring on GCP | Access Grafana on GCP VM | Dashboard with data |
| V5.3 | Security: no public DB | `nmap` DB port from internet | Port unreachable |
| V5.4 | Security: LB only path | Direct EC2 port 5000 from internet | Blocked by SG |
| V5.5 | End-to-end failover test | Scripted test: deploy all → kill AWS → verify Azure serves | Passes |
| V5.6 | Cost check | Review billing on all 3 clouds | Within budget |
| V5.7 | All containers healthy | `docker ps` on each cloud | All 5 containers running |

---

## Sprint 6 Validation (Final — Pre-Evaluation)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| V6.1 | DR rehearsal #1 | Team executes full DR | Success in < 15 min |
| V6.2 | DR rehearsal #2 | Different team member leads | Success in < 15 min |
| V6.3 | DR rehearsal #3 | Timed, recorded | Success in < 15 min; video captured |
| V6.4 | Documentation complete | Review all docs | README, deployment guide, architecture, DR runbook, ADRs |
| V6.5 | Clean deploy from scratch | Fresh terraform apply (all 3 clouds) | Everything works first try |
| V6.6 | Clean teardown | terraform destroy (all 3) | $0 resources remain |
| V6.7 | Presentation ready | Team presents to each other | Slides cover all deliverables |
| V6.8 | Video backup exists | Recorded DR demonstration | Video shows successful failover |

---

## Validation Evidence Artifacts

| Artifact | Location | Format |
|----------|----------|--------|
| Sprint validation screenshots | 06-validation/ | Screenshots or terminal output |
| Failover test recording | 06-validation/ | Video file or GIF |
| Cost report | 06-validation/ | Screenshot of billing per cloud |
| Security scan results | 06-validation/ | nmap output, SG verification |
| CI pipeline evidence | GitHub Actions UI | Link to passing pipeline |
| DR rehearsal log | 07-operations/dr-procedures/ | Timestamped execution log |

---

*Produced under AI Assisted Engineering Framework v1.0*
