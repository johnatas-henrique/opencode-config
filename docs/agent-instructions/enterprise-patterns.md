# Enterprise Patterns

<!-- [SECURITY] MANDATORY -->
NEVER: Commit .env, secrets, tokens, credentials
NEVER: Expose API keys, passwords, PII in code
MANDATORY: Audit trail comments for financial/auth paths
<!-- [/SECURITY] -->

<!-- [ERRORS] MANDATORY -->
NEVER: Use `any` type
NEVER: Swallow exceptions without logging
MANDATORY: Typed errors, Result types where appropriate
<!-- [/ERRORS] -->

<!-- [LOGS] MANDATORY -->
NEVER: Log secrets or PII
MANDATORY: Structured JSON logs, correlation IDs
MANDATORY: Traceable transactions in banking systems
<!-- [/LOGS] -->

<!-- [CODE] MANDATORY -->
MANDATORY: strict: true in TypeScript
MANDATORY: Self-explanatory code (no comments needed)
MINIMUM: Code that solves the problem only
<!-- [/CODE] -->
