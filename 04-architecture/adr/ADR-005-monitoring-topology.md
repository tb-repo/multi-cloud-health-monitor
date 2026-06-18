# ADR-005: Distributed Monitoring (Per-Cloud)

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

We need Prometheus and Grafana for monitoring. The question is whether to run a single centralized monitoring stack or distribute monitoring per cloud.

## Decision

Deploy **Prometheus + Grafana on each cloud independently**, alongside the application.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Distributed (per-cloud)** | Fault-isolated; each cloud self-observable; survives single-cloud failure | 3 Grafana instances to manage; no unified view |
| Centralized (single cloud) | Unified dashboard; single config | If monitoring cloud fails, lose all visibility; cross-cloud scraping adds latency |
| Managed service (CloudWatch, Azure Monitor, Cloud Monitoring) | No infrastructure to manage | Different per cloud; not unified; vendor lock-in |
| Grafana Cloud (SaaS) | Unified; managed | Cost; external dependency; data egress |

## Consequences

**Positive:**
- Each cloud is independently observable — if AWS goes down, Azure monitoring still works
- Same Docker Compose pattern everywhere (Prometheus + Grafana are just containers)
- Demonstrates distributed operations thinking (resilience principle)
- Each cloud's Grafana shows its own metrics — good for demo ("here's the AWS view, here's the Azure view")

**Negative:**
- No single unified dashboard across all 3 clouds (acceptable — the app dashboard shows cross-cloud status)
- Grafana configuration must be maintained per deployment (mitigated by dashboard-as-code)
- Slightly more deployment effort (mitigated by identical Docker Compose)

**Rationale:** The principle that "one cloud's failure should not impact another" extends to monitoring. Self-contained stacks per cloud demonstrate proper fault isolation.

---

*AI Assisted Engineering Framework v1.0*
