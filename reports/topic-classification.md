# Data-driven topic classification — milestone 1

The baseline classifier uses titles plus OpenAlex topics and supports multiple labels per paper. It evaluated every requested candidate direction without forcing a one-to-one Skill mapping. Counts overlap and therefore do not sum to 3,000.

| Candidate theme | Papers | Local full text | Assessment |
|---|---:|---:|---|
| Climate variability and change | 1,538 | 589 | strong, broad; split by task rather than make one giant domain Skill |
| Dynamics and weather systems | 1,322 | 515 | strong, overlaps forecasting/extremes |
| Atmospheric chemistry | 746 | 295 | strong; combine shared composition evidence rules |
| Cloud, precipitation, microphysics | 728 | 235 | strong |
| Observations and instruments | 726 | 272 | strong; distinct validation workflow |
| Aerosols | 723 | 255 | strong, tightly coupled to chemistry and air quality |
| Air quality and exposure | 478 | 129 | adequate; health causality needs special review |
| Forecasting and predictability | 459 | 144 | adequate; combine NWP/verification workflow |
| Extremes | 405 | 122 | adequate; attribution is a distinct high-risk mode |
| Hydrometeorology | 394 | 125 | adequate, overlaps precipitation/land |
| Land–atmosphere interaction | 341 | 97 | adequate |
| Remote sensing and retrieval | 339 | 117 | adequate; combine with instrument validation where possible |
| Earth-system models | 154 | 80 | moderate, high full-text fraction |
| Statistics, causal inference, ML | 142 | 51 | moderate; cross-cutting methods reference first |
| Quality control and uncertainty | 136 | 68 | cross-cutting, not a standalone subfield Skill initially |
| Ocean–atmosphere interaction | 127 | 53 | moderate |
| Model evaluation, correction, downscaling | 96 | 41 | moderate but task-distinct |
| Atmospheric radiation | 83 | 28 | thin for a standalone Skill |
| Boundary layer and turbulence | 78 | 21 | thin; targeted expert review required |
| Numerical weather prediction | 67 | 20 | keyword under-detection; merge with forecasting initially |
| Paleoclimate | 37 | 30 | small but unusually high full-text coverage; defer dedicated Skill |
| Research integrity and writing | 1 | 1 | corpus is not suitable as its evidence base; use authoritative guidance |
| Unclassified | 81 | 33 | manual taxonomy review queue |

## Method signals

Numerical modeling appears in 1,715 records, observation in 664, remote sensing in 335, review/synthesis in 284, statistical/ML in 122, and reanalysis in 64. Another 813 have no method keyword signal in title/topic metadata. These are conservative lexical signals, not study-design labels.

## Recommended Skill architecture

The initial cross-cutting demonstrator was later renamed and reduced to the lightweight `atmospheric-science-research` orchestrator. The suite uses task-distinct Skills rather than 22 topic wrappers:

1. forecast/model evaluation and predictability;
2. observation/retrieval/instrument validation;
3. atmospheric composition and air-quality synthesis;
4. extremes detection and attribution;
5. manuscript claim and scientific-review audit.

Radiation, boundary-layer turbulence, paleoclimate, and NWP require taxonomy refinement or targeted expert curation before a dedicated release. Research integrity/writing must be grounded mainly in authoritative external standards because the local atmospheric corpus does not cover it.

## Limitations

The classifier is an auditable baseline, not a scientific ontology. Lexical matches over-label generic terms and under-label studies whose method is absent from title/topic metadata. Counts guide architecture and sampling only; they must not be used as prevalence estimates. Manual review and a supervised multi-label model trained only on the training split are appropriate next steps.
