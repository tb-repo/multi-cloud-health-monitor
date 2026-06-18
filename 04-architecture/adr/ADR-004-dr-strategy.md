# ADR-004: Backup/Restore Disaster Recovery Strategy

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

The capstone requires disaster recovery with data replication across clouds. We must choose between real-time replication and backup/restore for cross-cloud data protection.

## Decision

Use **backup/restore** (pg_dump to S3, pg_restore on target cloud) as the DR strategy.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Backup/Restore (pg_dump/pg_restore)** | Simple, proven, cross-cloud compatible, no managed services needed | Non-zero RPO (data since last backup may be lost) |
| PostgreSQL Streaming Replication | Near-zero RPO | Requires network connectivity between clouds; complex setup; latency |
| Managed DB replication (RDS → Azure) | Managed, reliable | Cross-cloud not natively supported; expensive |
| Application-level replication | Write to multiple DBs | Massive application complexity; consistency issues |

## Consequences

**Positive:**
- pg_dump/pg_restore works identically regardless of source/target cloud
- No ongoing cross-cloud network connectivity required
- Simple scripting (team's strength)
- Backup stored in S3 (durable, inexpensive)
- Demonstrates DR principles without enterprise complexity
- RTO < 15 minutes achievable

**Negative:**
- RPO = time since last backup (could be minutes to hours)
- Manual trigger required (no automatic replication)
- Backup must be copied to target cloud before restore

**Acceptable because:**
- Academic demonstration, not production SLA
- Health check history data is not business-critical
- The demonstration proves the concept regardless of RPO precision
- Evaluator cares that DR works, not that RPO is zero

---

*AI Assisted Engineering Framework v1.0*
