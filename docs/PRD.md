# PayChain Core – Product Requirements Document (PRD)

**Document Version:** 1.0  
**Last Updated:** 2026‑06‑17  
**Author:** Senior Product/Engineering Lead, AxentX  

---

## 1. Overview

**PayChain Core** is a decentralized, blockchain‑based payment processing engine designed to replace legacy, siloed payment rails with a high‑throughput, low‑cost, and fully auditable network. It targets banks, payment service providers (PSPs), large enterprises, and digital‑asset platforms that need to settle high‑volume transactions (both fiat and tokenized assets) across borders with real‑time visibility.

The product will be delivered as a **self‑hosted, open‑source runtime** (Docker‑compose / Helm chart) plus a **managed SaaS gateway** for rapid onboarding. Core components include:

| Component | Description |
|-----------|-------------|
| **Consensus Layer** | Permissioned BFT consensus (HotStuff) tuned for sub‑second finality on up to 10 k TPS. |
| **Smart‑Contract Runtime** | WASM‑based execution sandbox for custom settlement logic, fee models, and compliance hooks. |
| **Payment API** | gRPC + REST endpoints (JSON‑RPC) for transaction creation, status queries, and batch settlement. |
| **Node SDKs** | First‑class libraries for Go, Rust, Python, and JavaScript. |
| **Observability Suite** | Prometheus metrics, OpenTelemetry traces, and a Grafana dashboard for latency, throughput, and node health. |
| **Compliance Module** (optional) | KYC/AML plug‑in points, transaction tagging, and audit‑log export. |

---

## 2. Problem Statement

| Pain Point | Affected Stakeholder | Impact |
|------------|----------------------|--------|
| **High processing fees** – legacy rails (SWIFT, ACH) charge 0.5‑3 % per transaction. | Banks, PSPs, Enterprises | Reduces margins, discourages micro‑transactions. |
| **Slow settlement times** – 1‑3 days for cross‑border fiat. | Corporations, Digital‑asset platforms | Cash‑flow friction, increased working‑capital costs. |
| **Opaque audit trails** – limited visibility into intermediate steps. | Regulators, Auditors, Enterprises | Compliance risk, manual reconciliation effort. |
| **Vendor lock‑in** – proprietary APIs prevent integration agility. | All payment participants | High switching costs, stifles innovation. |
| **Scalability limits** – existing blockchains (e.g., Ethereum) cannot sustain >2 k TPS for payment workloads. | High‑volume merchants, exchanges | Transaction bottlenecks, lost revenue. |

**Result:** A market‑validated need for a **decentralized, high‑throughput, low‑cost payment network** that offers transparent, programmable settlement while remaining compliant with financial regulations.

---

## 3. Target Users & Personas

| Persona | Primary Goals | Success Criteria |
|---------|---------------|------------------|
| **Bank Payments Ops Lead** | Reduce inter‑bank settlement cost & latency. | ≥ 30 % fee reduction, sub‑second finality for domestic, ≤ 5 s for cross‑border. |
| **Payment Service Provider Engineer** | Integrate a single API for multiple payment methods. | One‑click SDK integration, < 200 ms API latency. |
| **Enterprise Treasury Manager** | Real‑time cash visibility and programmable escrow. | Dashboard shows end‑to‑end latency, automated compliance tagging. |
| **Digital‑Asset Exchange CTO** | On‑chain settlement of fiat‑backed stablecoins. | Support for tokenized fiat, < 2 s finality, 10 k TPS. |
| **Regulatory Compliance Officer** | Ensure auditability and AML/KYC enforcement. | Immutable audit logs, plug‑in compliance hooks, exportable reports. |

---

## 4. Goals & Success Metrics

