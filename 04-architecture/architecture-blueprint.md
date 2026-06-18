# Architecture Blueprint — Multi-Cloud Resource Health Monitor

**Document Version:** 1.0  
**Status:** Draft — Pending Approval  
**Last Updated:** 2026-06-17  
**Framework Stage:** 4 — Architecture & Solution Design

---

## 1. Architecture Overview

### System Context

The Multi-Cloud Resource Health Monitor is a two-layer system:

- **Layer 1 (Infrastructure):** Terraform-managed multi-cloud deployment with load balancing, DNS failover, and disaster recovery
- **Layer 2 (Application):** A lightweight Flask web application that monitors and displays the health of all cloud deployments

The application is the workload that proves the infrastructure works.

### High-Level Architecture

```
                          ┌──────────────────────────┐
                          │       USERS / DEMO       │
                          └────────────┬─────────────┘
                                       │
                          ┌────────────▼─────────────┐
                          │    Route53 DNS Failover   │
                          │    app.project.example    │
                          │                          │
                          │  Primary: AWS ALB         │
                          │  Secondary: Azure LB      │
                          │  Tertiary: GCP LB         │
                          └──┬──────────┬──────────┬─┘
                             │          │          │
              ┌──────────────▼──┐  ┌────▼────────┐ ┌▼──────────────┐
              │   AWS (Primary)  │  │Azure (Standby)│ │GCP (Tertiary) │
              │                  │  │              │ │               │
              │  ┌────────────┐  │  │ ┌──────────┐│ │ ┌───────────┐│
              │  │    ALB     │  │  │ │ Azure LB ││ │ │  GCP LB   ││
              │  └─────┬──────┘  │  │ └────┬─────┘│ │ └─────┬─────┘│
              │        │         │  │      │      │ │       │      │
              │  ┌─────▼──────┐  │  │ ┌────▼─────┐│ │ ┌─────▼─────┐│
              │  │  EC2/ECS   │  │  │ │  Azure VM││ │ │  GCE VM   ││
              │  │            │  │  │ │          ││ │ │           ││
              │  │ ┌────────┐ │  │  │ │┌────────┐││ │ │┌────────┐ ││
              │  │ │  Flask  │ │  │  │ ││ Flask  │││ │ ││ Flask  │ ││
              │  │ │  App    │ │  │  │ ││ App    │││ │ ││ App    │ ││
              │  │ └────┬───┘ │  │  │ │└───┬────┘││ │ │└───┬────┘ ││
              │  │      │     │  │  │ │    │     ││ │ │    │      ││
              │  │ ┌────▼───┐ │  │  │ │┌───▼────┐││ │ │┌───▼────┐ ││
              │  │ │PostgreSQL│ │  │  │ ││PostgreSQL│││ │ ││PostgreSQL│││
              │  │ └────────┘ │  │  │ │└────────┘││ │ │└────────┘ ││
              │  │            │  │  │ │          ││ │ │           ││
              │  │ ┌────────┐ │  │  │ │┌────────┐││ │ │┌────────┐ ││
              │  │ │Prometh. │ │  │  │ ││Prometh.│││ │ ││Prometh.│ ││
              │  │ │+Grafana │ │  │  │ ││+Grafana│││ │ ││+Grafana│ ││
              │  │ └────────┘ │  │  │ │└────────┘││ │ │└────────┘ ││
              │  └────────────┘  │  │ └──────────┘│ │ └───────────┘│
              └──────────────────┘  └─────────────┘ └──────────────┘
```

---

## 2. Component Architecture

### 2.1 Application Stack (Per Cloud — Identical)

Each cloud deployment runs the identical stack:

