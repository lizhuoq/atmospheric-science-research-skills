# Measurement and retrieval chain

Record instrument/platform, channel/wavelength/frequency, scan geometry, footprint, calibration lineage, noise/detection limit, saturation, sampling, geolocation, retrieval version, forward model, priors, ancillary inputs, averaging kernel/sensitivity, quality flags, and known failure regimes.

Separate uncertainty components where possible: calibration, random instrument noise, forward-model error, ancillary-input error, smoothing, sampling/representativeness, algorithm structural uncertainty, and reference uncertainty. Total uncertainty must not be formed by quadrature unless independence and scale assumptions are justified.

## Aerosol optical depth against sun photometers

For AOD validation, record the satellite collection/product/version, retrieval family, wavelength, native footprint, overpass geometry, surface algorithm, cloud mask, and every decoded QA bit or summary-QA threshold. Record the sun-photometer network version, processing level, direct-sun product, wavelength, calibration status, cloud-screening/triplet-stability processing, and uncertainty model. Do not call the ground product error-free.

Match wavelengths directly when possible. Otherwise document interpolation/extrapolation, the Angstrom-exponent source and interval, spectral-curvature assumption, and propagated uncertainty. Test sensitivity to QA thresholds and product-version transitions. Keep retrieval success/failure as an analyzable outcome because cloud, surface brightness, loading, geometry, and aerosol type can make the validation sample selective.

Separate validation from calibration/tuning sites and periods. Report whether ancillary data, priors, or ground observations enter both the retrieval and reference chain and could correlate errors.
