# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

This repo (`AIML`) holds two independent bodies of work plus root-level config:

- **`Salesforce/`** — a Salesforce DX project named **"Udemy - Agentforce"** ("Agent Script Recipes"). Self-contained: its own `package.json`, `sfdx-project.json`, and tooling. Run all npm/`sf` commands from inside `Salesforce/`, not the repo root.
- **`Python/`** — a Python fundamentals learning track: standalone exercise scripts for collections, loops, functions, file I/O, JSON, and pandas/numpy/seaborn EDA (`*_prac.py`), plus a `python fundamentals.ipynb` notebook and sample data files (`students.csv`, `student_records.txt`, etc.). Not connected to the Salesforce project.
- **Root** — repo-wide config only (`CLAUDE.md`, `.gitignore`).

Default Salesforce org alias on this machine: **`AgentScript`** (global `target-org`). See the auto-memory note on the Salesforce MCP server for connection details and its read-only-data limitation.

## Branch-per-area strategy (important)

Each area has its own branch off `main`; **never mix areas in one branch/commit**:

| Editing… | Branch | Commit prefix |
| --- | --- | --- |
| `Python/…` | `feature/python` | `Python: …` |
| `Salesforce/…` | `feature/Salesforce` | `Salesforce: …` |
| Root files | `feature/root` | `Root: …` |

`main` is the integration branch (already contains the merged Salesforce work). Workflow: branch off / sync with `main` → commit only your area's files → `git push` (plain push; the one-time history rewrite is done, so no `--force`) → open a PR into `main`. Before pushing, sanity-check scope: `git diff --name-only origin/main...HEAD` should list only your area's paths. Don't commit directly to `main`.

## Salesforce — commands (run from `Salesforce/`)

These npm scripts need Node/npm on PATH. On this machine Node is **not** on PATH by default (only the Salesforce CLI, which bundles its own Node); install Node or use the bundled one for the npm-based scripts. The `sf` commands work as-is.

| Task | Command |
| --- | --- |
| Run all LWC Jest tests | `npm run test:unit` |
| Run a single LWC test | `npm run test:unit -- <path/to/x.test.js>` or `npm run test:unit -- --findRelatedTests <component.js>` |
| Watch / debug / coverage | `npm run test:unit:watch` · `npm run test:unit:debug` · `npm run test:unit:coverage` |
| Lint JS (aura/lwc) | `npm run lint` |
| Format / check | `npm run prettier` · `npm run prettier:verify` |
| Deploy metadata | `sf project deploy start --target-org AgentScript` (scope with `-d <dir>` or `-m <type:Name>`) |
| Retrieve metadata | `sf project retrieve start --target-org AgentScript` |
| Run Apex tests in org | `sf apex run test --target-org AgentScript` (or the MCP `run_apex_test` tool) |
| Run anonymous Apex | `sf apex run --file scripts/apex/hello.apex --target-org AgentScript` |
| Run a SOQL query | `sf data query --query "<SOQL>" --target-org AgentScript` (or the MCP `run_soql_query` tool) |

A Husky `pre-commit` hook runs `lint-staged`: Prettier on most file types, ESLint on aura/lwc JS, and `sfdx-lwc-jest --bail --findRelatedTests` on changed LWC.

**Note:** `sfdx-project.json` pins `sourceApiVersion` **65.0** but the connected org is on API **66.0** — keep new metadata at a version the org accepts.

## Salesforce — architecture

A collection of **Agentforce agent recipes**. The core building block is **Agent Script** — agents authored as `.agent` text files (a custom DSL), not clicks.

```
.agent file  ──(action target)──►  Flow  │  Apex @InvocableMethod  │  genAiPromptTemplate
(aiAuthoringBundles)                (flows) (classes)                (genAiPromptTemplates)
```

- **Agent bundles** — `force-app/main/default/aiAuthoringBundles/<Name>/<Name>.agent` + `<Name>.bundle-meta.xml`. The `.agent` file defines the conversation: `config` → `variables` → `system` → `connections` → `knowledge` → `language` → `start_agent` → `topic` blocks (this ordering is mandatory). Topics declare `actions` whose `target:` points at a Flow (`flow://`), Apex (`apex://`), prompt template (`prompt://`), etc. **Always read `Salesforce/.airules/AGENT_SCRIPT.md` before writing or editing a `.agent` file** — the DSL has strict, easy-to-miss rules (e.g. `@utils.transition to` in `reasoning.actions` vs bare `transition to` in directive blocks; capitalized `True`/`False`; mutable vars need defaults, linked vars need a `source` and no default; `...` is slot-filling only).

- **Apex services** — `force-app/main/default/classes/*.cls`. The agent/Flow-callable actions, written as `@InvocableMethod` with inner request/result wrapper classes annotated `@InvocableVariable` (see `CaseEscalationScoreService.cls` for the canonical shape). They take a `List<Request>` and return a `List<Result>` but are **designed for single-record Agentforce execution** (operate on `requests[0]`). Follow `Salesforce/.airules/APEX_RULES.md`: user-mode DML/SOQL (`WITH USER_MODE`, `AccessLevel.USER_MODE`), bulkification, no SOQL/DML in loops, no hardcoded IDs, queueables (never `@future`), ≥75% meaningful test coverage.

- **Supporting metadata** — `flows/` (invocable Flows), `genAiPromptTemplates/` (prompt templates used as actions/grounding), `lightningTypes/` (custom input/output types with `schema.json` + renderer/editor JSON), `lwc/` (Lightning Web Components, each with a `__tests__/` Jest suite).

### `.airules/` — project-authored rules
`Salesforce/AGENTS.md` indexes topic-specific rule files in `Salesforce/.airules/`. **Read the relevant one only when working on that topic:** `AGENT_SCRIPT.md` (Agent Script DSL), `APEX_RULES.md` (Apex standards), `README_STRUCTURE.md` (recipe README structure), `MERMAID_DIAGRAMS.md` (diagram formatting), `GENERATE_CHANGELOG.md` (changelog generation).

## Python — running the exercises

Standalone scripts; run one directly, e.g. `python Python/Loops.py`. The EDA scripts (`pandas_prac*.py`, `numpy_prac.py`, `eda_prac.py`) require **pandas, numpy, seaborn, matplotlib**. There's no `requirements.txt`; a `Python/venv/` exists — activate it (`Python/venv/Scripts/activate` on Windows) or `pip install pandas numpy seaborn matplotlib`. The full exercise set lives on the `feature/python` branch (only the notebook is on `main` until merged).
