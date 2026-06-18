# ADR-003: Route53 for DNS-Based Failover

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

The capstone requires load balancing and failover mechanisms across cloud providers. We need a DNS solution that routes traffic to healthy endpoints and automatically fails over when a cloud goes down.

## Decision

Use **AWS Route53** with health checks and failover routing policy.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Route53 (failover routing)** | Native health checks, failover routing built-in, ~$2/month | AWS-specific; small cost |
| CloudFlare (free tier) | Free; fast DNS; proxy features | User's domain not suitable; less native failover control |
| Azure Traffic Manager | Multi-endpoint routing | Azure-specific; adds Azure dependency to DNS |
| GCP Cloud DNS | Managed DNS | No built-in health-check failover |
| Manual DNS (no failover) | Free; simple | Does not satisfy capstone failover requirement |

## Consequences

**Positive:**
- Health checks monitor each cloud's /health endpoint every 10 seconds
- Automatic failover: if AWS fails, Route53 returns Azure IP
- TTL of 60 seconds means failover visible within ~90 seconds
- Well-documented; Terraform provider support is mature
- Demonstrates automated failover (capstone requirement)

**Negative:**
- Cost: ~$2/month (3 health checks + hosted zone) — acceptable
- AWS-specific service for a "cloud-agnostic" project — documented trade-off
- Requires a domain name (can use Route53-registered or external)

**Note:** Using Route53 for DNS is pragmatic. The application itself is cloud-agnostic; the DNS layer is an operational choice. This is documented as an explicit trade-off.

---

*AI Assisted Engineering Framework v1.0*