| Goal | Metric | Target (12 mo) |
|------|--------|----------------|
| **Cost Reduction** | Avg. transaction fee (basis points) | ≤ 5 bps (vs. 50‑300 bps legacy) |
| **Performance** | 95th‑percentile transaction finality | ≤ 2 s (domestic), ≤ 5 s (cross‑border) |
| **Throughput** | Sustained TPS on a 5‑node cluster | ≥ 10 k TPS |
| **Adoption** | Number of production nodes (banks/PSPs) | ≥ 12 distinct institutions |
| **Compliance** | % of transactions with attached compliance metadata | ≥ 99 % |
| **Developer Experience** | Avg. time to integrate SDK (hours) | ≤ 4 h |
| **Reliability** | Monthly uptime (node + API) | ≥ 99.9 % |

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Permissioned BFT Consensus** | HotStuff‑derived consensus with deterministic finality. | • Finality ≤ 2 s for 10 k TPS.<br>• Fault tolerance up to 1/3 Byzantine nodes.<br>• Node join/leave without service interruption. |
| **P1** | **Payment API (gRPC + REST)** | Unified endpoint for transaction submission, status, batch settlement, and refunds. | • End‑to‑end latency ≤ 200 ms (local).<br>• OpenAPI spec generated and versioned. |
| **P1** | **WASM Smart‑Contract Runtime** | Allows custom settlement logic (e.g., fee splits, escrow). | • Deploy/upgrade contracts without network downtime.<br>• Execution sandbox limits ≤ 5 ms per contract call. |
| **P2** | **Node SDKs (Go, Rust, Python, JS)** | Idiomatic client libraries with auto‑retry, signing, and streaming support. | • Unit‑tested ≥ 90 % coverage.<br>• Sample apps for each language pass integration test suite. |
| **P2** | **Observability Suite** | Prometheus metrics, OpenTelemetry traces, Grafana dashboards. | • Dashboard shows latency, TPS, error rates.<br>• Alerts fire on > 1 % error rate. |
| **P2** | **Compliance Plug‑in Framework** | Hooks for KYC/AML checks, transaction tagging, audit‑log export (CSV/JSON). | • Plug‑in can reject/flag a transaction.<br>• Immutable log stored on‑chain with off‑chain export. |
| **P3** | **Managed SaaS Gateway** (optional commercial layer) | Hosted API gateway with auto‑scaling, API‑key auth, and billing. | • Onboard a new tenant in < 15 min.<br>• Billing reports generated daily. |
| **P3** | **Cross‑Chain Bridge** | Tokenized fiat bridge to Ethereum, Solana, and Polkadot. | • Bridge lock/unlock latency ≤ 5 s.<br>• Supports at least two token standards (ERC‑20, SPL). |

---

## 6. Scope

### In‑Scope (MVP – 12 months)

1. Core consensus layer with permissioned BFT.
2. Payment API (gRPC + REST) with basic transaction lifecycle.
3. WASM runtime for deterministic smart contracts.
4. Node SDKs for Go and Python (first release).
5. Observability (metrics + basic dashboards).
6. Compliance plug‑in framework (KYC/AML stub).
7. Docker‑compose deployment scripts and Helm chart.
8. Comprehensive test harness (unit, integration, performance).

### Out‑of‑Scope (Post‑MVP)

* Full managed SaaS gateway (will be a commercial add‑on).
* Advanced cross‑chain bridges (deferred to Phase 2).
* Multi‑region sharding for > 100 k TPS.
* Native mobile SDKs (iOS/Android).
* Full regulatory certification (e.g., PCI DSS) – to be pursued per‑customer.

---

## 7. Assumptions & Dependencies

| Assumption | Rationale |
|------------|-----------|
| **Permissioned network** – participants are pre‑vetted financial institutions. | Enables BFT consensus with lower latency. |
| **WASM runtime** – existing open‑source runtime (wasmtime) is compatible with our security hardening. | Reduces engineering effort. |
| **Infrastructure** – nodes will run on Kubernetes clusters (AWS EKS, GKE, Azure AKS) or on‑prem VMs. | Aligns with customer ops teams. |
| **Regulatory compliance** – customers will supply KYC/AML data via plug‑ins; PayChain does not store PII. | Limits liability and simplifies GDPR/CCPA compliance. |
| **Dataset availability** – existing AxentX instruction‑response datasets can be used to train internal fraud‑detection models (future phase). | Provides a roadmap for AI‑enhanced compliance. |

**External Dependencies**

