# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

This git repo root contains one real project plus some incidental scaffolding:

- **`Salesforce/`** — the actual project: a Salesforce DX project named **"Udemy - Agentforce"** ("Agent Script Recipes"). **Nearly all work happens here.** It has its own `package.json`, `sfdx-project.json`, and tooling — run npm/sf commands from inside `Salesforce/`, not the repo root.
- `Python/` — an empty Sphinx-docs scaffold (`source/_static`, `source/_templates`, `build/`, `venv/`). Not part of the Salesforce work.
- `test.py`, `test2.py`, `test3.ipynb` (repo root) — throwaway "hello world" scratch files (deleted in the working tree). Ignore.

Default Salesforce org alias for this machine: **`AgentScript`** (set as the global `target-org`). See the auto-memory note on the Salesforce MCP server for connection details and its read-only-data limitation.

## Commands (run from `Salesforce/`)

| Task | Command |
| --- | --- |
| Run all LWC Jest tests | `npm run test:unit` |
| Run a single LWC test | `npm run test:unit -- <path/to/test.test.js>` or `npm run test:unit -- --findRelatedTests <component.js>` |
| Watch / debug / coverage | `npm run test:unit:watch` · `npm run test:unit:debug` · `npm run test:unit:coverage` |
| Lint JS (aura/lwc) | `npm run lint` |
| Format / check formatting | `npm run prettier` · `npm run prettier:verify` |
| Deploy metadata to org | `sf project deploy start --target-org AgentScript` (add `-d <dir>` or `-m <type:Name>` to scope) |
| Retrieve metadata | `sf project retrieve start --target-org AgentScript` |
| Run Apex tests in org | `sf apex run test --target-org AgentScript` (or the MCP `run_apex_test` tool) |
| Run anonymous Apex | `sf apex run --file scripts/apex/hello.apex --target-org AgentScript` |
| Run a SOQL query | `sf data query --query "<SOQL>" --target-org AgentScript` (or the MCP `run_soql_query` tool) |

A Husky `pre-commit` hook runs `lint-staged`: Prettier on most file types, ESLint on aura/lwc JS, and `sfdx-lwc-jest --bail --findRelatedTests` on changed LWC.

**Note:** `sfdx-project.json` pins `sourceApiVersion` **65.0**, but the connected org is on API **66.0** — keep new metadata at a version the org accepts.

## Architecture

This project is a collection of **Agentforce agent recipes**. The core building block is **Agent Script** — agents authored as `.agent` text files (a custom DSL), not clicks.

**The wiring (how a recipe fits together):**

```
.agent file  ──(action target)──►  Flow  │  Apex @InvocableMethod  │  genAiPromptTemplate
(aiAuthoringBundles)                (flows) (classes)                (genAiPromptTemplates)
```

- **Agent bundles** — `force-app/main/default/aiAuthoringBundles/<Name>/<Name>.agent` + `<Name>.bundle-meta.xml`. The `.agent` file defines the conversation: `config` → `variables` → `system` → `connections` → `knowledge` → `language` → `start_agent` → `topic` blocks (this ordering is mandatory). Topics declare `actions` whose `target:` points at a Flow (`flow://`), Apex (`apex://`), prompt template (`prompt://`), etc. **Always read `Salesforce/.airules/AGENT_SCRIPT.md` before writing or editing a `.agent` file** — the DSL has strict, easy-to-miss rules (e.g. `@utils.transition to` in `reasoning.actions` vs bare `transition to` in directive blocks; capitalized `True`/`False`; mutable vars need defaults, linked vars need a `source` and no default; `...` is slot-filling only).

- **Apex services** — `force-app/main/default/classes/*.cls`. These are the agent/Flow-callable actions, written as `@InvocableMethod` with inner request/result wrapper classes annotated `@InvocableVariable` (see `CaseEscalationScoreService.cls` for the canonical shape). They take a `List<Request>` and return a `List<Result>` but are **designed for single-record Agentforce execution** (operate on `requests[0]`). Follow `Salesforce/.airules/APEX_RULES.md`: user-mode DML/SOQL (`WITH USER_MODE`, `AccessLevel.USER_MODE`), bulkification, no SOQL/DML in loops, no hardcoded IDs, queueables (never `@future`), and ≥75% meaningful test coverage.

- **Supporting metadata** — `flows/` (invocable Flows), `genAiPromptTemplates/` (prompt templates used as actions/grounding), `lightningTypes/` (custom input/output types with `schema.json` + renderer/editor JSON), `lwc/` (Lightning Web Components, each with a `__tests__/` Jest suite).

## `.airules/` — project-authored rules

`Salesforce/AGENTS.md` indexes a set of topic-specific rule files in `Salesforce/.airules/`. **Read the relevant one only when working on that topic:**

- `AGENT_SCRIPT.md` — full Agent Script DSL syntax, patterns, validation checklist, common mistakes.
- `APEX_RULES.md` — Apex standards (governor limits, security/FLS, `@InvocableMethod` patterns, testing).
- `README_STRUCTURE.md` — standard structure for per-recipe README files.
- `MERMAID_DIAGRAMS.md` — Mermaid diagram formatting rules for docs.
- `GENERATE_CHANGELOG.md` — prompt/format for generating `CHANGELOG.md` from git commits.
