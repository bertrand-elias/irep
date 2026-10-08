# Requirements: Interactive Review & Evidence Pipeline (IREP)

## 1. Scope & System Boundary

`irep` is an evidence-verification CLI designed to assist an Independent Internal Human Reviewer evaluating RFC-001. Under governance standard NEF-STD-009 §8.3 and §31, the pipeline and reviewer possess no approval, veto, ratification, ownership, Sponsor, or Decision Authority [Brief §1]. The pipeline makes no governance decisions; it verifies evidence, validates citations, assists draft generation, and enforces a durable human review gate [Brief §1, §4].

---

## 2. Functional Requirements (Seeded Brief Rules)

### REQ-01: Read-Only Evidence Package

* **Source:** Brief §5 ("Do not modify the supplied evidence. Work on copies if you annotate.")
* **Description:** The pipeline must treat the evidence package (`repo/`, `derived/`, `MANIFEST.md`, `MANIFEST.sha256`) as strictly immutable. All operations must run read-only.
* **Acceptance Criteria:** After any command executes, the package's file hashes and file modification timestamps are verified to be unchanged.

### REQ-02: Cryptographic Checksum Integrity & Manifest Verification

* **Source:** Brief §3 ("Everything is listed, with SHA-256 checksums, in MANIFEST.md (checksums for every file: MANIFEST.sha256).")
* **Description:** The pipeline must compute SHA-256 hashes of all supplied files and verify them against `MANIFEST.sha256`.
* **Acceptance Criteria:** Ingestion halts immediately with an integrity error if any listed file is missing or yields a checksum mismatch.
* **Stage 2 Open Decision:** Determine behavior for present but unlisted files (e.g., OS artifacts like `.DS_Store`): should unlisted files halt execution as an untracked artifact violation, or emit a non-blocking warning?

### REQ-03: Evidence Reference Traceability (`path:line` or `path:§`)

* **Source:** Brief §5 ("Refer to material by file path and line number (or section number)...") and §6 ("Supplied-file path plus line or section").
* **Description:** Every finding drafted or exported must cite its source formatted as `<supplied-path>:<line>` or `<supplied-path>:<§section>`.
* **Acceptance Criteria:** The CLI validator rejects any finding lacking an explicit, resolvable path reference to a file verified under REQ-02.

### REQ-04: Finding Identifier Uniqueness & Discipline

* **Source:** Brief §6 ("Findings, each with a unique identifier of your choice (for example F-01, F-02). Do not use identifiers beginning with HD-; those denote human governance decisions.")
* **Description:** Every finding must possess a globally unique identifier within the consultation return. Sequential numbering (e.g., `F-01`, `F-02`) is an adopted design convention.
* **Acceptance Criteria:** The validator rejects duplicate finding IDs and halts with an error if any finding identifier starts with the `HD-` prefix.

### REQ-05: Strict Review Taxonomy (Classification & Categories)

* **Source:** Brief §4 ("Classification of findings") and §6 ("Classification of each finding").
* **Description:** Findings must conform strictly to the two brief-defined classifications and nine designated categories:
  * **Classification:** `Material concern` | `Observation`
  * **Category:** `factual error` | `internal inconsistency` | `governance conflict` | `unsupported claim` | `missing evidence` | `ambiguous requirement` | `implementation risk` | `unresolved concern` | `other`
* **Acceptance Criteria:** Schema validation rejects any finding using classifications or categories outside this closed vocabulary.

### REQ-06: Mandatory AI Disclosure

* **Source:** Brief §5 ("If you use any AI tool in preparing your return, disclose which and for what...") and §6 ("Independence and conflict disclosure, including any AI tool use...").
* **Description:** The pipeline must record and export an explicit declaration specifying the AI model used and the scope of its assistance.
* **Acceptance Criteria:** Export of the final review return is blocked if the AI disclosure field is blank or omitted.

### REQ-07: Independent Judgment & Wording Provenance Tracking

* **Source:** Brief §4 ("Evaluate RFC-001 independently... in your own judgment") and §5 ("Use your own judgment and wording. Do not adopt the wording of any other reviewer, tool, or summary as your own without saying so.")
* **Description:** The system tracks the origin of all text. Every finding must record an explicit provenance tag: `reviewer-authored`, `ai-drafted-and-edited`, or `ai-adopted-as-is`.
* **Acceptance Criteria:** The pipeline requires explicit confirmation and rejects export if any finding has unverified or untracked text provenance.

### REQ-08: Explicit Disagreement Framing

* **Source:** Brief §4 ("If you disagree with any proposition in RFC-001... say so explicitly and identify the proposition.")
* **Description:** Any logged disagreement must explicitly cite and name the exact proposition it disputes.
* **Acceptance Criteria:** Disagreements submitted without a referenced proposition string or target identifier fail validation.

### REQ-09: Mandated 10-Part Return Structure

* **Source:** Brief §6 ("Requested return: Please return a single document, in your own words, with the following parts [1-10]...")
* **Description:** The exported document must strictly adhere to the ten numbered sections specified in the brief.
* **Acceptance Criteria:** Exporter generates an error if any of the 10 mandated sections are missing from the output document.

### REQ-10: Evidence Coverage Map (Materials Reviewed vs. Unread)

* **Source:** Brief §6 item 3 ("Materials actually reviewed — by manifest path; state which parts of the package you did not read.")
* **Description:** The system must record every file and section read during the review process and compile an unread coverage list against all files in `MANIFEST.md`.
* **Acceptance Criteria:** The final return document automatically lists both inspected files and all package files left unread.

### REQ-11: Canonical Precedence (`repo/` Governs `derived/`)

* **Source:** Brief §3 ("If a derived file and a repo/ file ever differ, the repo/ file governs.")
* **Description:** Findings citing only files in `derived/` must be flagged for manual verification against authoritative sources in `repo/`.
* **Acceptance Criteria:** The system warns the reviewer when a finding references `derived/` without a corresponding `repo/` anchor.

### REQ-12: Non-Resolution of Open Decisions

* **Source:** Brief §4 ("Open decisions... You are not asked to resolve them and have no authority to.")
* **Description:** The automated drafter must never generate recommendations or finding statements that purport to resolve decisions marked as `OPEN`.
* **Acceptance Criteria:** Automated prompts enforce non-resolution; drafting rules block proposing status transitions for open governance items.

### REQ-13: Verbatim Recording of Reviewer Statements

* **Source:** Brief §1, §5.4, and Commencement ("Independence... disclose it", "Bertrand Elias acknowledges receipt...")
* **Description:** The reviewer's identity, conflict declarations, and commencement acknowledgments are recorded as written by the human reviewer. The system must never draft, autocomplete, or alter these entries.
* **Acceptance Criteria:** Return templates require direct human input for Parts 1 and 2, bypassing LLM generation entirely.

---

## 3. Non-Functional Requirements (Engineering Standards)

### NFR-01: Strict Static Type Safety

* All Python codebase files must satisfy `mypy --strict` with zero typing errors or untyped definitions.

### NFR-02: Deterministic Environment & Lockfile Hygiene

* Dependencies must be managed with `uv` and pinned strictly in `uv.lock` using PEP 735 `[dependency-groups]`.

### NFR-03: Zero Real-Package Contamination

* Repository `.gitignore` rules must block committing real governance packages or return artifacts (`*review-package*`, `*REVIEW-RETURN*`).