```
┌─────────────────────────────────────────────────┐
│  Docker Host (EC2 / Azure VM / GCE VM)          │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Nginx (Reverse Proxy)      Port 80     │    │
│  │  - Forwards to Gunicorn on port 5000    │    │
│  │  - Serves static files                  │    │
│  │  - Health check passthrough             │    │
│  └──────────────────┬──────────────────────┘    │
│                     │                           │
│  ┌──────────────────▼──────────────────────┐    │
│  │  Gunicorn + Flask App       Port 5000   │    │
│  │  - /health         → Health check JSON  │    │
│  │  - /metrics        → Prometheus metrics │    │
│  │  - /               → Dashboard (Jinja2) │    │
│  │  - /api/checks     → Health history API │    │
│  └──────────────────┬──────────────────────┘    │
│                     │                           │
│  ┌──────────────────▼──────────────────────┐    │
│  │  PostgreSQL                 Port 5432   │    │
│  │  - health_checks table                  │    │
│  │  - deployment_info table                │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Prometheus                 Port 9090   │    │
│  │  - Scrapes Flask /metrics               │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Grafana                    Port 3000   │    │
│  │  - Pre-provisioned dashboard            │    │
│  │  - Datasource: local Prometheus         │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### 2.2 Container Composition

| Container | Image | Port | Purpose |
|-----------|-------|------|---------|
| nginx | nginx:alpine | 80 | Reverse proxy, static files |
| app | custom (Flask + Gunicorn) | 5000 | Application logic |
| db | postgres:15-alpine | 5432 | Health check history storage |
| prometheus | prom/prometheus:latest | 9090 | Metrics collection |
| grafana | grafana/grafana:latest | 3000 | Metrics visualization |

### 2.3 Application Routes

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | No | Dashboard page (Jinja2 template) |
| `/health` | GET | No | Health check endpoint (JSON) — used by LB and Route53 |
| `/metrics` | GET | No | Prometheus metrics endpoint |
| `/api/checks` | GET | No | Health check history (JSON, last 50) |
| `/api/status` | GET | No | Multi-cloud status (checks all endpoints) |


---

## 3. Network Architecture (Per Cloud)

### 3.1 AWS Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│  VPC: 10.0.0.0/16                                               │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Public Subnet: 10.0.1.0/24 (us-east-1a)              │     │
│  │                                                        │     │
│  │  ┌──────────────┐                                     │     │
│  │  │     ALB      │ ← Internet traffic                  │     │
│  │  └──────┬───────┘                                     │     │
│  │         │                                             │     │
│  │  ┌──────▼───────┐                                     │     │
│  │  │   EC2 (t2.micro)                                   │     │
│  │  │   - Docker Host                                    │     │
│  │  │   - All containers                                 │     │
│  │  │   - Security Group: allow 80 from ALB              │     │
│  │  │                     allow 3000 from your IP        │     │
│  │  │                     allow 9090 from your IP        │     │
│  │  └──────────────┘                                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
│  Internet Gateway attached                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Key AWS Resources (Terraform):**
- VPC + Internet Gateway
- Public Subnet (single AZ — cost constraint)
- Security Group (app: 80 from ALB, monitoring: 3000/9090 from admin IP)
- EC2 instance (t2.micro, free-tier)
- Application Load Balancer + Target Group + Listener
- IAM Role (EC2 instance profile for S3 backup access)
- S3 Bucket (database backups)

### 3.2 Azure Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│  Resource Group: rg-health-monitor                              │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  VNet: 10.1.0.0/16                                    │     │
│  │  Subnet: 10.1.1.0/24                                  │     │
│  │                                                        │     │
│  │  ┌──────────────┐                                     │     │
│  │  │  Azure LB    │ ← Internet traffic (Public IP)      │     │
│  │  └──────┬───────┘                                     │     │
│  │         │                                             │     │
│  │  ┌──────▼───────┐                                     │     │
│  │  │  VM (B1s)    │                                     │     │
│  │  │  - Docker Host                                     │     │
│  │  │  - All containers                                  │     │
│  │  │  - NSG: allow 80 from LB                           │     │
│  │  └──────────────┘                                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
│  Storage Account (DB backups)                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Key Azure Resources (Terraform):**
- Resource Group
- VNet + Subnet
- Network Security Group
- Public IP
- Standard Load Balancer + Backend Pool + Health Probe
- VM (B1s — free tier 750h/month)
- Storage Account + Container (backups)

### 3.3 GCP Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│  Project: health-monitor-gcp                                    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  VPC Network: health-monitor-vpc                       │     │
│  │  Subnet: 10.2.0.0/24 (us-central1)                    │     │
│  │                                                        │     │
│  │  ┌──────────────┐                                     │     │
│  │  │  HTTP(S) LB  │ ← Internet traffic                  │     │
│  │  └──────┬───────┘                                     │     │
│  │         │                                             │     │
│  │  ┌──────▼───────┐                                     │     │
│  │  │ GCE (e2-micro)│                                    │     │
│  │  │  - Docker Host │                                    │     │
│  │  │  - All containers                                  │     │
│  │  │  - Firewall: allow 80 from LB                      │     │
│  │  └──────────────┘                                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
│  Cloud Storage Bucket (DB backups)                              │
└─────────────────────────────────────────────────────────────────┘
```

