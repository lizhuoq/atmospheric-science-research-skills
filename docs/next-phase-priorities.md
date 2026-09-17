# Next-phase priorities

1. **Complete the prepared expert queues.** Review `reports/taxonomy-review-queue.csv` and `reports/evidence-review-queue.csv`, then run the supplied scorer. Software must not self-certify these human gates.
2. **Build evidence extraction on training papers only.** Start with 60–100 papers spanning study designs and themes. Require page/section/figure/table locators and dual review for reusable rules.
3. **Create the behavioral evaluation harness.** Implement the nine required adversarial cases and claim-level scoring before adding more Skills.
4. **Calibrate forecast/model evaluation.** The Skill is implemented; next collect expert-scored realistic outputs involving lead time, initialization, ensembles, baselines, verification data, resolution, and dependence.
5. **Calibrate observation/retrieval validation.** The Skill is implemented; next collect expert-scored cases for calibration, collocation, representativeness, quality flags, and retrieval assumptions.
6. **Develop composition/air-quality synthesis.** Combine chemistry, aerosol, and exposure foundations while separating mechanistic atmospheric inference from epidemiological causality.
7. **Repair or quarantine parse failures.** Handle the one observed malformed PDF and define a rendering/OCR fallback without committing derived full text.
8. **Add CI after repository initialization.** Run unit tests, generated-output checks, Skill frontmatter validation, and publication-safety checks on every pull request.

Do not add new topic Skills until priorities 1–3 have acceptance results and the demonstration Skill has been tested by domain experts.