* `wasmtime` (WASM runtime) – version ≥ 22.0.
* `hotstuff` reference implementation – forked and hardened.
* `grpc-go`, `grpc-python` libraries – latest stable releases.
* Prometheus & Grafana Helm charts.

---

## 8. Milestones & Timeline

| Milestone | Deliverable | Owner | Target Date |
|-----------|-------------|-------|-------------|
| **M1 – Architecture Freeze** | Detailed design docs, component diagram, threat model. | Architecture Lead | 2026‑07‑15 |
| **M2 – Consensus Prototype** | 5‑node BFT network with sub‑second finality (testnet). | Core Engineer | 2026‑08‑30 |
| **M3 – Payment API v1** | gRPC + REST spec, CI pipeline, basic end‑to‑end tests. | API Team | 2026‑10‑15 |
| **M4 – WASM Runtime Integration** | Deployable contracts, sandbox security tests. | Smart‑Contract Team | 2026‑11‑30 |
| **M5 – SDK Release (Go/Python)** | Published to GitHub, PyPI, Go modules, docs. | SDK Team | 2026‑12‑20 |
| **M6 – Observability & Dashboard** | Prometheus metrics, Grafana dashboards, alert rules. | Ops Team | 2027‑01‑15 |
| **M7 – Compliance Plug‑in** | KYC/AML hook interface, sample implementation. | Compliance Team | 2027‑02‑10 |
| **M8 – MVP Release Candidate** | Full stack (consensus + API + SDK + observability) packaged as Helm chart. | Release Engineering | 2027‑03‑01 |
| **M9 – Pilot Deployments** | Onboard 3 banks/PSPs for beta testing, collect feedback. | BD / PM | 2027‑04‑15 |
| **M10 – GA Launch** | Public GitHub release, documentation site, support SLA. | PM | 2027‑06‑01 |

---

## 9. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Consensus performance not meeting 10 k TPS** | Core value proposition fails. | Medium | Early performance testing, hardware benchmarking, ability to scale node count. |
| **Regulatory pushback on decentralized settlement** | Adoption barrier. | Low | Keep network permissioned, provide compliance plug‑ins, engage legal early. |
| **Smart‑contract security vulnerabilities** | Potential fund loss. | Medium | Use audited WASM runtime, formal verification of critical contracts, bounty program. |
| **SDK adoption lag** | Slower ecosystem growth. | Low | Provide extensive samples, auto‑generated client code, developer portal. |
| **Operational complexity for customers** | Deployment friction. | Medium | Offer Helm chart + Docker‑compose, detailed ops guide, optional managed gateway. |

---

## 10. Acceptance Criteria (Definition of Done)

* All **P1** features are implemented, unit‑tested (≥ 90 % coverage), and pass performance benchmarks.
* End‑to‑end integration tests demonstrate:
  * Transaction submission → finality ≤ 2 s (local) / ≤ 5 s (cross‑region).
  * Smart‑contract execution within sandbox limits.
* Documentation:
  * Architecture overview (PDF/Markdown).
  * API reference (OpenAPI + gRPC proto files).
  * SDK quick‑start guides.
  * Ops guide (deployment, monitoring, upgrade).
* Security audit completed by an external firm (no critical findings).
* Pilot customers have run a minimum of 100 k transactions on the network with < 1 % error rate.
* Release package (Helm chart, Docker images) published to AxentX artifact registry with versioning.

---

## 11. Appendices

### A. Glossary
* **BFT** – Byzantine Fault Tolerance.  
* **TPS** – Transactions Per Second.  
* **WASM** – WebAssembly.  
* **KYC** – Know Your Customer.  
* **AML** – Anti‑Money Laundering.  

### B. References
1. HotStuff paper – *“HotStuff: BFT Consensus in the Lens of Blockchain”* (2020).  
2. `wasmtime` documentation – <https://github.com/bytecodealliance/wasmtime>.  
3. AxentX Runbook (2026‑05‑23) – internal repository `arkashira/surrogate-1-harvest`.  

--- 

*Prepared for internal review and alignment across product, engineering, and business development.*
