# REQUIREMENTS.md

## Document Overview
This document defines the functional and non‑functional requirements for **paychain‑core**, the decentralized, blockchain‑based payment processing engine for banks, payment providers, corporations, and digital‑asset ecosystems. It serves as the definitive source of truth for designers, developers, QA, and reviewers throughout the product lifecycle.

---

## 1. Scope
- Build a permissioned, high‑throughput blockchain network that settles fiat‑linked and crypto‑linked payments in near‑real‑time.
- Expose a clean, versioned API (REST + gRPC) for integration with external banking systems, PSPs, and corporate ERP/Treasury platforms.
- Provide on‑chain transparency, auditability, and tamper‑evidence while preserving privacy where required (confidential transactions).
- Enable plug‑in support for multiple settlement assets (USD, EUR, stablecoins, tokenized assets).

---

## 2. Definitions
| Term | Meaning |
|------|---------|
| **Node** | A validator or full participant in the paychain network. |
| **Transaction** | A payment instruction recorded on‑chain, optionally containing metadata. |
| **Settlement Asset** | The currency/token used to settle the transaction (e.g., USD‑t, EUR‑t, USDC). |
| **Confidential Transaction** | A transaction where amounts are hidden using range proofs / bulletproofs. |
| **API Gateway** | The front‑end service exposing REST/gRPC endpoints to external clients. |
| **Smart‑Contract Module** | On‑chain logic for fee calculation, compliance checks, and settlement routing. |

---

## 3. Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| **FR‑1** | **Network Bootstrap** | The system shall allow a consortium of up to 50 pre‑approved entities to bootstrap a permissioned network using a genesis configuration file. |
| **FR‑2** | **Transaction Submission** | Clients shall submit payment transactions via REST (`POST /v1/tx`) or gRPC (`SubmitTx`). The request must include: payer ID, payee ID, amount, settlement asset, optional metadata, and a digital signature. |
| **FR‑3** | **Deterministic Ordering** | The consensus layer shall order transactions deterministically using a BFT algorithm (e.g., Tendermint/HotStuff) guaranteeing finality within **≤ 3 seconds** for ≤ 10 k TPS load. |
| **FR‑4** | **Fee Engine** | A configurable fee module shall compute fees per transaction based on: asset type, transaction size, and optional tiered discounts. Fees are deducted automatically before settlement. |
| **FR‑5** | **Compliance Hook** | Before inclusion in a block, each transaction shall be passed to a pluggable compliance service (KYC/AML). The service can **reject** or **flag** a transaction; flagged transactions are still recorded but marked for audit. |
| **FR‑6** | **Multi‑Asset Settlement** | The core shall support at least three settlement assets out‑of‑the‑box (USD‑t, EUR‑t, USDC). Adding a new asset shall require only a configuration file and a smart‑contract module, no code change. |
| **FR‑7** | **Confidential Transactions** | When a client sets `confidential=true`, the system shall encrypt the amount using Pedersen commitments and generate a bulletproof range proof. The encrypted amount is stored on‑chain; only parties possessing the shared secret can reveal it. |
| **FR‑8** | **Query API** | Provide endpoints to retrieve transaction status (`GET /v1/tx/{hash}`), account balance (`GET /v1/account/{id}`), and audit trails (`GET /v1/audit?from=&to=`). |
| **FR‑9** | **Node Management** | Operators shall be able to add/remove validator nodes via the admin CLI (`paychain-node admin add-validator --id …`). The system shall automatically rebalance the validator set. |
| **FR‑10** | **Data Export** | The system shall emit immutable transaction logs to an external Kafka topic (`paychain.events`) for downstream analytics and reconciliation. |
| **FR‑11** | **Rollback Protection** | Once a block reaches finality, the system shall reject any attempt to revert or rewrite that block. |
| **FR‑12** | **Health & Metrics** | Expose Prometheus metrics (`/metrics`) and a health endpoint (`/healthz`) for each service component. |
| **FR‑13** | **Versioned API** | All external APIs shall be versioned (`/v1/…`). Deprecation policy: ≥ 12 months notice before removal. |
| **FR‑14** | **SDKs** | Provide official client SDKs (Python, Go, JavaScript) that wrap the API, handle signing, and support both synchronous and asynchronous usage. |
| **FR‑15** | **Testing Harness** | Include an integration test harness that can spin up a 4‑node testnet, submit 1 M synthetic transactions, and verify deterministic finality and balance invariants. |

---

