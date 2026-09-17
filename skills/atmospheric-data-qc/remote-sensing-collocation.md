# Collocation and comparison

Predeclare spatial, temporal, vertical, angular, and regime matching. Report the initial population, exclusions by each filter, final matchup count, and repeated observations per site/event.

Check:

- point versus footprint or grid-cell support;
- instantaneous overpass versus averaging/accumulation interval;
- pressure/height/model levels and vertical smoothing;
- cloud, precipitation, aerosol, surface emissivity/albedo, terrain, and illumination;
- parallax, geolocation, scan angle, and orbital sampling;
- shared model/ancillary inputs that can create correlated errors;
- independence of calibration and validation samples.

Use paired samples for algorithm comparisons. Preserve failure-to-retrieve as an outcome rather than silently dropping it when retrieval availability matters.

## Operational AOD matchup design

Predeclare whether the satellite sample is the containing pixel, nearest valid pixel, or an aggregation within a radius. Define temporal half-window, minimum number of ground observations, aggregation statistic, minimum satellite pixel count, duplicate-overpass handling, and whether multiple pixels/overpasses per site-day are separate cases. Keep an attrition table for each QA and matchup rule.

Diagnose representativeness using within-window satellite spatial variability, ground temporal variability, distance/time offsets, and sensitivity across several defensible radii and windows. Avoid selecting the best window after seeing validation scores.

At minimum report matchup count, number of sites and overpasses, bias and median bias, MAE, RMSE, correlation with caveats, and a declared regression method. Where the satellite product defines an expected-error envelope, report the fraction within/above/below it without treating the envelope as ground truth. Examine heteroscedasticity and low-AOD relative-error behavior; consider errors-in-variables when reference uncertainty matters.

Cluster inference by site and/or overpass as appropriate, and use site-held-out or region-held-out analysis when claiming geographic transfer. Stratify only with adequate sample size by land/ocean or surface brightness, aerosol type/loading, season, viewing/solar geometry, cloud adjacency, elevation/terrain, and region. Report retrieval availability as well as conditional accuracy to expose selection bias.
