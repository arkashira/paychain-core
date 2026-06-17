# TECH_SPEC.md – paychain‑core  

**Project:** paychain‑core  
**Owner:** AxentX – Payments & Distributed Ledger Team  
**Status:** MVP → Production‑Ready (v1.0)  
**Last Updated:** 2026‑06‑17  

---  

## 1. Overview  

paychain‑core is a **decentralized, blockchain‑based payment processing platform** that enables banks, payment service providers, corporations, and digital‑asset ecosystems to settle transactions with:

* **Sub‑second finality** (via a high‑throughput consensus layer)  
* **Deterministic fee model** (cost‑per‑transaction < 0.1 %)  
* **Full auditability** (tamper‑evident ledger + on‑chain provenance)  
* **Inter‑operability** (native support for fiat‑on‑chain bridges and ERC‑20/721 assets)  

The core repository contains the **protocol layer**, **node implementation**, **smart‑contract runtime**, and **public APIs** required to run a permissioned/permissionless network of paychain nodes.

---  

## 2. Architecture Overview  

```
+-------------------+       +-------------------+       +-------------------+
|   Client SDKs     | <---> |   API Gateway     | <---> |   Paychain Nodes  |
+-------------------+       +-------------------+       +-------------------+
                                   |   ^   |
                                   |   |   |
                                   v   |   v
                           +-----------------------+
                           |  Consensus Engine     |
                           |  (HotStuff + BFT)     |
                           +-----------------------+
                                   |
                                   v
                           +-----------------------+
                           |  Ledger Store (RocksDB)|
                           +-----------------------+
                                   |
                                   v
                           +-----------------------+
                           |  Smart‑Contract VM    |
                           |  (WebAssembly, WASM)  |
                           +-----------------------+
```

* **Client SDKs** – Go, Rust, JavaScript/TypeScript libraries for transaction construction, signing, and submission.  
* **API Gateway** – Stateless HTTP/2 & gRPC entry point (AuthN/AuthZ, rate‑limiting, request validation).  
* **Paychain Nodes** – Full‑stack runtime hosting the consensus engine, ledger, and WASM VM. Nodes can run in **validator**, **archival**, or **light** mode.  
* **Consensus Engine** – HotStuff BFT with dynamic validator set, supporting up to **10 k TPS** on commodity hardware.  
* **Ledger Store** – Append‑only Merkle‑Patricia tree persisted in RocksDB; snapshots are streamed to S3/MinIO for backup.  
* **Smart‑Contract VM** – WASM‑based sandbox with deterministic execution, gas metering, and native crypto primitives.  

---  

## 3. Core Components  

| Component | Description | Primary Language | Key Interfaces |
|-----------|-------------|------------------|----------------|
| **Node Core** | Network stack, peer discovery, message routing | Rust | `p2p::Network`, `node::NodeHandle` |
| **Consensus** | HotStuff BFT implementation, leader election, view changes | Rust | `consensus::HotStuff`, `consensus::ValidatorSet` |
| **Ledger** | Merkle‑Patricia tree, state DB, block storage | Rust | `ledger::BlockStore`, `ledger::StateDB` |
| **VM** | WASM runtime (Wasmtime), syscalls for token ops, crypto | Rust | `vm::WasmExecutor`, `vm::SyscallHandler` |
| **API Gateway** | HTTP/2 & gRPC façade, auth, metrics | Go (gin‑gonic) | `api/v1/SubmitTx`, `api/v1/GetTxStatus` |
| **SDKs** | Helper libs for transaction creation, signing, and query | Go / Rust / TS | `client.SubmitTx`, `client.QueryBalance` |
| **Bridge Module** | Fiat‑on‑chain gateway adapters (ISO‑20022, ACH) | Rust | `bridge::FiatAdapter`, `bridge::CryptoAdapter` |
| **Monitoring** | Prometheus exporter, OpenTelemetry traces | Go / Rust | `/metrics`, `otel::Tracer` |

---  

## 4. Data Model  

### 4.1 Blocks  

| Field | Type | Description |
|-------|------|-------------|
| `height` | u64 | Sequential block number |
| `prev_hash` | `[u8;32]` | SHA‑256 of previous block |
| `state_root` | `[u8;32]` | Merkle‑Patricia root after tx execution |
| `tx_root` | `[u8;32]` | Merkle root of transaction list |
| `timestamp` | u64 (ms) | Epoch time |
| `validator_sig` | `Signature` | Aggregate BFT signature |
| `txs` | `Vec<Tx>` | Ordered list of included transactions |

