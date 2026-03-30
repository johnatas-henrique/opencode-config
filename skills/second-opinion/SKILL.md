---
name: second-opnion
description: "Seek external AI perspective on complex decisions. Use when: (1) stuck after 3+ failed attempts, (2) architectural trade-offs unclear, (3) need validation on high-stakes choices, (4) domain mismatch detected, (5) approaching problem wrong way. Keywords: decision, complex, stuck, architecture, trade-off, opinion, perspective, verify."
---

# Second Opinion

## When to Seek

**MUST seek second opinion when:**
- After 3+ failed attempts on same problem
- Architectural decision with multiple valid approaches
- High-stakes choice with irreversible consequences
- Detecting domain mismatch (working outside expertise)
- Gut says "something is wrong" but can't identify

**NEVER seek for:**
- Simple tasks Claude can solve directly
- Before attempting self-resolution
- As authority to bypass own judgment

## The Process

1. **Formulate the Question**
   - What specific decision needs addressing?
   - What options have you considered?
   - What makes this complex?

2. **Present Context**
   - What have you tried?
   - What constraints exist?
   - What's the risk of each choice?

3. **Evaluate the Response**
   - Does it address your specific question?
   - Does it align with your constraints?
   - Use as input, not authority

## Anti-Patterns

**NEVER:**
- Use without first attempting self-resolution
- Treat second opinion as final authority
- Ask vague "what should I do?" questions
- Seek for simple tasks (wastes resources)
- Ignore domain expertise in your original reasoning

## Invocation

```
opencode run "<your question>" -m opencode/big-pickle
```

**Tip:** Be specific. "I'm choosing between A and B because X, Y, Z" works better than "help me".
