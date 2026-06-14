## Creation

- Tests run with a single command. Discover it from `README`, `package.json`, `Cargo.toml`, or other build configuration.
- Every new function gets a test. Bug fixes get a regression test.
- Mock external I/O (API, DB, filesystem) with named fake classes, not inline stubs.
- Tests must be F.I.R.S.T: fast, independent, repeatable, self-validating, timely.

## Guidelines

- Preserve existing tests. Update tests when behavior changes. Do not silently change tested behavior.
- Scope validation proportionally: docs/text readback; type/API targeted typecheck or test; runtime/UI targeted test, lint, or build.
- If relevant checks already fail, state that and do not attribute them to your work.
- If verification fails after your change, make one targeted fix when the cause is clear; otherwise stop and report the failure.
- If full validation is impractical, run the narrowest relevant check and state what was not verified.