### 4.2 Transactions  

| Field | Type | Description |
|-------|------|-------------|
| `tx_id` | `[u8;32]` | Hash of the serialized transaction |
| `sender` | `AccountId` | 20‑byte address (derived from public key) |
| `nonce` | u64 | Sender‑specific counter |
| `payload` | `enum TxPayload` | `Transfer`, `ContractCall`, `BridgeDeposit`, … |
| `gas_limit` | u64 | Max gas units |
| `gas_price` | u64 | Fee per gas unit (in native token) |
| `signature` | `Signature` | ECDSA‑secp256k1 or Ed25519 |

### 4.3 Accounts  

| Field | Type | Description |
|-------|------|-------------|
| `balance` | u128 | Native token balance |
| `nonce` | u64 | Next expected nonce |
| `code_hash` | Option<[u8;32]> | If contract account |
| `storage_root` | [u8;32] | Root of contract storage trie |

---  

## 5. Key APIs / Interfaces  

### 5.1 Public gRPC / HTTP Endpoints  

| Method | Path | Request | Response | Auth |
|--------|------|---------|----------|------|
| `SubmitTx` | `POST /v1/tx` | `TxSubmitRequest` (signed Tx) | `TxSubmitResponse { tx_id, status }` | API‑Key / JWT |
| `GetTxStatus` | `GET /v1/tx/{tx_id}` | – | `TxStatusResponse { status, block_height, receipt }` | API‑Key |
| `QueryBalance` | `GET /v1/account/{addr}/balance` | – | `BalanceResponse { balance }` | Public |
| `SubscribeBlocks` | `GET /v1/blocks/stream` (Server‑Sent Events) | – | Stream of `BlockHeader` | Public |
| `CallContract` | `POST /v1/contract/call` | `ContractCallRequest` | `ContractCallResponse { output, gas_used }` | API‑Key |

### 5.2 SDK Functions (example – Rust)

```rust
pub fn submit_tx(tx: SignedTx) -> Result<TxId>;
pub fn get_tx_status(id: TxId) -> Result<TxStatus>;
pub fn query_balance(addr: &AccountId) -> Result<U128>;
pub fn call_contract(
    caller: &AccountId,
    contract: &AccountId,
    data: &[u8],
    gas_limit: u64,
) -> Result<ContractResult>;
```

### 5.3 Inter‑Node Protocol  

* **Message Types** – `Proposal`, `Vote`, `Commit`, `SyncRequest`, `SyncResponse`.  
* **Transport** – libp2p (TCP + QUIC), encrypted with Noise, authenticated via node TLS certs.  
* **Serialization** – Protocol Buffers v3 (`proto/paychain.proto`).  

---  

## 6. Technology Stack  

| Layer | Technology | Version | Rationale |
|-------|-------------|---------|-----------|
| Language | **Rust** (core, VM, consensus) | 1.78 | Memory safety, zero‑cost abstractions, strong async ecosystem |
| API Gateway | **Go** (gin‑gonic) | 1.22 | Low‑latency HTTP/2, easy concurrency |
| Networking | **libp2p** (rust‑libp2p) | 0.53 | Proven P2P stack, NAT traversal |
| Consensus | **HotStuff** (custom Rust impl) | – | Linear communication complexity, fast finality |
| Storage | **RocksDB** (rust‑rocksdb) | 8.9 | High‑throughput LSM tree, point‑in‑time snapshots |
| VM | **Wasmtime** (WASM) | 23.0 | Secure sandbox, deterministic execution |
| Crypto | **blst** (BLS12‑381), **secp256k1**, **ed25519-dalek** | – | Multi‑sig support for validator set |
| Monitoring | **Prometheus** + **Grafana**, **OpenTelemetry** | – | Observability across services |
| CI/CD | **GitHub Actions**, **Docker**, **Helm** | – | Automated builds, multi‑arch images |
| Container Runtime | **Docker** (OCI) | 27.0 | Portable deployment |
| Orchestration | **Kubernetes** (v1.30) | – | Horizontal scaling of validator nodes |
| Cloud Storage | **MinIO** (S3‑compatible) | 2024‑09 | Ledger snapshots & backups |

---  

## 7. Dependencies  

