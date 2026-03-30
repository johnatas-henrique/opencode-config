---
name: git-release
description: "Create semantic versioning releases with changelogs. Use when: (1) preparing tagged release (v1.x.x), (2) generating release notes from merged PRs, (3) deciding version bump type (major/minor/patch), (4) creating GitHub release. Keywords: semantic versioning, changelog, release notes, conventional commits, version bump, gh release."
---

# Git Release Process

## The Iron Rule

```
NO RELEASE WITHOUT VERSION ANALYSIS FIRST
```

Determine bump type BEFORE writing release notes.

## Decision Tree: Version Bump

| If commits contain... | Then bump... | Unless... |
|----------------------|--------------|-----------|
| `BREAKING CHANGE:` in body/footer | **MAJOR** | - |
| `feat:` | **MINOR** | Already covers feat |
| `fix:` | **PATCH** | - |
| Only `docs:`, `style:`, `refactor:` | **PATCH** | Version unchanged if no code change |
| `perf:`, `test:` | **PATCH** | - |

**Edge cases requiring MAJOR even without breaking change:**
- Dependency update that drops Node <X version
- API deprecation (even if not breaking yet)
- Security hardening that breaks old clients

## When NOT to Release

**NEVER create release if:**
- Commits don't follow conventional commits format (unparseable)
- Unreleased commits are only internal/chore (waste of release)
- CI/CD pipeline not passing on main branch
- Release would be identical to previous tag (check first)

**SKIP version bump if:**
- Changes are 100% documentation only
- Changes are CI/internal tooling only
- Package version already reflects changes

## Workflow

1. **Verify release is warranted**
   ```bash
   # Check commits since last tag
   git log $(git describe --tags --abbrev=0)..HEAD --oneline
   ```
   If only internal commits → ask human if release needed.

2. **Determine bump type** (see Decision Tree)

3. **Check conventional commit compliance**
   ```bash
   # Validate commit format
   git log --format="%s" | grep -E "^(feat|fix|docs|perf|refactor|test|chore|build|ci|style|revert):" || echo "WARNING: Non-conforming commits found"
   ```

4. **Generate grouped release notes**
   - **Features** (`feat:`)
   - **Fixes** (`fix:`)
   - **Performance** (`perf:`)
   - **Documentation** (`docs:`)
   - **Refactoring** (`refactor:` - if notable)
   - **Internal** (`chore:`, `build:`, `ci:` - minimize or skip)

5. **Create release**
   ```bash
   gh release create v1.2.3 --title "v1.2.3" --notes-file RELEASE_NOTES.md
   ```

## Anti-Patterns

**NEVER:**
- Bump major for new feature without breaking change (violates semver)
- Include every single commit (noise, use PR scope)
- Skip checking if changes warrant release at all
- Use non-conventional commit format without validating
- Create release from non-main branch

## Release Notes Template

```markdown
## What's Changed

### ✨ Features
- feat: description (#PR)

### 🐛 Fixes
- fix: description (#PR)

### 📚 Documentation
- docs: description (#PR)

### ♻️ Refactoring
- refactor: description (#PR)

**Full Changelog**: https://github.com/org/repo/compare/v1.2.2...v1.2.3
```

## Fallback: No Conventional Commits

If commits don't follow format:
1. Ask human to categorize changes
2. Or use `git diff --stat` to infer impact
3. Document in release notes as "Various improvements"
