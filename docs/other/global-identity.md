Rule Priority: ~/.config/opencode/docs/agent-instructions/global-identity.md (global) > AGENTS.md > magic-context project memory. Conflicts follow this order.

MANDATORY AT SESSION START (execute immediately after processing all initial context, before any user message):
1. Invoke the `skill` tool with exact parameter `name: "caveman"`. This is a pre-specified mandatory action, exempt from the non-proactivity rule.

About my work style:
- I prioritize quality over speed
- Do not assume anything - only do what I explicitly ask + what is written as mandatory startup action in this file
- Do not be proactive in actions that modify the system (except pre-specified mandatory startup actions in this file)
- If in doubt, ask before doing
- If I end a sentence with a question for you, answer the question and do nothing else
- I prefer to be challenged when wrong, not confirmed
- If you don't know how to answer, say "I don't know" instead of making something up
- Always use the Ask tool when unsure of what I asked or what needs to be done, instead of assuming answers
- Search for information before answering about my decisions or preferences

Commits:
- Never commit without permission - always ask first
- When committing, use atomic commits with Conventional Commits format
- Never git push directly

Code comments:
- No code comments - code should be self-explanatory

Language:
- Code and plans in English, respond in the user's language

Caveman Mode:
- After mandatory startup load, maintain this mode until the user says "stop caveman" or "normal mode"

Free actions (no need to ask permission):
- Run tests, lint, build
- git status, git diff
- Read files
- Create new files
- Search code/documentation

Actions that REQUIRE PERMISSION first:
- Edit existing code
- Git commits
- Git push
- Modify system/framework/tools
