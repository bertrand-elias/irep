# ADR-001: Pipeline Orchestration via Plain Python and Local State Persistence

## Status

Accepted

## Context

The Interactive Review & Evidence Pipeline (`irep`) coordinates evidence verification, LLM drafting, and human review gates.

The principal architectural constraint is that the human review and sign-off phase is asynchronous and can remain paused for multiple days. Consequently, in-memory execution is insufficient; pipeline state must survive process termination, CLI exit, and machine restarts.

We require an orchestration mechanism that manages long-lived paused states, deterministic verification gates, and step execution without introducing unnecessary external infrastructure.

## Decision

We will orchestrate the pipeline using **plain Python control flow** and manage paused review state via **explicit SQLite serialization** (introduced in Stage 3), rather than adopting an external durable-workflow runtime or LLM graph framework.

## Alternatives Rejected

1. **LangGraph (with Built-in Checkpointing)**
   * *Evaluation:* Provides out-of-the-box state graph persistence and checkpointing designed for agentic loops.
   * *Reason Rejected:* Adds significant framework abstraction, complex graph debugging overhead, and tight coupling to the LangChain ecosystem for what is fundamentally a linear, predictable governance review flow.

2. **Temporal (Durable Execution Platform)**
   * *Evaluation:* The industry standard for durable workflows with arbitrary long-term pauses, timers, and automatic retry states.
   * *Reason Rejected:* Requires maintaining a separate daemon/server cluster and external service dependencies, creating excessive operational footprint for a local, single-reviewer CLI tool.

## Reversal Trigger

We will reconsider this decision and migrate to a framework like LangGraph or Temporal if:

* The review workflow evolves beyond linear transitions to require complex dynamic branching or multi-reviewer consensus graphs.
* The maintenance overhead of custom SQLite schema migrations and state serialization exceeds the overhead of adopting an external runtime (i.e., if we find ourselves rebuilding an ad-hoc workflow engine from scratch).

## Consequences

* **Positive:** Zero external services or daemon dependencies; straightforward unit testing with standard `pytest` fixtures; transparent SQLite inspection using standard tools.
* **Negative:** State persistence, resume logic, and schema migration must be implemented and tested manually rather than inherited from a managed engine.