| Dependency | License | Purpose |
|------------|---------|---------|
| `tokio` | MIT | Async runtime |
| `serde` / `serde_json` | MIT/Apache‑2.0 | (De)serialization |
| `prost` | Apache‑2.0 | Protobuf codegen |
| `libp2p` | MIT | P2P networking |
| `blst` | Apache‑2.0 | BLS signatures |
| `secp256k1` | MIT | ECDSA |
| `wasmtime` | Apache‑2.0 | WASM execution |
| `rocksdb` | Apache‑2.0 | Persistent KV store |
| `gin-gonic` | MIT | HTTP API |
| `prometheus/client_golang` | Apache‑2.0 | Metrics |
| `opentelemetry` | Apache‑2.0 | Tracing |

All third‑party libraries are compatible with the **Apache‑2.0** or **MIT** licenses, satisfying our permissive‑license policy.

---  

## 8. Deployment Architecture  

### 8.1 Kubernetes Manifest Overview  

* **Namespace:** `paychain`  
* **StatefulSet:** `validator-node` (replicas = validator count, PVC 200 Gi each)  
* **Deployment:** `api-gateway` (stateless, horizontal pod autoscaler)  
* **DaemonSet:** `node-exporter` (metrics)  
* **Service:** `paychain-p2p` (ClusterIP + LoadBalancer for external peers)  
* **Ingress:** TLS‑terminated, JWT‑validated entry point for SDK traffic  

### 8.2 CI/CD Pipeline  

1. **Push → GitHub Actions**  
   * Lint (`cargo fmt`, `clippy`)  
   * Unit & integration tests (`cargo test --all`)  
   * Build multi‑arch Docker images (`docker buildx`)  
2. **Release Tag** → Docker Hub & internal registry  
3. **ArgoCD** watches `helm/paychain` chart → rolls out to `staging` → smoke tests → manual promotion to `prod`.  

### 8.3 Scaling & Fault Tolerance  

| Component | Scaling Strategy | Failure Mode |
|-----------|------------------|--------------|
| Validator Nodes | Add replicas; consensus automatically re‑balances validator set via on‑chain governance | If < 2/3 of validators offline, network halts (by design) – alerts trigger auto‑scale |
| API Gateway | HPA based on request latency & CPU | Stateless – new pods replace failed ones instantly |
| Storage | RocksDB per node; snapshots replicated to MinIO (3‑way erasure) | Node crash → another validator can replay from latest snapshot |
| VM | WASM sandbox runs per‑tx; isolated – OOM kills only offending container | Crash‑only design; node restarts automatically |

---  

## 9. Security Considerations  

| Threat | Mitigation |
|--------|------------|
| **Sybil / Validator takeover** | BLS‑based weighted staking; on‑chain slashing for equivocation |
| **Replay attacks** | Nonce per account + transaction hash inclusion |
| **DoS on API** | Rate limiting per API‑Key, IP reputation, gRPC back‑pressure |
| **VM escape** | Wasmtime sandbox with deterministic memory limits, no syscalls beyond defined host functions |
| **Key compromise** | Hardware‑backed signing (YubiKey, HSM) support; optional multi‑sig for high‑value accounts |
| **Data at rest** | RocksDB encrypted with AES‑256‑GCM (per‑node key derived from KMS) |
| **Network eavesdropping** | libp2p Noise protocol + TLS for API gateway |

---  

## 10. Testing & Validation  

* **Unit Tests:** > 90 % coverage (cargo tarpaulin).  
* **Integration Tests:** Simulated 5‑node network, 10 k TPS load via `locust` scripts.  
* **Formal Verification:** Critical consensus state machine verified with TLA+.  
* **Fuzzing:** `cargo afl` on transaction deserialization and VM syscalls.  
* **Compliance:** ISO‑20022 bridge passes AML/KYC sandbox; audit logs immutable via on‑chain hashes.  

---  

## 11. Roadmap (post‑v1.0)

| Milestone | Target | Highlights |
|-----------|--------|------------|
| **v1.1** | Q4 2026 | Cross‑chain atomic swaps (BTC ↔ PAY), sharding pilot |
| **v2.0** | Q2 2027 | Permissionless validator onboarding, zk‑Rollup settlement |
| **v2.1** | Q4 2027 | Native stable‑coin module, regulatory reporting API |

---  

## 12. Glossary  

* **BFT** – Byzantine Fault Tolerance  
* **HotStuff** – Linear‑communication BFT consensus protocol  
* **WASM** – WebAssembly, portable binary instruction format  
* **Merkle‑Patricia Tree** – Sparse authenticated data structure used for state  
* **Validator Set** – Ordered list of nodes authorized to propose/commit blocks  

---  

*Prepared by the Paychain Core Engineering Team – AxentX*
