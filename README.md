# BillLens 🔎🇬🇧

### AI-powered parliamentary intelligence for everyone.

**Ask Parliament a question. BillLens finds the evidence and explains what actually happened.**

> "What has Parliament actually done about housing?"

Instead of searching hundreds of parliamentary pages, BillLens brings together parliamentary debates, bills, legislation, votes and MPs to produce a clear, evidence-backed answer.

---

## 🚀 What is BillLens?

Parliamentary information is public, but understanding it can be difficult.

Important information is spread across bills, debates, amendments, divisions, parliamentary questions and legislation.

BillLens uses AI-powered search and reasoning to connect these sources and turn them into answers that ordinary citizens can understand.

### Ask questions like:

* What has Parliament actually done about housing?
* What laws have changed because of this issue?
* Which MPs proposed these changes?
* What did Parliament vote on?
* What happened to this bill?
* Which MPs voted for or against it?
* What has been proposed but never implemented?
* What has my MP said or voted on?
* What changed in the law after this debate?

---

## ✨ Core Features

### 🧠 Ask Parliament

Ask a question in natural language and BillLens searches relevant parliamentary and legislative sources.

### 📜 Bills & Legislation

Understand:

* Bills
* Acts
* Amendments
* Legislative changes
* Current status

### 🏛️ Parliamentary Debates

Find relevant debates and explain what MPs actually discussed.

### 👥 MP Intelligence

Explore:

* MPs
* Parliamentary questions
* Contributions
* Relevant votes
* Policy positions supported by parliamentary evidence

### 🗳️ Voting Intelligence

BillLens connects questions to relevant parliamentary divisions and helps users understand what MPs voted on.

### 🔍 Evidence-backed answers

BillLens does not simply generate an answer.

It identifies supporting evidence and provides links to the underlying parliamentary or legislative source.

### ⚠️ "What didn't happen?"

One of BillLens's key features is identifying proposals, bills and parliamentary activity that did not result in legislative change.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    BillLens Web     │
                    │   Citizen Question   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AI Research Agent │
                    │ Query planning       │
                    │ Retrieval            │
                    │ Reasoning            │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       Parliament APIs    Legislation       Debate data
       MPs / Bills        Acts / changes    Hansard
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Search + RAG Layer  │
                    │ Semantic retrieval  │
                    │ Evidence ranking    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Evidence Verifier   │
                    │ Source checking      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    BillLens Answer  │
                    │ Clear + sourced      │
                    │ + understandable     │
                    └─────────────────────┘
```

---

## 🛠️ Technology

* Python
* FastAPI
* AI/LLM reasoning
* Retrieval-Augmented Generation (RAG)
* Semantic search
* Vector search
* Parliamentary APIs
* UK legislation data
* MCP-compatible AI tooling
* Modern web interface

---

## 🎯 Example

### Question

> What has Parliament actually done about housing?

### BillLens

**Short answer**

Parliament has introduced, debated and amended legislation affecting housing, while MPs have also raised housing issues through debates and parliamentary questions.

**Bills & legislation**

BillLens identifies relevant legislation and explains what changed.

**Parliamentary activity**

BillLens identifies relevant debates and parliamentary contributions.

**Votes**

Relevant parliamentary divisions are surfaced with the subject of each vote.

**What hasn't happened**

BillLens identifies proposals or bills that did not progress into law.

**Evidence**

Every major claim can be traced back to its underlying source.

---

## 🔐 Transparency by design

BillLens is designed around a simple principle:

> **AI should explain Parliament, not replace the evidence.**

Answers are therefore accompanied by supporting sources whenever possible.

Users can inspect the evidence behind an answer instead of blindly trusting an AI-generated response.

---

## 🌍 Why BillLens?

Parliamentary information is public.

Understanding it shouldn't require being a parliamentary researcher.

BillLens makes parliamentary information:

**Searchable → Understandable → Verifiable**

---

## 🧪 Hackathon Project

BillLens was created as an experimental AI application demonstrating how public parliamentary and legislative information can be transformed into an accessible citizen-facing research experience.

---

## ⚖️ Data & Attribution

BillLens uses publicly available parliamentary and legislative information and may incorporate open-source software and APIs from third-party projects.

Where third-party code is used, the applicable licences and attribution notices are preserved in `THIRD_PARTY_NOTICES.md`.

BillLens is an independent project and is not an official UK Parliament or UK Government product.

---

## 🚧 Status

**Prototype / Hackathon**

The current version is a research prototype. Data coverage, source availability and AI-generated answers may contain limitations.

Users should verify important information against the original parliamentary and legislative sources.

---

## 🗺️ Roadmap

* [x] Natural-language parliamentary questions
* [x] Semantic document retrieval
* [x] Evidence-backed answers
* [ ] MP profiles
* [ ] Parliamentary voting explorer
* [ ] Bill timeline visualisation
* [ ] "What changed?" legislation comparison
* [ ] Personalised "My MP" dashboard
* [ ] Political promise → parliamentary action tracking
* [ ] Parliamentary issue trend detection
* [ ] Public API
* [ ] Mobile application

---

## ⭐ Vision

**BillLens makes Parliament understandable to everyone.**

Ask a question.

See what happened.

Understand who did what.

Follow the evidence.

---

## 📄 Licence

See `LICENSE` and `THIRD_PARTY_NOTICES.md` for project and dependency licensing information.
