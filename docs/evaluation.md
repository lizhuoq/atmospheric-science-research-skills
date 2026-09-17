# Evaluation plan

## Complete-suite routing contract

`tests/skill_routing_cases.json` contains 15 representative requests spanning all 13 Skills, including composed SCI, forecast-verification, and retrieval-validation workflows. `scripts/validate_skill_suite.py` verifies complete Skill inventory, discovery metadata, workflow/quality-gate/example structure, orchestrator discoverability, and routing-case coverage. These deterministic checks validate packaging and declared behavior only; they are not evidence that an LLM will always route correctly or perform expert-level science.

## Levels

1. **Structural tests** validate generated artifacts, split completeness/disjointness, evidence records, leakage policy, query output, and publication safety.
2. **Scientific workflow cases** score question framing, evidence typing, source localization, unit/scale checks, uncertainty, conflict handling, and refusal to overclaim.
3. **Blind generalization** uses only `blind_test` papers after the Skill and rubric are frozen. No blind-test result may be promoted into the same version's rules.

## Required cases

The evaluation set must include a normal synthesis; incomplete input; a cross-subfield question; genuinely conflicting studies; an invalid DOI; a causal-overreach request; incompatible units or temporal aggregation; a request for long copyrighted text; and a prompt likely to induce citation hallucination.

## Metrics

- scientific accuracy;
- evidence traceability and locator correctness;
- citation/DOI accuracy;
- workflow completeness;
- uncertainty calibration;
- subfield appropriateness;
- unsupported-claim and hallucinated-citation rate;
- blind-test generalization.

Use a claim-level scoring sheet. A claim is supported only when the cited source and locator entail it within stated scope. Report denominators and confidence intervals where sample size permits. Human atmospheric-science review is mandatory for causal claims, numerical conclusions, contested mechanisms, and high-stakes exposure or hazard interpretations.

## Milestone-1 automated checks

```powershell
python -m unittest discover -s tests -v
python scripts/build_milestone1.py --check
python scripts/check_publication_safety.py
```

The automated suite includes engineering, distribution-isolation, leakage, evidence-status, and structured behavioral-policy gates. `tests/evaluation_cases.json` freezes the nine required behavioral scenarios; `scripts/run_behavioral_eval.py` executes their deterministic decision-coverage check. This is not an LLM accuracy or expert scientific benchmark. Blind entity-extractor reach is reported separately and never flows back into the current rule library.
