# Hindsight Memory Skill for Copilot

## Purpose
Use Hindsight as Copilot’s long-term memory so you can carry forward useful context across sessions, recall relevant project knowledge before answering, and retain durable insights after completing meaningful work.

Treat Hindsight as a support layer for continuity:
- use it to recover relevant past context,
- use it to preserve important new context,
- use it to improve consistency across interactions.

If Hindsight is connected through MCP, use the MCP-exposed Hindsight tools as the primary interface for recall, retain, and reflection.

---

## Core behavior
Work with Hindsight in three modes:

1. **Recall**
   - Before answering, recall relevant memory when the task may benefit from prior context.
   - Use recall especially for project conventions, user preferences, prior decisions, recurring bugs, architecture history, and ongoing tasks.

2. **Retain**
   - After completing a meaningful interaction, retain durable information that will likely help in future sessions.
   - Save stable knowledge, not transient noise.

3. **Reflect**
   - When raw recalled memories are too fragmented, use reflection to synthesize what Hindsight already knows into a concise working summary.
   - Prefer a compact synthesis over dumping many loosely related memories.

---

## When to use Hindsight
Use Hindsight proactively in cases like these:

- the user refers to something discussed before;
- the request depends on prior project decisions;
- the task involves established conventions or preferences;
- the user is continuing earlier work;
- the project has recurring workflows, fixes, or architecture patterns;
- the answer would improve if you remembered prior context.

Use Hindsight less aggressively when the task is fully self-contained and does not benefit from memory.

Good pattern:
- **Recall first when continuity matters.**
- **Answer normally when memory adds little value.**

---

## MCP usage rule
If Hindsight is available through MCP, use the MCP-connected Hindsight tools directly.

Follow this rule:
- first check whether the current task would benefit from memory;
- if yes, use the MCP Hindsight tool for recall before drafting the answer;
- once the task is completed, use the MCP Hindsight tool again to retain durable insights.

Treat MCP as the runtime connection layer that exposes Hindsight capabilities.
If the MCP tool is unavailable, continue the task normally without blocking.

---

## How to recall before answering
Before responding, do this:

1. Decide whether prior memory could improve the answer.
2. If yes, perform a targeted recall.
3. Prefer focused recall over broad recall.
4. Pull only the memories that are clearly relevant to the current task.
5. Use the recalled content to shape the answer, not to overwhelm it.

Do this:
- recall project-specific conventions before suggesting code changes;
- recall user preferences before choosing style, structure, or tooling;
- recall earlier debugging outcomes before proposing a new fix;
- recall ongoing objectives before planning next steps.

Do this instead of this:
- **Do this:** perform a focused recall for relevant past decisions.
- **Instead of this:** answering from scratch when the user is clearly continuing prior work.

- **Do this:** recall a small, high-signal set of memories.
- **Instead of this:** injecting large amounts of loosely related context.

- **Do this:** use recalled memory to improve precision.
- **Instead of this:** repeating memory verbatim without synthesis.

---

## How to retain after useful interactions
After completing a meaningful task, retain useful long-term knowledge.

Retain information like:
- user preferences that are likely to stay stable;
- project structure and architecture decisions;
- coding conventions and naming rules;
- important debugging discoveries;
- recurring failure modes and validated fixes;
- environment or workflow details that will help again;
- long-running goals, plans, and project direction.

Do this:
- retain the conclusion after a bug is root-caused;
- retain a newly established project convention;
- retain a user’s stable formatting or workflow preference;
- retain a confirmed architectural decision.

Do this instead of this:
- **Do this:** retain durable, reusable conclusions.
- **Instead of this:** saving every message or every temporary thought.

- **Do this:** save stable context after successful resolution.
- **Instead of this:** storing speculative or unverified assumptions.

- **Do this:** retain concise summaries of what matters.
- **Instead of this:** retaining noisy transcripts when only a few facts are useful.

---

## What to store
Prefer storing information that remains useful over time.

High-value memory includes:
- repository or project conventions;
- preferred languages, frameworks, and tools;
- user preferences for explanations, formatting, and workflow;
- architecture decisions and rationale;
- common commands and setup expectations;
- recurring issue patterns and their solutions;
- reusable implementation constraints;
- milestone goals and long-term plans;
- relationships between services, packages, or components;
- validated assumptions that help future task execution.

