# Testing Guidelines

- Preserve existing tests. Update tests when behavior changes. Do not silently change tested behavior.
- Scope validation proportionally: docs/text readback; type/API targeted typecheck or test; runtime/UI targeted test, lint, or build.
- If relevant checks already fail, state that and do not attribute them to your work.
- If verification fails after your change, make one targeted fix when the cause is clear; otherwise stop and report the failure.
- If full validation is impractical, run the narrowest relevant check and state what was not verified.