# Independent forward test — 2026-09-17

Three independent read-only evaluators exercised the installed instructions without being given intended answers.

## Scenarios

1. End-to-end SCI design on urbanization and East Asian extreme precipitation.
2. Comparison of two 10-day ensemble precipitation forecasts over China.
3. Satellite AOD validation against AERONET.

## Defects observed and resolved

- Added an explicit stage-Skill plus topic-Skill composition rule.
- Added scope freezing, current-literature cutoff, priority-paper selection, saturation/stopping, study-comparison, bibliography, and gap-to-design handoff requirements.
- Added design-only output labels so planned analyses cannot read like completed results.
- Added land-use exposure/counterfactual, mechanism-separation, network-change, data-access, and coverage checks.
- Expanded statistical Skill discovery metadata with forecast, ensemble, CRPS, Brier, reliability, and lead-time terms.
- Expanded forecast verification for zero-inflated precipitation, fair CRPS, CRPSS, ranks/PIT, rare-event reliability, paired blocked inference, multiplicity, common masks/grids, ensemble genealogy, postprocessing leakage, and baselines.
- Expanded AOD validation for product/network versions, QA decoding, wavelength interpolation, matchup algorithms, representativeness diagnostics, expected-error reporting, reference uncertainty, clustering, site-held-out testing, stratification, selection bias, and calibration independence.
- Updated routing fixtures so validation design composes research design, data QC, and statistics, while extreme-precipitation research also invokes the extremes specialist.

## Remaining interpretation boundary

The deterministic routing cases document expected composition and verify complete coverage; they do not measure an agent runtime's automatic routing accuracy. The independent forward tests provide qualitative behavior evidence, not expert-scored scientific accuracy. Expert review and prospective user tasks remain required for performance claims.
