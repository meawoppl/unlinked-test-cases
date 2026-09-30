# Unlinked test cases

Compatibility corpus for the Unlinked model importer, renderer, simulator, and MATLAB/Octave transpiler. The repository is `meawoppl/unlinked-test-cases` (referred to as “simulink-test-cases” in the project brief).

## Included fixtures

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

`verify` checks every fixture, license, and numerical oracle, and rejects unlisted model/source files. `refresh` fetches only manifest-pinned upstream files, checks their hashes before writing, and then verifies everything. It does not update revisions or silently accept changed bytes. Neither command executes imported MATLAB code, model callbacks, or simulations.

To add fixtures, record the exact source commit and file URL, preserve the applicable license verbatim, audit file-level provenance, and add hashes and coverage metadata. Review licensing and new baselines before accepting them. Any outputs from a real MATLAB/Octave/Simulink run must record tool version, configuration, tolerances, and how the run was made.

## License and provenance

Repository-authored material and synthetic fixtures are MIT licensed under `LICENSE`. Upstream material remains under its original MIT notices in `licenses/`; the manifest maps each fixture to its notice. Files are copied byte-for-byte, without executing them. No proprietary runtime or toolbox is bundled.

Deliberately excluded: MathWorks-hosted examples with MathWorks-only license conditions, and parser demonstration MDLs with unclear model-level provenance. A permissive license on a parser alone does not establish permission to redistribute every bundled model. Consequently the initial MDL corpus is synthetic, while the SLX corpus contains existing third-party projects.

This is an initial compatibility corpus, not a comprehensive conformance suite. Expand with independently licensed legacy MDL projects, split-system SLX archives, branches, masks, model references, buses, discrete rates, and independently established numerical references.
