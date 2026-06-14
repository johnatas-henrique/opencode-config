# Monkey-patch: mnemory plugin — session ID template interpolation

**Date:** 2026-06-14
**Author:** build agent
**Reason:** OpenCode server bug — session template `{id}` is not interpolated and arrives URL-encoded as `%7Bid%7D` in event properties. This causes:

```
ERROR: Expected a string starting with "ses", got "%7Bid%7D"
```

(visible in TUI as a minified JS error at hooks.ts:240)

## Root Cause

OpenCode's server fails to replace the `{id}` template in session URLs. The mnemory plugin receives `props.sessionID = "%7Bid%7D"` (URL-encoded `{id}`) in `session.idle`, `session.compacted`, and `session.created` events. When it passes this to the SDK `session.messages()` call, the SDK validates the session ID and throws:

```
Expected a string starting with "ses", got "%7Bid%7D"
```

Before v1.17.4, this error was silently logged. Since v1.17.4, plugin hook errors are surfaced in the TUI, making the flicker visible.

## Upstream Issues

- [anomalyco/opencode#29868](https://github.com/anomalyco/opencode/issues/29868) — TUI hangs in infinite render loop
- [anomalyco/opencode#31145](https://github.com/anomalyco/opencode/issues/31145) — Session routes throw ParseError
- [anomalyco/opencode#28486](https://github.com/anomalyco/opencode/issues/28486) — Historical sessions disappear
- [anomalyco/opencode#29262](https://github.com/anomalyco/opencode/issues/29262) — TUI shows error on `--continue --fork`

All still OPEN, no upstream fix merged.

## Fix Applied

**Plugin moved to local directory:** `~/.config/opencode/plugins/opencode-mnemory/`
**Reference in `opencode.jsonc`:** `"~/.config/opencode/plugins/opencode-mnemory"`

Three guards added to reject un-interpolated session IDs before making SDK calls:

### 1. `session.created` handler (line 196)

```typescript
// Before:
const sessionId = props?.sessionID ?? props?.info?.id;
if (!sessionId) return;

// After:
const sessionId = props?.sessionID ?? props?.info?.id;
// Reject un-interpolated template (%7Bid%7D = URL-encoded {id}) or invalid session IDs.
// Workaround for OpenCode server bug where the session template {id} is not interpolated.
if (!sessionId || sessionId.startsWith('ses_') === false) return;
```

### 2. `session.idle` handler (line 219)

```typescript
// Before:
if (!sessionId) return;

// After:
if (!sessionId || sessionId.startsWith('ses_') === false) return;
```

### 3. `session.compacted` handler (line 306)

```typescript
// Before:
if (!sessionId) return;

// After:
if (!sessionId || sessionId.startsWith('ses_') === false) return;
```

The check `sessionId.startsWith('ses_') === false` matches the SDK's own session ID validation (the error message says "Expected a string starting with 'ses'"). This catches `%7Bid%7D`, `{id}`, empty strings, or any other malformed template that isn't a real session ID.

## Impact

- `session.created`: skips init recall and state creation when session ID is invalid (prevents zombie state in Map)
- `session.idle`: skips memory extraction when session ID is invalid
- `session.compacted`: skips message count preservation when session ID is invalid
- All other handlers (`chat.message`, `system.transform`) are unaffected — they receive session IDs from tool inputs (which are correct)

## Updating the plugin

When a new version of `@fpytloun/opencode-mnemory` is released:

```bash
# 1. Download the new version to a temp directory
mkdir /tmp/mnemory-update && cd /tmp/mnemory-update
npm pack @fpytloun/opencode-mnemory
tar xzf *.tgz

# 2. Copy the new files to the local plugin directory
cp package/node_modules/@fpytloun/opencode-mnemory/{hooks.ts,client.ts,helpers.ts,index.ts,tools.ts,package.json} \
  ~/.config/opencode/plugins/opencode-mnemory/

# 3. Re-apply the guards (search for "if (!sessionId) return;" and add ses_ check)
# Or re-apply this patch manually as documented above.

# 4. Restart OpenCode
```

## How to redo if reverted

```bash
# Open the target file
$EDITOR ~/.config/opencode/plugins/opencode-mnemory/hooks.ts

# Find all occurrences of:
if (!sessionId) return;
# → replace with:
if (!sessionId || sessionId.startsWith('ses_') === false) return;
```

Or use sed:

```bash
sed -i 's/if (!sessionId) return;/if (!sessionId || sessionId.startsWith('\''ses_'\'') === false) return;/' \
  ~/.config/opencode/plugins/opencode-mnemory/hooks.ts
```
