# Safety & Git Guidelines

## Safety & Infrastructure

- Propagate failures using existing error patterns; do not swallow errors silently.
- Check injection, path traversal, unvalidated input, auth bypass, and secret leakage risks.
- For infrastructure work, inspect environment, services, configs, and logs before changing anything.
- Validate config before reload or restart; prefer reload when safe.
- Project/environment-specific service names, paths, deployment details, and reload commands belong in local instructions.

## Git & PRs

- Commit only when explicitly requested.
- Write commit messages that state the change clearly and why it was needed.
- Keep PRs small and scoped to one concern.
- Do not force-push to main/master.
- Do not use `--no-verify` or `--no-gpg-sign`.