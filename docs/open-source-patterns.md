# Open-source research Skill patterns reviewed

Review date: 2026-09-16. Star counts are volatile snapshots used only to select mature examples; popularity is not evidence of scientific validity.

## Repositories reviewed

- [ai-science-toolkit](https://github.com/dgilford/ai-science-toolkit) — atmospheric/climate research toolkit with task-specific skills and adversarial domain reviewers. Useful patterns: separate literature, figure, statistics, attribution, and meteorological review responsibilities; document platform support, per-skill configuration, graceful degradation, and invocation control.
- [weather-skills](https://github.com/rhiza-research/weather-skills) — composable weather/climate data pipelines. Useful patterns: source-specific fetchers separated from generic operators, a shared dataset/provenance contract, explicit credentials, reproducible manifests, and natural-language composition. Its own warning that smoke tests are not scientific validation is retained as an important boundary.
- [nature-reviewer-skills](https://github.com/GeoGeekLab/nature-reviewer-skills) — domain-routed Earth-system review suite. Useful patterns: claim-to-evidence stress-test gates, abstracted reasoning rather than copied content, deterministic retrieval, evidence anchoring, defensive document limits, and explicit distinction between software benchmarks and expert scientific validation.

- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — high-adoption human-in-the-loop research pipeline. Useful patterns: explicit integrity gates, evidence anchors, provenance, evaluation assets, risk/security documentation, and stated limits of verification.
- [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) — large research-engineering skill curriculum. Useful pattern: capability-oriented modularity. Risk to avoid: allowing breadth to outrun domain validation.
- [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) — broad scientific tool/database Skill collection. Useful patterns: portable skill folders, discovery metadata, references, scripts, examples, and cross-agent compatibility.
- [nature-skills](https://github.com/Yuan1z0825/nature-skills) — focused writing/figure suite. Useful pattern: a small set of cohesive deliverables rather than one Skill per scientific noun.
- [ai4s-skills](https://github.com/ai4s-research/ai4s-skills) — smaller AI-for-science suite. Useful patterns: `SKILL.md` plus progressive references/tools, structure validation in CI, single-purpose dependencies, tests, citation metadata, and install-by-copy portability.
- [awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) — comparative catalog used to identify suites and inspect license/tooling risks.

## Adopted decisions

- Progressive disclosure: short entrypoint, focused references, deterministic helper scripts.
- Human review gates for scientific judgment; validators enforce structure, not truth.
- Claim-level evidence locators and provenance rather than citation lists alone.
- Tests and publication-safety checks from the first Skill.
- Domain-driven Skill boundaries after coverage analysis, not one Skill per taxonomy label.
- Provider-neutral scripts with no OpenAI/Anthropic SDK dependency.
- Live retrieval as a source-routing layer: discovery, identity verification, full-text acquisition, reading, and evidence extraction are distinct stages with access/status provenance.
- Example corpora are fixtures and evaluation assets, never a closed-world runtime knowledge base.

## Deliberately not adopted

- Autonomous paper production as the default outcome.
- Large monolithic prompts or hundreds of thin overlapping Skills.
- Popularity, journal prestige, or citation count as evidence-strength scores.
- Hooks, broad shell permissions, external accounts, or network dependencies for the milestone-1 Skill.
- Copying instructions or scientific content from other repositories; only general engineering patterns were used.