**Key GCP Resources (Terraform):**
- VPC Network + Subnet
- Firewall Rules
- Compute Engine Instance (e2-micro — free tier)
- HTTP(S) Load Balancer + Backend Service + Health Check
- Cloud Storage Bucket (backups)

---

## 4. DNS Failover Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Route53 Configuration                      │
│                                                             │
│  Hosted Zone: project-domain.example                        │
│                                                             │
│  Record: app.project-domain.example                         │
│  Type: A (Alias)                                            │
│  Routing Policy: Failover                                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  PRIMARY Record                                      │   │
│  │  Target: AWS ALB DNS name                            │   │
│  │  Health Check: HC-AWS (checks AWS ALB /health)       │   │
│  │  Failover: PRIMARY                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SECONDARY Record                                    │   │
│  │  Target: Azure LB Public IP                          │   │
│  │  Health Check: HC-Azure (checks Azure LB /health)    │   │
│  │  Failover: SECONDARY                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Health Checks:                                             │
│  - HC-AWS:   GET /health on AWS ALB, interval 10s          │
│  - HC-Azure: GET /health on Azure LB, interval 10s         │
│  - HC-GCP:   GET /health on GCP LB, interval 10s (monitor) │
│                                                             │
│  TTL: 60 seconds (fast failover)                            │
└─────────────────────────────────────────────────────────────┘

Failover Flow:
─────────────
1. Normal: DNS → AWS ALB → Flask App (AWS)
2. AWS fails: HC-AWS marks unhealthy (3 failures × 10s = 30s)
3. Route53 returns SECONDARY record
4. DNS → Azure LB → Flask App (Azure)
5. Total failover time: ~60–90 seconds (30s detection + 60s TTL)
```

---

## 5. Disaster Recovery Architecture

### DR Strategy: Warm Standby + Backup/Restore

```
┌─────────────────────────────────────────────────────────────────┐
│                    NORMAL OPERATION                               │
│                                                                  │
│  AWS (ACTIVE)         Azure (STANDBY)        GCP (DEPLOYABLE)   │
│  ┌──────────────┐    ┌──────────────┐        ┌──────────────┐  │
│  │ App: Running │    │ App: Running │        │ App: Off     │  │
│  │ DB: Active   │    │ DB: Empty/Old│        │ DB: N/A      │  │
│  │ LB: Active   │    │ LB: Active   │        │ Terraform:   │  │
│  │              │    │ (no traffic) │        │ Ready        │  │
│  └──────┬───────┘    └──────────────┘        └──────────────┘  │
│         │                                                        │
│         │  Periodic Backup                                       │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │ S3: DB Dumps │ ← pg_dump daily/on-demand                    │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DR ACTIVATION                                  │
│                                                                  │
│  Step 1: Detect AWS failure (Route53 health check fails)         │
│  Step 2: Retrieve latest backup from S3                          │
│  Step 3: Restore to Azure PostgreSQL (pg_restore)                │
│  Step 4: Azure app now has current data                          │
│  Step 5: Route53 automatically routes to Azure (failover)        │
│  Step 6: Verify application functional with restored data        │
│                                                                  │
│  AWS (DOWN)           Azure (NOW ACTIVE)     GCP (AVAILABLE)    │
│  ┌──────────────┐    ┌──────────────┐       ┌──────────────┐   │
│  │ App: Dead    │    │ App: Running │       │ Deploy if     │   │
│  │ DB: Unreachable│  │ DB: Restored │       │ Azure fails   │   │
│  │              │    │ LB: Serving  │       │ too           │   │
│  └──────────────┘    │ DNS: Active  │       └──────────────┘   │
│                      └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

