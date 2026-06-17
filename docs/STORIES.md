# STORIES.md – paychain‑core  

**Project:** paychain‑core – Decentralized, blockchain‑based payment processing platform  
**Target Release:** MVP (v0.1) → Full Release (v1.0)  

---  

## Table of Contents
1. [Epics Overview](#epics-overview)  
2. [User Story Backlog](#user-story-backlog)  
   - [Epic 1 – Network & Ledger Foundations](#epic-1---network--ledger-foundations)  
   - [Epic 2 – Core Payment Flows](#epic-2---core-payment-flows)  
   - [Epic 3 – Security & Compliance](#epic-3---security--compliance)  
   - [Epic 4 – Monitoring & Operations](#epic-4---monitoring--operations)  

---  

## Epics Overview  

| Epic | Description | MVP Priority |
|------|-------------|--------------|
| **Epic 1 – Network & Ledger Foundations** | Set up the permissioned blockchain network, consensus, and immutable ledger primitives required for any payment transaction. | High |
| **Epic 2 – Core Payment Flows** | Implement end‑to‑end payment creation, routing, settlement, and reconciliation across participating entities. | High |
| **Epic 3 – Security & Compliance** | Provide authentication, authorization, audit‑trail, AML/KYC hooks, and data‑privacy guarantees. | Medium |
| **Epic 4 – Monitoring & Operations** | Deliver observability, health‑checks, admin tooling, and upgrade mechanisms for production operation. | Medium |

Stories are ordered within each epic to reflect the logical build order for the MVP, followed by stretch goals for the full release.

---  

## User Story Backlog  

### Epic 1 – Network & Ledger Foundations  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 1.1 | **As a **Network Engineer**, I want a permissioned blockchain network that only approved nodes can join, so that the system remains private and controlled.** | - Nodes can be added/removed via signed admin transaction.<br>- New node joins after verifying its X.509 certificate against the network’s root CA.<br>- Network rejects any connection from an unknown public key.<br>- Documentation of node‑join workflow is in `docs/network‑onboarding.md`. |
| 1.2 | **As a **Consensus Operator**, I want a Byzantine Fault‑Tolerant (BFT) consensus algorithm (e.g., Tendermint) configured with a 2/3 quorum, so that the ledger finalizes transactions quickly and safely.** | - Consensus reaches finality within ≤ 2 seconds under normal load (≤ 500 TPS).<br>- System tolerates up to 1/3 faulty/partitioned nodes without loss of liveness.<br>- Unit tests cover quorum calculation and view‑change scenarios. |
| 1.3 | **As a **Data Engineer**, I want an immutable ledger schema that records every payment event with cryptographic hash linking, so that auditability is guaranteed.** | - Ledger entries contain: `payment_id`, `timestamp`, `sender`, `receiver`, `amount`, `currency`, `prev_hash`, `curr_hash`.<br>- `curr_hash = SHA‑256(prev_hash || serialized_event)` verified on write.<br>- Tamper‑detection script flags any broken hash chain. |
| 1.4 | **As a **DevOps Engineer**, I want automated network bootstrap scripts (Docker‑Compose + Helm) so that a full testnet can be spun up in ≤ 5 minutes.** | - `scripts/bootstrap-testnet.sh` creates 4 validator nodes and 2 observer nodes.<br>- All services start without manual config edits.<br>- Testnet can be destroyed and recreated cleanly. |
| 1.5 | **As a **Product Owner**, I want a versioned API gateway that abstracts the underlying ledger, so that downstream services can evolve without breaking contracts.** | - OpenAPI 3.0 spec published at `api/v1/openapi.yaml`.<br>- Backward‑compatible version bump (`v1 → v2`) does not break existing clients.<br>- Integration test suite validates contract compliance. |

### Epic 2 – Core Payment Flows  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 2.1 | **As a **Bank Operator**, I want to create a payment instruction (P‑IN) that includes sender, receiver, amount, and currency, so that the transaction can be processed on‑chain.** | - POST `/api/v1/payments` accepts JSON payload with required fields.<br>- Returns `payment_id` and `status: pending`.<br>- Payload validation rejects missing or malformed fields with HTTP 400. |
| 2.2 | **As a **Payment Processor**, I want the system to automatically route the payment to the optimal validator set based on geographic latency, so that settlement is fast.** | - Routing service queries node latency matrix and selects the nearest 2 validators.<br>- End‑to‑end latency from API call to ledger commit ≤ 3 seconds in testnet.<br>- Logs contain chosen validator IDs. |
| 2.3 | **As a **Corporate Treasury**, I want real‑time settlement confirmation (finality receipt) once the payment is committed, so that I can reconcile instantly.** | - Upon consensus, system emits a `PaymentFinalized` event on a WebSocket channel.<br>- Event payload includes `payment_id`, `block_number`, `final_hash`.<br>- Client receives receipt within 2 seconds of commit. |
| 2.4 | **As an **Accountant**, I want a bulk reconciliation endpoint that returns all settled payments for a given date range, so that I can generate daily reports.** | - GET `/api/v1/payments?from=YYYY‑MM‑DD&to=YYYY‑MM‑DD&status=settled` returns paginated list.<br>- Each record includes `payment_id`, `timestamp`, `amount`, `currency`, `status`.<br>- Response time ≤ 1 second for ≤ 10 k records. |
| 2.5 | **As a **Developer**, I want SDKs (Python & Go) that wrap the API calls, so that integration is frictionless.** | - `paychain-sdk-py` and `paychain-sdk-go` published to PyPI and GitHub Packages.<br>- SDK includes `create_payment`, `get_status`, `subscribe_finalized` helpers.<br>- Unit tests achieve ≥ 90 % coverage. |
| 2.6 | **As a **Compliance Analyst**, I want the ability to flag a payment for manual review before settlement, so that suspicious transactions can be blocked.** | - POST `/api/v1/payments/{id}/hold` sets `status: on_hold`.<br>- System prevents further routing until `release` or `reject` is called.<br>- Audit log records user, timestamp, and reason. |

### Epic 3 – Security & Compliance  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 3.1 | **As a **Security Engineer**, I want all API traffic to be mutually TLS‑authenticated, so that only trusted clients can interact with the platform.** | - Server presents certificate signed by internal CA.<br>- Clients must present valid client cert.<br>- Unauthorized TLS handshake results in HTTP 403. |
| 3.2 | **As a **Regulatory Officer**, I need AML/KYC hooks that invoke an external risk‑scoring service before a payment is routed, so that we stay compliant.** | - Payment creation triggers async call to `risk‑engine` endpoint.<br>- If risk score > threshold, payment status becomes `on_hold` and a `risk_flag` is attached.<br>- Integration test simulates high‑risk response and verifies hold behavior. |
| 3.3 | **As a **Data Privacy Lead**, I want personal identifiers (e.g., SSN, bank account numbers) to be encrypted at rest using a rotating KEK, so that data breaches are mitigated.** | - Sensitive fields stored encrypted with AES‑256‑GCM.<br>- KEK rotation script rotates keys without downtime.<br>- Decryption only possible with active KEK and proper IAM role. |
| 3.4 | **As an **Auditor**, I want immutable audit logs for every admin action (node join, config change, key rotation), so that investigations are possible.** | - Logs written to append‑only storage (e.g., Amazon S3 Object Lock or IPFS).<br>- Each log entry includes `action`, `actor`, `timestamp`, `hash` of previous entry.<br>- Tamper‑evidence verified via Merkle proof script. |

### Epic 4 – Monitoring & Operations  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 4.1 | **As an **Site Reliability Engineer**, I want Prometheus metrics exposed for node health, transaction throughput, and latency, so that we can set alerts.** | - `/metrics` endpoint provides `paychain_tx_total`, `paychain_tx_latency_seconds`, `node_peer_count`.<br>- Grafana dashboards pre‑bundled in `ops/grafana/`. |
| 4.2 | **As a **Support Engineer**, I want a web‑based admin console to view pending payments, node status, and audit logs, so that I can troubleshoot quickly.** | - React SPA at `/admin` protected by OAuth2 + MFA.<br>- Views: “Pending Payments”, “Node Map”, “Audit Trail”.<br>- Actions (e.g., release hold) are logged. |
| 4.3 | **As a **Release Manager**, I want a rolling upgrade mechanism that updates validator software without halting consensus, so that we can deploy patches safely.** | - Upgrade script performs canary rollout to 1 validator, validates block production, then proceeds to remaining nodes.<br>- No more than 1 block height gap during upgrade.<br>- Automated rollback if health checks fail. |
| 4.4 | **As a **Product Analyst**, I want daily usage reports (TPS, failed payments, average latency) emailed to stakeholders, so that business impact can be tracked.** | - Cron job generates CSV + PDF summary at 00:00 UTC.<br>- Sent to `reports@axentx.com` via SMTP.<br>- Report includes trend graphs. |

---  

## Prioritization for MVP (v0.1)

1. **Epic 1 – Network & Ledger Foundations** (Stories 1.1‑1.5)  
2. **Epic 2 – Core Payment Flows** (Stories 2.1‑2.4)  
3. **Epic 3 – Security & Compliance** (Stories 3.1‑3.2)  

*Stories 2.5‑2.6, 3.3‑3.4, and all Epic 4 items are slated for the Full Release (v1.0) but are included in the backlog for early design.*  

---  

*End of STORIES.md*
