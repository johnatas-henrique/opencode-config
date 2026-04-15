# Enterprise Patterns

## Overview

Guidelines for banking/enterprise projects. Use these patterns when working on financial systems, auth, or production code.

## Security & Compliance

- **NEVER commit .env files, secrets, tokens, credentials** of any kind
- Never expose API keys, passwords, or sensitive data in code
- For banking/enterprise projects: add audit trail comments when modifying financial/auth paths
- Use secret scanning before commit when available

## Error Handling

- Always use typed errors, never `any`
- Never swallow exceptions without logging
- For financial/auth systems: add audit trail comments
- Use Result types where appropriate (Go, Rust, etc.)

## Production Logging

- Structured JSON logs for production systems
- Include correlation IDs for traceability
- **Never log secrets or PII** (personally identifiable information)

## Observability

- Add metrics endpoints for critical paths
- Include health check endpoints
- For banking systems: ensure all transactions are traceable

## Code Standards

- Always use `strict: true` in TypeScript/configs
- Minimum code that solves the problem
- No speculative abstractions
- Code must be self-explanatory without comments