### DR Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| **RPO (Recovery Point Objective)** | Last backup (minutes to hours) | Depends on backup frequency |
| **RTO (Recovery Time Objective)** | < 15 minutes | Backup restore + DNS failover |
| **Data Loss Window** | Since last backup | Acceptable for demo — not zero-loss |

### DR Procedure (Summary)

| Step | Action | Time | Tool |
|------|--------|------|------|
| 1 | Detect failure | 30s | Route53 health check (automatic) |
| 2 | DNS failover to Azure | 60s | Route53 (automatic) |
| 3 | Retrieve backup from S3 | 1 min | aws s3 cp |
| 4 | Restore DB on Azure | 2 min | pg_restore |
| 5 | Verify application | 1 min | curl /health + browser check |
| **Total** | | **~5 min** | |


---

## 6. Terraform Module Structure

```
terraform/
├── modules/                          # Reusable modules
│   ├── networking/                   # VPC/VNet/VPC-Network per cloud
│   │   ├── aws/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── azure/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   └── gcp/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   │
│   ├── compute/                      # VM/Instance per cloud
│   │   ├── aws/                      # EC2 + Docker setup
│   │   ├── azure/                    # Azure VM + Docker setup
│   │   └── gcp/                      # GCE + Docker setup
│   │
│   ├── loadbalancer/                 # LB per cloud
│   │   ├── aws/                      # ALB + Target Group
│   │   ├── azure/                    # Azure Standard LB
│   │   └── gcp/                      # GCP HTTP LB
│   │
│   ├── storage/                      # Object storage (backups)
│   │   ├── aws/                      # S3 bucket
│   │   ├── azure/                    # Storage Account
│   │   └── gcp/                      # Cloud Storage
│   │
│   └── dns/                          # Route53 failover
│       └── aws/                      # Hosted zone + health checks + records
│
├── environments/                     # Per-cloud root configs
│   ├── aws/
│   │   ├── main.tf                   # Composes modules for AWS
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars.example
│   │   └── backend.tf                # Remote state config
│   ├── azure/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars.example
│   │   └── backend.tf
│   └── gcp/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── terraform.tfvars.example
│       └── backend.tf
│
└── global/                           # Cross-cloud resources
    ├── dns/
    │   ├── main.tf                   # Route53 hosted zone + failover
    │   ├── variables.tf              # Endpoints from each cloud
    │   └── outputs.tf
    └── backend.tf
```

### Module Design Principles

| Principle | Application |
|-----------|-------------|
| **One module per concern** | Networking, Compute, LB, Storage are separate modules |
| **Provider-specific implementations** | Each module has aws/, azure/, gcp/ subdirectories |
| **Common interface** | Each module exposes similar outputs (e.g., `public_ip`, `lb_dns_name`) |
| **Environment composition** | environments/aws/main.tf composes all AWS modules together |
| **Separate state per environment** | AWS, Azure, GCP each have independent Terraform state |
| **Global layer for cross-cloud** | DNS failover references outputs from all 3 environments |

---

## 7. Data Architecture

### Database Schema

