# Business Model Canvas – **paychain‑core**

| **Key Partners** | **Key Activities** | **Key Resources** |
|------------------|--------------------|-------------------|
| **Blockchain infrastructure providers** (e.g., Ethereum, Solana, Polkadot) – for node hosting, validator staking, and network upgrades | • Design & maintain the core payment‑processing protocol (consensus, settlement, routing) <br>• Develop and publish SDKs / APIs for banks, PSPs, and corporate treasury systems <br>• Operate validator nodes & monitoring services <br>• Ensure regulatory compliance (KYC/AML, PCI DSS, GDPR) <br>• Community & developer outreach (hackathons, docs, support) | • Open‑source codebase (paychain‑core repo) <br>• Proprietary consensus & fee‑optimization algorithms <br>• Cloud/edge compute for validator nodes (AWS, GCP, Azure) <br>• Security audit reports & certifications <br>• Data sets for transaction analytics (from existing Axentx datasets) |
| **Financial institutions & payment service providers (PSPs)** – early adopters & pilot partners | • Integrate paychain‑core with legacy core banking & PSP platforms <br>• Provide sandbox environments for testing <br>• Collect usage metrics & feedback for continuous improvement | • SDKs (Java, Go, Rust, Python) and API gateway <br>• Documentation portal & developer portal <br>• Support team (technical account managers) |
| **Regulators & standards bodies** (ISO 20022, FSB) | • Align protocol to emerging standards (e.g., ISO‑20022 messaging) <br>• Participate in regulatory sandboxes | • Legal counsel & compliance tooling |
| **Enterprise cloud & edge providers** (e.g., Fastly, Cloudflare) | • Deploy low‑latency edge nodes for transaction routing | • Edge compute contracts |
| **Security auditors & formal verification firms** | • Conduct periodic code audits, formal verification of smart contracts | • Audit reports, bug bounty program |

| **Value Propositions** |
|------------------------|
| • **Cost reduction** – Eliminate traditional interchange fees by settling on a permissioned blockchain with near‑zero marginal transaction cost. <br>• **Speed** – Sub‑second finality for domestic and cross‑border payments using optimized consensus (e.g., Tendermint‑style BFT). <br>• **Transparency & auditability** – Immutable ledger provides real‑time traceability for regulators and corporate auditors. <br>• **Interoperability** – Native support for ISO‑20022, tokenized digital assets, and fiat on‑ramps/off‑ramps. <br>• **Scalability** – Architecture designed for >10,000 TPS with sharding/roll‑up extensions. <br>• **Developer friendliness** – Open‑source core, language‑agnostic SDKs, and plug‑and‑play modules for settlement, compliance, and reporting. |

| **Customer Segments** |
|-----------------------|
| • **Banks & credit unions** – Core banking systems seeking cheaper, faster settlement. <br>• **Payment Service Providers (PSPs) & fintechs** – Need white‑label, programmable payment rails. <br>• **Large corporates & treasury departments** – Want direct settlement and real‑time cash management. <br>• **Digital‑asset platforms** – Require fiat‑on‑ramp/off‑ramp with regulatory compliance. <br>• **Regulators & audit firms** – Value transparent, tamper‑proof transaction logs. |

| **Channels** |
|--------------|
| • **Direct sales** – Enterprise account executives targeting banks/PSPs. <br>• **Partner ecosystem** – Cloud providers & system integrators (Accenture, Deloitte) delivering implementation services. <br>• **Developer portal** – Open‑source repo, SDKs, API docs, sample apps. <br>• **Industry events & webinars** – FinTech conferences, blockchain consortia. <br>• **Regulatory sandboxes** – Co‑development with central banks. |

| **Revenue Streams** |
|----------------------|
| 1. **License‑as‑a‑Service (LaaS)** – Subscription tier for hosted validator nodes, monitoring, and SLA guarantees (monthly/annual). <br>2. **Transaction fee share** – Small per‑transaction fee (e.g., 0.05 % of settlement amount) collected from on‑chain activity, capped for high‑volume customers. <br>3. **Professional services** – Integration, custom module development, compliance consulting (time‑and‑material or fixed‑price). <br>4. **Enterprise support contracts** – 24/7 priority support, security patches, and upgrade paths. <br>5. **Data & analytics licensing** – Aggregated, anonymized transaction insights sold to market‑research firms. |

| **Cost Structure** |
|--------------------|
| • **Infrastructure** – Validator node hosting, edge routing, storage, bandwidth. <br>• **R&D & engineering** – Salaries for core protocol team, SDK developers, security engineers. <br>• **Compliance & legal** – Ongoing regulatory monitoring, audit fees, certifications. <br>• **Sales & marketing** – Enterprise sales team, partner enablement, conference sponsorships. <br>• **Security & audits** – Third‑party code audits, bug bounty program, formal verification tools. <br>• **Community & open‑source maintenance** – Documentation, issue triage, community events. |

| **Key Metrics** |
|-----------------|
| • **TPS (transactions per second) achieved in production** <br>• **Average settlement latency** <br>• **Number of active validator nodes** <br>• **Monthly recurring revenue (MRR)** <br>• **Customer acquisition cost (CAC) vs. LTV** <br>• **Compliance audit pass rate** <br>• **Developer adoption (SDK downloads, GitHub stars/forks)** |

---  

*Prepared by the Paychain‑Core product/engineering lead, Axentx – 2026‑06‑17*