When possible, store information in a compact, actionable form.

Good examples:
- “User prefers concise diffs and short implementation summaries.”
- “Project uses pnpm, not npm.”
- “Auth middleware must run before tenant resolution.”
- “Team prefers explicit types in exported TypeScript APIs.”
- “The flaky test usually fails when background jobs are not drained.”

---

## What not to store
Keep memory clean and safe.

Do not store:
- secrets, API keys, passwords, tokens, credentials;
- personal sensitive data unless explicitly appropriate and safely handled;
- raw confidential content that should not persist;
- one-off noise with no future value;
- speculative conclusions;
- obsolete or contradictory details without clarification;
- verbose transcripts when a short summary is enough.

Do this:
- store the useful conclusion.
- avoid storing the sensitive source material.

Do this instead of this:
- **Do this:** retain “deployment requires region X and service Y.”
- **Instead of this:** retaining the full secret-bearing deployment transcript.

- **Do this:** retain validated troubleshooting guidance.
- **Instead of this:** retaining every failed hypothesis.

---

## Project scoping and memory bank rules
Use the correct memory scope so unrelated projects do not contaminate each other.

Prefer project-aware memory organization:
- use a project-specific or repository-specific bank when available;
- keep memory separated across unrelated codebases;
- use dynamic bank selection when the integration supports it.

Follow this rule:
- if the task belongs to a specific repository, workspace, or project, use that scope consistently;
- if the user switches projects, switch memory scope too;
- if shared memory would create confusion, prefer isolated memory.

Do this:
- keep one project’s architecture and conventions in that project’s memory scope;
- separate personal preferences from repository-specific conventions when the tool supports that distinction.

Do this instead of this:
- **Do this:** use the project or workspace bank.
- **Instead of this:** mixing memories from unrelated repositories.

---

## Reflection behavior
When recalled results are numerous or fragmented, create a short working synthesis.

Use reflection to:
- summarize what matters from past sessions;
- combine related memories into one practical conclusion;
- reduce clutter before responding.

Good pattern:
- reflect first when memory is noisy,
- then answer from the reflected summary.

Do this instead of this:
- **Do this:** synthesize three related memories into one actionable conclusion.
- **Instead of this:** surfacing all three as separate, repetitive fragments.

---

## Response behavior when memory is used
When recalled memory materially improves the answer, incorporate it naturally.

Prefer this style:
- use memory to make the response more consistent, precise, and helpful;
- mention prior context briefly when doing so helps the user understand the answer;
- keep the answer focused on the current task.

Examples:
- “Based on the project convention established earlier, I’ll keep this in the existing service layer.”
- “You previously preferred short summaries, so I’ll keep this concise.”
- “From earlier debugging context, this looks related to the same migration issue.”

Do this instead of this:
- **Do this:** briefly acknowledge relevant remembered context when it meaningfully affects the answer.
- **Instead of this:** over-explaining internal memory usage on every response.

---

## Fallback behavior
If Hindsight or the MCP connection is unavailable, continue normally.

Follow this pattern:
- do not block the task;
- do not over-apologize;
- answer using the available repository context and current conversation;
- proceed as a capable assistant even without memory.

Do this instead of this:
- **Do this:** continue with best-effort reasoning if memory tools are unavailable.
- **Instead of this:** stopping the workflow because Hindsight could not be reached.

---

## Suggested operating pattern
For continuity-sensitive tasks, follow this sequence:

1. Check whether memory would help.
2. Recall only relevant context through the MCP-connected Hindsight tool.
3. Synthesize recalled results if needed.
4. Answer or act using the enriched context.
5. Retain durable insights after the task is completed.

Use this sequence consistently to make interactions feel continuous, informed, and adaptive over time.

---

## Default decision rule
When in doubt:

- **Recall** if the task may depend on prior context.
- **Reflect** if the recalled context is noisy or fragmented.
- **Retain** if the new information is durable and likely to help again.
- **Skip memory** if the task is trivial, fully self-contained, or not improved by long-term context.

The goal is not to use memory constantly.
The goal is to use memory well.