```sql
-- Health check history (core data — proves DR works)
CREATE TABLE health_checks (
    id              SERIAL PRIMARY KEY,
    timestamp       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    cloud_provider  VARCHAR(10) NOT NULL,      -- aws, azure, gcp
    target_cloud    VARCHAR(10) NOT NULL,       -- which cloud was checked
    status          VARCHAR(10) NOT NULL,       -- healthy, unhealthy, timeout
    response_time_ms INTEGER,                   -- response time in milliseconds
    details         JSONB                       -- additional info
);

-- Deployment info (identifies this instance)
CREATE TABLE deployment_info (
    id              SERIAL PRIMARY KEY,
    cloud_provider  VARCHAR(10) NOT NULL,
    region          VARCHAR(50) NOT NULL,
    instance_id     VARCHAR(100),
    deployed_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version         VARCHAR(20)
);

-- Failover events (records when failover occurred)
CREATE TABLE failover_events (
    id              SERIAL PRIMARY KEY,
    timestamp       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    from_cloud      VARCHAR(10) NOT NULL,
    to_cloud        VARCHAR(10) NOT NULL,
    reason          TEXT,
    duration_seconds INTEGER
);

-- Indexes for query performance
CREATE INDEX idx_health_checks_timestamp ON health_checks(timestamp DESC);
CREATE INDEX idx_health_checks_target ON health_checks(target_cloud);
```

### Data Flow

```
Flask App (running on Cloud X)
    │
    ├── Every 30 seconds: check /health on all 3 cloud endpoints
    │   └── INSERT INTO health_checks (cloud_provider=X, target_cloud=Y, status=...)
    │
    ├── On page load: SELECT * FROM health_checks ORDER BY timestamp DESC LIMIT 50
    │
    └── On startup: INSERT INTO deployment_info (cloud_provider, region, instance_id)
```

---

## 8. Application Architecture

### Flask Application Structure

```
app/
├── app.py                    # Flask application factory
├── config.py                 # Environment variable configuration
├── models.py                 # SQLAlchemy models
├── routes/
│   ├── __init__.py
│   ├── health.py             # /health endpoint
│   ├── metrics.py            # /metrics endpoint
│   ├── dashboard.py          # / main page
│   └── api.py                # /api/* endpoints
├── services/
│   ├── __init__.py
│   └── health_checker.py     # Background health check logic
├── templates/
│   ├── base.html             # Base template
│   └── dashboard.html        # Main dashboard
├── static/
│   ├── style.css
│   └── app.js                # Minimal JS for auto-refresh
├── migrations/               # Alembic migrations
├── requirements.txt          # Pinned dependencies
├── Dockerfile                # Multi-stage build
├── gunicorn.conf.py          # Gunicorn configuration
└── tests/
    ├── test_health.py
    └── test_models.py
```

### Key Dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| Flask-SQLAlchemy | Database ORM |
| Flask-Migrate | Alembic migrations |
| psycopg2-binary | PostgreSQL driver |
| gunicorn | WSGI server |
| prometheus-flask-instrumentator | Automatic Prometheus metrics |
| requests | HTTP client (health checks to other clouds) |
| python-dotenv | Environment variable loading |
| APScheduler | Background health check scheduling |

---

## 9. Monitoring Architecture

### Per-Cloud Monitoring Stack

```
┌─────────────────────────────────────────────────────┐
│  Same pattern on each cloud:                         │
│                                                     │
│  Flask App ──(/metrics)──▶ Prometheus ──▶ Grafana   │
│                                                     │
│  Prometheus scrape config:                          │
│  - job: 'flask-app'                                 │
│    target: 'app:5000'                               │
│    path: '/metrics'                                 │
│    interval: 15s                                    │
└─────────────────────────────────────────────────────┘
```

### Grafana Dashboard Panels

