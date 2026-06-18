# ADR-007: Separate Terraform State per Environment

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

With Terraform managing resources across 3 clouds + a global DNS layer, we need a state management strategy that supports team collaboration and prevents cross-environment interference.

## Decision

Use **separate Terraform state per environment** (aws, azure, gcp, global) with remote backend on S3.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Separate state per environment (remote)** | Isolated; safe; team can work in parallel; no cross-environment blast radius | More backend config; global layer needs outputs from other states |
| Single shared state | Simple; one apply does everything | Extremely risky; one error affects all clouds; slow plan |
| Local state files | No backend setup | No team collaboration; state loss risk; no locking |
| Terraform Cloud | Managed; UI; collaboration | Adds dependency; free tier limited; overkill for this |

## Consequences

**Positive:**
- `terraform destroy` in one environment doesn't affect others
- Team members can work on different clouds in parallel
- State locking (DynamoDB) prevents corruption
- Clear ownership: aws/main.tf owns AWS resources only
- Global DNS layer reads outputs from other states via `terraform_remote_state` data source

**Negative:**
- Need to pass information between states (outputs → remote_state data source)
- Initial backend setup required (S3 bucket + DynamoDB table)
- Global layer depends on other environments being applied first

**State Architecture:**
```
s3://project-terraform-state/
├── aws/terraform.tfstate
├── azure/terraform.tfstate
├── gcp/terraform.tfstate
└── global/terraform.tfstate
```

---

*AI Assisted Engineering Framework v1.0*
