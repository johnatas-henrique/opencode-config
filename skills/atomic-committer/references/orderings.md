# Dependency Ordering

Load this file when ordering commits in Phase 1D. Read only the section that matches your project type. Commits that other commits depend on go first.

## Backend

```
Level 0: Utilities, constants, type definitions
Level 1: Models, schemas, interfaces
Level 2: Services, business logic
Level 3: API endpoints, controllers
Level 4: Config, infrastructure
```

## Frontend

```
Level 0: Types, constants, theme tokens
Level 1: Hooks, utilities, context providers
Level 2: Components (atomic → composite)
Level 3: Pages, routes, layouts
Level 4: Config, build, CI
```

## Monorepo

```
Level 0: Shared libs, design system
Level 1: Internal packages
Level 2: Applications
Level 3: Root config, CI, scripts
```

## When the project doesn't match any template

Apply the principle: **foundations before dependents.** Sort by:
1. Definitions and types (nothing imports them, they import nothing)
2. Low-level utilities (pure functions, helpers)
3. Business logic (services, hooks, state)
4. Presentation (components, pages, routes)
5. Infrastructure (config, CI, deployment)