| Panel | Type | Metric/Query |
|-------|------|-------------|
| Application Status | Stat | `up{job="flask-app"}` |
| Request Rate | Graph | `rate(http_requests_total[5m])` |
| Response Latency | Graph | `histogram_quantile(0.95, http_request_duration_seconds_bucket)` |
| Health Check Status | Table | `health_check_status` (custom gauge) |
| Database Connected | Stat | `db_connected` (custom gauge) |
| Uptime | Stat | `process_start_time_seconds` |
| Active Cloud | Stat | Custom label from /metrics |

---

## 10. CI/CD Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  GitHub Actions Workflow                                      │
│                                                              │
│  Trigger: Push to main / Pull Request                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │
│  │  Stage 1   │  │  Stage 2   │  │  Stage 3               │ │
│  │  Validate  │─▶│  Build     │─▶│  Terraform Plan        │ │
│  │            │  │            │  │  (per environment)     │ │
│  │ - Lint     │  │ - Docker   │  │                        │ │
│  │ - Test     │  │   build    │  │ - terraform fmt check  │ │
│  │ - Security │  │ - Push to  │  │ - terraform validate   │ │
│  │   scan     │  │   registry │  │ - terraform plan (AWS) │ │
│  └────────────┘  └────────────┘  │ - terraform plan (Azure)│ │
│                                  │ - terraform plan (GCP) │ │
│                                  └───────────┬────────────┘ │
│                                              │              │
│                                  ┌───────────▼────────────┐ │
│                                  │  Stage 4 (MANUAL)      │ │
│                                  │  Deploy                 │ │
│                                  │  - Requires approval    │ │
│                                  │  - terraform apply      │ │
│                                  └────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 11. Security Architecture

### Network Security

| Layer | Control | Implementation |
|-------|---------|---------------|
| Internet → LB | HTTPS (or HTTP for demo) | LB listener on port 80/443 |
| LB → App | Internal only | Security group: app port from LB only |
| App → DB | Internal only | DB port (5432) accessible only from app container |
| DB → Internet | Blocked | No public IP on DB; no inbound from internet |
| Admin access | Restricted | SSH/monitoring only from admin IP |

### Credential Management

| Cloud | Credential Type | Storage | Access Method |
|-------|----------------|---------|---------------|
| AWS | IAM Instance Profile | None (role-based) | Auto-assumed by EC2 |
| Azure | Service Principal | GitHub Secrets (CI) / VM env | Environment variables |
| GCP | Service Account | GitHub Secrets (CI) / VM env | Key file or metadata |
| Database | Password | Environment variable | Docker Compose env |

### Principle: No Static Credentials in Code

```
Source Code → .gitignore covers all secrets
             → terraform.tfvars never committed
             → .env files never committed
             → CI secrets in GitHub encrypted secrets
```


---

## 12. Deployment Flow

### Local Development

```bash
# Clone repo
git clone https://github.com/team/multi-cloud-health-monitor.git
cd multi-cloud-health-monitor/05-engineering

# Start locally
docker-compose up -d

# Access
# App:        http://localhost:80
# Grafana:    http://localhost:3000
# Prometheus: http://localhost:9090
```

### Cloud Deployment (Per Cloud)

```bash
# AWS Deployment
cd terraform/environments/aws
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
# Output: ALB DNS name, EC2 IP, etc.

# Azure Deployment
cd terraform/environments/azure
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
# Output: LB IP, VM IP, etc.

# GCP Deployment
cd terraform/environments/gcp
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
# Output: LB IP, VM IP, etc.

# DNS Failover (after all clouds deployed)
cd terraform/global/dns
terraform init
terraform plan -var="aws_endpoint=<alb_dns>" -var="azure_endpoint=<azure_ip>" -var="gcp_endpoint=<gcp_ip>"
terraform apply
```

### Teardown (Per Cloud)

```bash
# Reverse order: DNS first, then individual clouds
cd terraform/global/dns && terraform destroy
cd terraform/environments/gcp && terraform destroy
cd terraform/environments/azure && terraform destroy
cd terraform/environments/aws && terraform destroy
```