## 4. Non‑Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | The network shall sustain **≥ 10 k TPS** sustained throughput with **≤ 3 s** finality under normal load (≤ 80 % CPU per validator). |
| **NFR‑2** | **Scalability** | Horizontal scaling shall be supported by adding validator nodes; the consensus algorithm must maintain finality latency ≤ 3 s up to 50 validators. |
| **NFR‑3** | **Security – Cryptography** | All signatures must use **ECDSA‑secp256k1** or **Ed25519**. Confidential transaction proofs shall use **Bulletproofs** (≤ 200 µs verification). |
| **NFR‑4** | **Security – Network** | Mutual TLS (mTLS) is required for all node‑to‑node communication. API gateway must enforce OAuth 2.0 Bearer tokens with scopes (`paychain:submit`, `paychain:query`). |
| **NFR‑5** | **Reliability** | System availability ≥ 99.9 % monthly, measured as uptime of the API gateway and at least 4 validator nodes. |
| **NFR‑6** | **Durability** | All on‑chain data must be persisted on SSDs with RAID‑10 redundancy; snapshots shall be taken every 12 h and retained for 30 days. |
| **NFR‑7** | **Observability** | Emit structured logs (JSON) with correlation IDs; integrate with centralized logging (ELK) and tracing (OpenTelemetry). |
| **NFR‑8** | **Compliance** | Support GDPR “right to be forgotten” by allowing logical deletion of off‑chain metadata while preserving on‑chain immutability. |
| **NFR‑9** | **Maintainability** | Codebase shall follow the **Axentx C++/Rust style guide**, include ≥ 80 % unit test coverage, and enforce static analysis (clang‑tidy, cargo‑clippy). |
| **NFR‑10** | **Portability** | Deployable on Linux (Ubuntu 22.04+), containerized via Docker, orchestrated with Kubernetes (v1.27+). |
| **NFR‑11** | **Extensibility** | Smart‑contract modules shall be written in **Move** or **Solidity‑compatible** language and loaded at runtime via a module registry. |
| **NFR‑12** | **Documentation** | All public APIs must have OpenAPI 3.0 specs; SDKs must include autogenerated docs (Sphinx/Typedoc) and example snippets. |
| **NFR‑13** | **Legal** | All third‑party libraries must be compatible with Apache‑2.0 or MIT licenses; a SPDX license file must be present. |
| **NFR‑14** | **Resource Limits** | Each validator node shall be limited to ≤ 8 CPU cores and 32 GB RAM in production. |

---

## 5. Constraints

1. **Technology Stack** – Core consensus and node software must be implemented in **Rust** (for safety & performance). API gateway can be in **Go** or **Rust**.
2. **Data Residency** – Nodes located in the EU must store all EU‑origin transaction data within EU‑based data centers.
3. **Regulatory** – Must support AML‑CFT reporting hooks (e.g., SAR generation) as per FATF guidance.
4. **Interoperability** – Must provide a bridge module to connect with existing **ISO 20022** payment rails (via a message adapter).
5. **Version Compatibility** – New releases must remain backward compatible with the previous two major versions of the API.

---

## 6. Assumptions

| ID | Assumption |
|----|------------|
| **A‑1** | Consortium members will provision validator hardware meeting the resource limits defined in NFR‑14. |
| **A‑2** | All participating entities possess a PKI infrastructure for issuing X.509 certificates used in mTLS. |
| **A‑3** | Settlement assets are tokenized on an existing public L1 (e.g., Ethereum) or a private side‑chain that the consortium controls. |
| **A‑4** | External compliance services expose a gRPC interface with `ValidateTransaction(tx) -> (allow, flags)`. |
| **A‑5** | Network latency between validator nodes will not exceed 150 ms (typical for geo‑distributed data centers). |
| **A‑6** | The underlying storage layer (RocksDB) can handle the write amplification of the expected TPS without degrading latency. |
| **A‑7** | End‑users will manage their own private keys; the SDKs provide helper functions for secure key storage (e.g., hardware wallets, HSM). |

---

## 7. Acceptance Criteria

- **AC‑1**: Deploy a 4‑node testnet, submit 500 k mixed (confidential & non‑confidential) transactions, verify that finality ≤ 3 s and balances reconcile.
- **AC‑2**: API gateway returns correct HTTP status codes (200, 400, 401, 403, 429) for all defined scenarios.
- **AC‑3**: Security scan (OWASP ZAP, cargo‑audit) reports no critical vulnerabilities.
- **AC‑4**: Documentation passes automated linting and includes at least one end‑to‑end example for each SDK language.
- **AC‑5**: Monitoring dashboards display ≥ 99.9 % uptime over a 7‑day rolling window in a staging environment.

---

*Prepared by: Senior Product/Engineering Lead – paychain‑core*  
*Date: 2026‑06‑17*
