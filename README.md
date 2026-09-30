# Unlinked test cases

Compatibility corpus for the Unlinked model importer, renderer, simulator, and MATLAB/Octave transpiler. The repository is `meawoppl/unlinked-test-cases` (referred to as “simulink-test-cases” in the project brief).

## Included fixtures

The corpus now contains **30 existing models** (28 SLX, 2 legacy MDL) from nine upstream projects, plus nine MATLAB source files and one synthetic numerical fixture. SLX metadata spans 13 releases from R2014a through R2026a; 12 archives use split-system storage.

- Drone telemetry/calibration and model references (ARDrone), MAVLink buses and S-functions, wind-turbine controllers (DISCON), inverted pendulum control, flight software (SPAARO), and diagram-layout cases (McSCert).
- Robotology iCub firmware models cover force/torque calibration, Kalman filtering, spherical-wrist geometry, CAN messages, thermal dynamics, field-oriented motor control, minimum-jerk planning, and Stateflow supervision.
- Existing legacy MDL inputs are McSCert `AutoLayoutDemo` (format version 7.8) and Jed Frey `discrete_tf` (format version 8.6). Format numbers are preserved separately from producer release metadata.

- Three existing R2017a SLX underwater-vehicle models from [enricoande/uuv](https://github.com/enricoande/uuv), plus two matrix utility functions. Models contain nested systems, routing, math blocks, and Stateflow. They are useful rendering/import coverage; their simulations need additional workspace data and unsupported features.
- Seven existing MATLAB algorithms from [TheAlgorithms/MATLAB-Octave](https://github.com/TheAlgorithms/MATLAB-Octave), exercising functions, loops, conditionals, indexing, and array operations. These are syntax coverage inputs, not a claim that all already transpile.
- One explicitly **synthetic** legacy MDL flow: Constant(2) → Gain(3) → Sum(+4) → Integrator(initial 1) → Outport. Its independent analytic oracle is `y(t)=1+10t` for `0≤t≤1`. This fixture has not been saved or validated by MATLAB/Simulink. The legacy format version field is scaffolding and does not establish compatibility.

`manifest.json` records immutable upstream commit IDs, original paths, source/download URLs, byte SHA-256s, license files, release metadata, extracted block counts/types, and the provenance of any expected output. A null expected output means no numerical oracle is available. Counts are extracted from all `simulink/*.xml` members, including nested block definitions; line counts count XML `Line` elements rather than flattened connections.

## Integrity and refresh

Python 3.9+ with the standard library is sufficient:

```sh
python3 scripts/corpus.py verify
python3 scripts/corpus.py refresh
```

`verify` checks every fixture, license, and numerical oracle, and preserved provenance READMEs, and rejects unlisted model/source files. Each resource is capped at 16 MiB and the corpus at 128 MiB; refresh allows only HTTPS raw GitHub resource URLs. `refresh` fetches only manifest-pinned upstream files, checks their hashes before writing, and then verifies everything. It does not update revisions or silently accept changed bytes. Neither command executes imported MATLAB code, model callbacks, or simulations.

To add fixtures, record the exact source commit and file URL, preserve the applicable license verbatim, audit file-level provenance, and add hashes and coverage metadata. Review licensing and new baselines before accepting them. Any outputs from a real MATLAB/Octave/Simulink run must record tool version, configuration, tolerances, and how the run was made.

## License and provenance

Repository-authored material and synthetic fixtures are MIT licensed under `LICENSE`. Upstream material remains under its original MIT or BSD-3-Clause notices in `licenses/`; the manifest maps each fixture to its notice. Files are copied byte-for-byte, without executing them. No proprietary runtime or toolbox is bundled.

Deliberately excluded: MathWorks-hosted examples with MathWorks-only license conditions, and parser demonstration MDLs with unclear model-level provenance. A permissive license on a parser alone does not establish permission to redistribute every bundled model. Also excluded: Python-Simulink bouncing-ball models explicitly adapted from a MathWorks example, and disturbanceFittingSimulink trajectory code whose nested license limits use to MathWorks products. ARDrone is included because its actual license is unrestricted BSD-3-Clause, despite the MathWorks copyright holder. DISCON imports are limited to the TU Delft 64-bit models; the separately credited 32-bit controller is excluded. See `provenance/` for byte-preserved upstream descriptions.

This is an initial compatibility corpus, not a comprehensive conformance suite. Expand further with older MDL 5/6 formats and independently established numerical references. Existing models have not been executed, and corpus presence does not imply all features are supported by the current importer or simulator.
