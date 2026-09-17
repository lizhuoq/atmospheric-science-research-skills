# Skill architecture

## Layers

1. **Live source acquisition** — a task begins with a scoped question and routes searches across available scholarly databases, DOI registries, repositories, and publisher pages. Access, query, screening, version, and provenance are logged.
2. **Example corpus and evaluation fixtures** — `data/metadata/all_selected.csv` and the bundled index are development examples, terminology seeds, and regression-test inputs. They are not the installed Skill's knowledge boundary. Local PDFs are private build inputs and never a public package dependency.
3. **Derived evaluation indexes** — `data/derived/paper_topics.csv` contains inspectable multi-label classifications; `data/splits/` freezes leakage boundaries for development and benchmark evaluation, not for a user's new literature review.
4. **Evidence contract** — `schemas/evidence-record.schema.json` defines atomic claims, scientific context, locators, applicability, limitations, conflict status, and provenance.
5. **Workflow Skills** — concise `SKILL.md` entrypoints route to source discovery, full-text reading, focused domain references, and deterministic scripts. Scientific content is not copied into the entrypoint.
6. **Evaluation** — unit tests enforce structural invariants; behavioral cases assess scientific decisions and blind-test generalization.

## Initial Skill boundary

`atmospheric-science-research` is a lightweight orchestrator. Twelve task-distinct Skills cover literature search, paper reading, research design, statistics and verification, data and retrieval QC, figure analysis, numerical experiments, extremes attribution, composition/air quality, manuscript writing, claim audit, and peer review. The orchestrator selects only relevant stages and consolidates their artifacts; it does not duplicate specialist procedures.

Further Skills should be added only where procedures materially diverge. Possible later clusters are:

- boundary-layer/turbulence diagnostics;
- cloud and precipitation microphysics;
- radiative-transfer experiments;
- land/atmosphere and ocean/atmosphere coupled-process diagnostics;
- paleoclimate proxy and chronology assessment.

## Orchestration contract

The orchestrator passes scoped questions, source ledgers, evidence records, data/configuration inventories, analysis decisions, and unresolved issues between Skills. A downstream Skill must preserve provenance and must not silently upgrade metadata to evidence, association to causality, model output to observation, or an unreviewed machine draft to expert knowledge.

## Portability

Skills follow the open `SKILL.md` folder convention: frontmatter for discovery, a compact workflow, optional `references/`, and small executable `scripts/`. Runtime scripts use the Python standard library where practical. The current repository does not require an LLM-provider SDK. Live search and downloads are performed through capabilities available to the host agent and user's lawful access; the Skill declares source-selection logic but does not bundle subscriptions or credentials.

## External design review

The layout borrows engineering patterns, not text, from established research-skill repositories: progressive disclosure and portable skill folders; CI validation of frontmatter and structure; narrow scripts with tests; explicit integrity gates; install-by-copy portability; and repository-level citation and contribution policy. See `docs/open-source-patterns.md` for sources and tradeoffs.