---

## 13. Technology Decisions Summary

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Application Framework | Flask | FastAPI, Django | Simplest for server-rendered HTML; team familiarity |
| Frontend | Jinja2 + vanilla JS | React, Vue | Team lacks frontend dev experience; eliminates risk |
| Database | PostgreSQL (container) | SQLite, DynamoDB | Portable, familiar, supports DR backup/restore |
| Reverse Proxy | Nginx | Traefik, Caddy | Industry standard; simple config |
| WSGI Server | Gunicorn | uWSGI, Waitress | Most common Flask deployment pattern |
| Container Orchestration | Docker Compose | Kubernetes, ECS | Simple; team can manage; portable |
| Monitoring | Prometheus + Grafana | CloudWatch, DataDog | Open-source; cloud-agnostic; project requirement |
| DNS Failover | Route53 | CloudFlare, Azure DNS | Integrated with AWS; health check + failover built-in |
| CI/CD | GitHub Actions | GitLab CI, Jenkins | Integrated with GitHub; free tier; team decision |
| IaC | Terraform | Pulumi, CloudFormation | Project requirement; multi-cloud native |
| Container Registry | Docker Hub | ECR, ACR, GCR | Simplest; accessible from all clouds; free tier |

---

## 14. Architecture Decision Records (Summary)

Full ADRs will be documented in `04-architecture/adr/`. Key decisions requiring ADRs:

| ADR # | Title | Status |
|-------|-------|--------|
| ADR-001 | Use Flask over FastAPI for application framework | Accepted |
| ADR-002 | Single VM with Docker Compose per cloud (vs. managed containers) | Accepted |
| ADR-003 | Route53 for DNS failover (vs. CloudFlare) | Accepted |
| ADR-004 | Backup/Restore DR strategy (vs. real-time replication) | Accepted |
| ADR-005 | Distributed monitoring (per-cloud) vs. centralized | Accepted |
| ADR-006 | Docker Hub for container registry (public) | Accepted |
| ADR-007 | Separate Terraform state per environment | Accepted |

---

## 15. Constraints and Trade-offs

| Trade-off | Chosen | Sacrificed | Reason |
|-----------|--------|-----------|--------|
| Single VM vs. managed containers | Single VM + Docker Compose | Auto-scaling, HA within cloud | Cost ($0 for free-tier VM vs. ECS/AKS charges) |
| Single AZ vs. Multi-AZ | Single AZ | Intra-cloud HA | Cost + complexity; DR across clouds compensates |
| HTTP vs. HTTPS | HTTP for demo | Encryption in transit | Certificate management adds complexity; academic context |
| Backup/Restore vs. Replication | Backup/Restore | Zero RPO | Complexity; budget; replication requires managed DB |
| Route53 (paid) vs. manual failover | Route53 | $2/month saved | Demonstrates automated failover (capstone requirement) |

---

## 16. Validation Strategy

| What to Validate | How | When |
|-----------------|-----|------|
| App accessible on each cloud | `curl http://<lb-endpoint>/health` | After each Terraform apply |
| LB routing works | Stop app → LB returns 503 | Sprint 2/3 |
| DNS failover works | Stop AWS app → check DNS resolution | Sprint 4 |
| DB backup works | pg_dump + verify file integrity | Sprint 4 |
| DB restore works | pg_restore on Azure + verify data | Sprint 4 |
| DR end-to-end | Full procedure timed | Sprint 4, 6 |
| Monitoring works | Check Grafana dashboard has data | Sprint 2 onwards |
| CI pipeline works | Push code → pipeline runs | Sprint 2 onwards |
| Teardown complete | `terraform destroy` → verify $0 resources | Every sprint |

---

## Document Approval

| Role | Status | Date |
|------|--------|------|
| Project Team | Pending Review | 2026-06-17 |
| Framework Compliance | Aligned | 2026-06-17 |

---

*Produced under AI Assisted Engineering Framework v1.0*
