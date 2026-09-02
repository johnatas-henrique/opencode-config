#!/usr/bin/env python3
"""
opencode-optimizer analyze.py

Helper script for the opencode-optimizer skill.
Scans global config, global skills, and the current project,
then outputs a structured JSON report for the agent to consume.

Usage:
    python3 analyze.py [--project-dir /path/to/project]

Output: JSON to stdout.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────
GLOBAL_CONFIG = Path.home() / ".config" / "opencode" / "opencode.jsonc"
GLOBAL_SKILLS_DIR = Path.home() / ".agents" / "skills"


def read_jsonc(path: Path) -> dict:
    """Read a JSONC file (strip JS-style comments, control chars, trailing commas)."""
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")

    # strip single-line comments (only outside strings — simple heuristic)
    lines = raw.split("\n")
    clean_lines = []
    for line in lines:
        in_string = False
        escape = False
        out = []
        for ch in line:
            if escape:
                out.append(ch)
                escape = False
            elif ch == "\\" and in_string:
                out.append(ch)
                escape = True
            elif ch == '"' and not escape:
                in_string = not in_string
                out.append(ch)
            elif ch == "/" and not in_string and len(out) >= 1 and out[-1] == "/":
                out.pop()
                break
            else:
                out.append(ch)
        clean_lines.append("".join(out))
    raw = "\n".join(clean_lines)

    # strip multi-line comments
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)

    # strip trailing commas before ] or }
    raw = re.sub(r",\s*([}\]])", r"\1", raw)

    # escape literal control characters inside strings
    def _escape_control(m):
        ch = m.group(0)
        if ch == "\n":
            return "\\n"
        if ch == "\r":
            return "\\r"
        if ch == "\t":
            return "\\t"
        return f"\\u{ord(ch):04x}"

    raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', _escape_control, raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Warning: failed to parse {path}: {e}", file=sys.stderr)
        return {}


def read_skill_info(skill_dir: Path) -> dict | None:
    """Read SKILL.md in a skill directory, extract name and description from front matter."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding="utf-8")

    name = skill_dir.name
    description = ""

    # Parse YAML front matter (between --- markers)
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if m:
        front = m.group(1)
        name_m = re.search(r'^\s*name:\s*(.+)$', front, re.MULTILINE)
        if name_m:
            name = name_m.group(1).strip().strip('"').strip("'")
        desc_m = re.search(r'^\s*description:\s*(.+)$', front, re.MULTILINE)
        if desc_m:
            description = desc_m.group(1).strip().strip('"').strip("'")

    return {
        "name": name,
        "description": description,
        "path": str(skill_dir),
    }


def detect_project_type(project_dir: Path) -> list[str]:
    """Detect project types based on file presence."""
    types = []

    checks = [
        ("package.json", "node_project"),
        ("requirements.txt", "python_project"),
        ("pyproject.toml", "python_project"),
        ("Cargo.toml", "rust_project"),
        ("go.mod", "go_project"),
        ("pom.xml", "java_maven"),
        ("build.gradle", "java_gradle"),
        ("Gemfile", "ruby_project"),
        ("composer.json", "php_project"),
        ("CMakeLists.txt", "cpp_project"),
    ]

    for filename, ptype in checks:
        if (project_dir / filename).exists():
            if ptype not in types:
                types.append(ptype)

    if not types:
        types.append("unknown")

    return types


def detect_frontend_framework(project_dir: Path) -> str | None:
    """Check for common frontend framework indicators."""
    pkg = project_dir / "package.json"
    if not pkg.exists():
        return None

    data = read_jsonc(pkg)
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

    frameworks = {
        "react": ["react", "react-dom"],
        "vue": ["vue", "nuxt"],
        "angular": ["@angular/core"],
        "svelte": ["svelte", "sveltekit"],
        "solid": ["solid-js"],
        "nextjs": ["next"],
        "astro": ["astro"],
        "remix": ["@remix-run/react"],
    }

    for framework, packages in frameworks.items():
        for p in packages:
            if p in deps:
                return framework

    return None


def has_database_indicator(project_dir: Path) -> set[str]:
    """Scan project for actual database library usage in source code only."""
    dbs = set()

    # Import patterns that are unlikely to false-positive on docs/skill names
    import_patterns: dict[str, list[str]] = {
        "mysql": [
            r'import\s+mysql(?:connector|\.connector)',
            r'from\s+mysql(?:connector|\.connector)\s+import',
            r'require\([\'"]mysql[\'"]\)',
            r'from\s+[\'"]mysql[\'"]',
            r'import\s+pymysql',
            r'from\s+pymysql\s+import',
            r'import\s+MySQLdb',
            r'from\s+MySQLdb\s+import',
        ],
        "postgres": [
            r'import\s+psycopg',
            r'from\s+psycopg\s+import',
            r'require\([\'"]pg[\'"]\)',
            r'import\s+asyncpg',
            r'from\s+asyncpg\s+import',
            r'from\s+[\'"]pg[\'"]',
        ],
        "sqlite": [
            r'import\s+sqlite3',
            r'from\s+sqlite3\s+import',
            r'require\([\'"]better-sqlite3[\'"]\)',
            r'require\([\'"]sqlite3[\'"]\)',
        ],
        "redis": [
            r'import\s+redis',
            r'from\s+redis\s+import',
            r'require\([\'"]redis[\'"]\)',
            r'import\s+aioredis',
            r'require\([\'"]ioredis[\'"]\)',
        ],
    }

    exclude_dirs = {
        "node_modules", ".git", "__pycache__", ".agents", ".opencode",
        "references", "examples", "agents_md_examples",
    }

    for root, dirs, files in os.walk(str(project_dir)):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

        # Check package.json in each subdirectory
        if "package.json" in files:
            pkg_path = os.path.join(root, "package.json")
            try:
                pkg_data = read_jsonc(Path(pkg_path))
                deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                db_pkg_map = {
                    "mysql": {"mysql", "mysql2", "pymysql"},
                    "postgres": {"pg", "psycopg2", "postgresql"},
                    "sqlite": {"sqlite3", "better-sqlite3"},
                    "redis": {"redis", "ioredis"},
                }
                for db, pkg_names in db_pkg_map.items():
                    if db not in dbs and deps.keys() & pkg_names:
                        dbs.add(db)
            except Exception:
                pass

        # Check source files for import patterns
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext not in (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs"):
                continue

            try:
                with open(os.path.join(root, f), encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
            except Exception:
                continue

            for db, patterns in import_patterns.items():
                if db not in dbs:
                    for pat in patterns:
                        if re.search(pat, content):
                            dbs.add(db)
                            break

    return dbs


def read_agents_md(project_dir: Path) -> str | None:
    """Read project AGENTS.md if it exists."""
    for name in ["AGENTS.md", "CLAUDE.md", "AGENTS", "CLAUDE"]:
        p = project_dir / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return None


def extract_agents_domains(agents_content: str) -> dict[str, bool]:
    """Extract domain mentions from AGENTS.md content."""
    c = agents_content.lower()
    return {
        "frontend": any(kw in c for kw in ["前端", "frontend", "front-end", "ui", "vue", "react", "angular",
                                             "component", "畫面", "網頁", "界面", "style", "css"]),
        "database": any(kw in c for kw in ["資料庫", "database", "mysql", "postgres", "sqlite", "redis", "db"]),
        "mobile": any(kw in c for kw in ["mobile", "app", "ios", "android", "flutter", "react native",
                                          "swift", "kotlin", "行動"]),
    }


def classify_project(project_dir: Path, agents_content: str | None) -> str:
    """Determine a human-readable project classification."""
    types = detect_project_type(project_dir)
    framework = detect_frontend_framework(project_dir)

    if framework:
        if "node_project" in types:
            return f"Web app ({framework})"
        return f"Frontend ({framework})"

    # Check if it looks like a skill repo (like my-skills)
    skill_dirs = [d for d in project_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    if len(skill_dirs) >= 3:
        return "Agent Skills Repository"

    if "python_project" in types:
        return "Python project"
    if "rust_project" in types:
        return "Rust project"
    if "go_project" in types:
        return "Go project"
    if "node_project" in types:
        return "Node.js project"

    return "Generic project"


# ── MCP relevance rules ──────────────────────────────────────────────────
MCP_RULES: dict[str, dict] = {
    "easy-mysql-mcp": {
        "label": "MySQL",
        "relevance_if_db": "mysql",
    },
    "easy-pg-mcp": {
        "label": "PostgreSQL",
        "relevance_if_db": "postgres",
    },
    "easy-sqlite-mcp": {
        "label": "SQLite",
        "relevance_if_db": "sqlite",
    },
    "easy-redis-mcp": {
        "label": "Redis",
        "relevance_if_db": "redis",
    },
    "brave-search": {
        "always_b": True,
    },
    "context7": {
        "always_b": True,
    },
}

SKILL_RULES: dict[str, dict] = {
    "agents-md-creator": {"always_b": True, "agents_keyword": "frontend"},
    "codex-prompt-analysis": {"always_b": True},
    "create-plan": {"always_a": True},
    "execute-plan": {"always_a": True},
    "find-skills": {"always_c": True},
    "gemini-api-dev": {},
    "mysql": {"agents_keyword_dbs": ["mysql"]},
    "reproduce-bug": {"always_a": True},
    "research-plan": {"always_a": True},
    "source-command-baseline-ui": {"agents_keyword": "frontend"},
    "ui-ux-pro-max": {"agents_keyword": "frontend"},
}


def rate_mcp(
    name: str,
    config: dict,
    project_dbs: set[str],
    agents_domains: dict[str, bool],
) -> dict:
    """Rate a single MCP's relevance to the current project."""
    rule = MCP_RULES.get(name, {})
    grade = "D"
    reason = "與專案領域無關"

    mcp_label = rule.get("label", name)

    # always_b MCPs (brave-search, context7)
    if rule.get("always_b"):
        grade = "B"
        reason = f"開發通用工具 ({mcp_label})"

    # DB-specific MCPs
    db_key = rule.get("relevance_if_db")
    if db_key:
        if db_key in project_dbs:
            grade = "A"
            reason = f"專案使用 {mcp_label}"
        elif agents_domains.get("database"):
            grade = "B"
            reason = f"AGENTS.md 提及資料庫需求"
        else:
            grade = "D"
            reason = f"專案未使用 {mcp_label}"

    return {
        "name": name,
        "grade": grade,
        "reason": reason,
        "suggest_action": "保留" if grade in ("A", "B") else "建議屏蔽",
        "project_override": None if grade in ("A", "B") else {"enabled": False},
    }


def rate_skill(
    name: str,
    info: dict | None,
    project_dbs: set[str],
    agents_domains: dict[str, bool],
    project_type: str,
) -> dict:
    """Rate a single skill's relevance."""
    rule = SKILL_RULES.get(name, {})
    grade = "D"
    reason = "與專案領域無關"

    desc = info["description"] if info else ""

    if rule.get("always_a"):
        grade = "A"
        reason = "開發必備工具"
    elif rule.get("always_b"):
        grade = "B"
        reason = "開發常用工具"
        agents_word = rule.get("agents_keyword")
        if agents_word and agents_domains.get(agents_word):
            grade = "A"
            reason = f"AGENTS.md 提及 {agents_word} 需求 → 高相關"
    elif rule.get("always_c"):
        grade = "C"
        reason = "偶爾使用"
    else:
        # Dynamic rules
        agents_kws = rule.get("agents_keywords", [])
        if agents_kws and any(kw in desc.lower() for kw in agents_kws):
            grade = "B"
            reason = "與專案類型可能相關"

        agents_db = rule.get("agents_keyword_dbs", [])
        if agents_db:
            if any(db in project_dbs for db in agents_db):
                grade = "A"
                reason = f"專案使用對應資料庫"
            elif agents_domains.get("database"):
                grade = "B"
                reason = "AGENTS.md 提及資料庫需求"
            else:
                grade = "D"
                reason = "專案未使用對應資料庫"

        # UI skills
        if name in ("source-command-baseline-ui", "ui-ux-pro-max"):
            if "frontend" in project_type.lower() or "ui" in project_type.lower():
                grade = "A"
                reason = "專案包含前端 UI"
            elif agents_domains.get("frontend"):
                grade = "B"
                reason = "AGENTS.md 提及前端需求"
            else:
                grade = "D"
                reason = "專案無前端 UI"

    return {
        "name": name,
        "grade": grade,
        "reason": reason,
        "suggest_action": "保留" if grade in ("A", "B") else "建議屏蔽",
    }


def check_duplicates(
    global_mcp: dict,
    project_mcp: dict,
) -> list[dict]:
    """Detect MCPs defined in both global and project config."""
    duplicates = []
    for name, p_config in project_mcp.items():
        if name in global_mcp and isinstance(p_config, dict):
            # Only flag if project has full definition (not just { enabled: false })
            if "type" in p_config or "command" in p_config or "url" in p_config:
                duplicates.append({
                    "name": name,
                    "severity": "warning",
                    "detail": f"'{name}' 在 global 與 project 皆有完整定義。"
                              f"建議移除 project 定義，僅保留 `{{ \"enabled\": false }}` 即可。",
                })
    return duplicates


def suggest_safe_paths(project_dir: Path) -> list[dict]:
    """Suggest low-risk paths for external_directory permission."""
    seen: set[str] = set()
    suggestions: list[dict] = []

    agent_content = read_agents_md(project_dir)
    if agent_content and "/tmp/" in agent_content:
        suggestions.append({
            "path": "/tmp/*",
            "action": "allow",
            "reason": "AGENTS.md 明確使用 /tmp/ 路徑",
        })
        seen.add("/tmp/*")

    defaults = [
        ("/tmp/*", "通用暫存目錄，無持續性資料"),
        ("/var/tmp/*", "持久性暫存目錄"),
        ("/dev/null", "捨棄輸出用"),
    ]
    for path, reason in defaults:
        if path not in seen:
            suggestions.append({"path": path, "action": "allow", "reason": reason})
            seen.add(path)

    # $TMPDIR if exists and differs from /tmp
    tmpdir = os.environ.get("TMPDIR")
    if tmpdir and tmpdir != "/tmp":
        key = f"{tmpdir}/*" if not tmpdir.endswith("/*") else tmpdir
        if key not in seen:
            suggestions.append({"path": key, "action": "allow", "reason": "系統指定的暫存目錄（$TMPDIR）"})
            seen.add(key)

    # Project-internal .cache
    if (project_dir / ".cache").is_dir():
        suggestions.append({"path": ".cache/*", "action": "allow", "reason": "建置快取目錄，非原始碼"})
        seen.add(".cache/*")

    return suggestions


# ── New analysis: Provider / Model ────────────────────────────────────
def analyze_provider_model(global_config: dict) -> list[dict]:
    """Analyze provider and model configuration."""
    findings: list[dict] = []

    providers = global_config.get("provider", {})
    disabled = global_config.get("disabled_providers", [])
    enabled = global_config.get("enabled_providers", [])
    model = global_config.get("model")
    small_model = global_config.get("small_model")
    default_agent = global_config.get("default_agent")

    active_providers = [k for k in providers if k not in disabled]

    if not disabled and not enabled and len(active_providers) >= 3:
        findings.append({
            "area": "providers",
            "severity": "suggestion",
            "detail": f"{len(active_providers)} 個 provider 已啟用且未設定 disabled_providers。"
                      f"建議關閉非必要的 provider（如僅使用 Anthropic 時設 disabled_providers: [\"openai\", \"gemini\"]）。",
        })

    if not model:
        findings.append({
            "area": "model",
            "severity": "suggestion",
            "detail": "`model` 未設定。建議固定一個 model，避免 session 間模型不一致。",
        })

    if not small_model:
        findings.append({
            "area": "small_model",
            "severity": "info",
            "detail": "`small_model` 未設定。建議設定輕量 model（如 Haiku）以節省輕量任務的 token 成本。",
        })

    if not default_agent:
        findings.append({
            "area": "default_agent",
            "severity": "info",
            "detail": "`default_agent` 未設定。建議設為 \"build\" 或 \"plan\" 以確保預期行為。",
        })

    return findings


# ── New analysis: Feature Toggles ─────────────────────────────────────
def analyze_feature_toggles(project_dir: Path, global_config: dict) -> list[dict]:
    """Analyze feature toggles (formatter, lsp, snapshot, autoupdate, share)."""
    findings: list[dict] = []

    fmt = global_config.get("formatter")
    lsp = global_config.get("lsp")
    snapshot = global_config.get("snapshot")
    autoup = global_config.get("autoupdate")
    share = global_config.get("share")

    has_pkg_json = (project_dir / "package.json").exists()
    has_formatter_config = any(
        (project_dir / f).exists()
        for f in [".prettierrc", ".prettierrc.json", ".prettierrc.js", ".prettierrc.yaml",
                   "prettier.config.js", "rustfmt.toml", "pyproject.toml", ".ruff.toml"]
    )
    has_ts = any(project_dir.glob("**/*.ts")) or any(project_dir.glob("**/*.tsx"))
    has_python = any(project_dir.glob("**/*.py"))

    # formatter
    if has_formatter_config or has_pkg_json:
        if fmt is None or fmt is False:
            findings.append({
                "area": "formatter",
                "severity": "suggestion",
                "detail": "專案有 formatter 設定檔或 package.json，建議啟用 formatter。",
            })
    elif fmt is True:
        findings.append({
            "area": "formatter",
            "severity": "info",
            "detail": "formatter 已啟用但專案無對應設定檔。formatter 會自動偵測，目前無需異動。",
        })

    # lsp
    needs_lsp = has_ts or has_python or any(project_dir.glob("**/*.go")) or any(project_dir.glob("**/*.rs"))
    if needs_lsp:
        if lsp is None or lsp is False:
            findings.append({
                "area": "lsp",
                "severity": "suggestion",
                "detail": "專案含 TypeScript/Python/Go/Rust 檔案，建議啟用 LSP。",
            })

    # snapshot (only flag for very large repos)
    if snapshot is False:
        findings.append({
            "area": "snapshot",
            "severity": "info",
            "detail": "snapshot 已關閉。若需要還原操作，建議開啟。",
        })

    # autoupdate
    if autoup is False:
        findings.append({
            "area": "autoupdate",
            "severity": "info",
            "detail": "autoupdate 已關閉。建議設為 \"notify\" 以接收版本通知但不自動更新。",
        })

    # share
    if share == "disabled":
        findings.append({
            "area": "share",
            "severity": "info",
            "detail": "分享已停用。若無安全顧慮，可維持預設 manual 模式。",
        })

    return findings


# ── New analysis: Resource Usage ──────────────────────────────────────
def analyze_resource_usage(global_config: dict, mcp_enabled_count: int) -> list[dict]:
    """Analyze resource usage (watcher.ignore, MCP count, compaction)."""
    findings: list[dict] = []

    watcher = global_config.get("watcher", {})
    ignore_list = watcher.get("ignore", [])
    missing = [p for p in ["node_modules/**", "dist/**", ".git/**"] if p not in ignore_list]
    if missing:
        findings.append({
            "area": "watcher.ignore",
            "severity": "suggestion",
            "detail": f"watcher.ignore 缺少: {', '.join(missing)}。建議加入以減少檔案監控負擔。",
        })

    if mcp_enabled_count > 5:
        findings.append({
            "area": "mcp_count",
            "severity": "warning",
            "detail": f"已啟用 {mcp_enabled_count} 個 MCP server，超過 5 個建議線。"
                      f"過多 MCP 會消耗 token，建議關閉與專案無關的 MCP。",
        })

    compaction = global_config.get("compaction", {})
    if compaction.get("auto") is False:
        findings.append({
            "area": "compaction",
            "severity": "suggestion",
            "detail": "compaction.auto 已關閉。建議啟用以自動管理 context 長度。",
        })

    return findings


# ── New analysis: Safety Checks ───────────────────────────────────────
def analyze_safety_checks(global_config: dict) -> list[dict]:
    """Analyze safety-related permission settings (no flow-disrupting suggestions)."""
    findings: list[dict] = []

    perm = global_config.get("permission", {})
    if isinstance(perm, str):
        return findings

    # Check rm -rf in bash
    bash_perm = perm.get("bash", {})
    if isinstance(bash_perm, str):
        if bash_perm == "allow":
            findings.append({
                "area": "bash.rm",
                "severity": "suggestion",
                "detail": "bash 權限為全域 allow，但未對 `rm -rf *` 設 deny。"
                          "建議加入 `\"rm -rf *\": \"deny\"` 防止誤刪。",
            })
    elif isinstance(bash_perm, dict):
        has_rm_deny = any("rm " in k or "rm -rf" in k for k in bash_perm if bash_perm[k] == "deny")
        if not has_rm_deny and bash_perm.get("*", "allow") != "deny":
            findings.append({
                "area": "bash.rm",
                "severity": "suggestion",
                "detail": "bash 權限未對 `rm -rf *` 設 deny。建議加入 `\"rm -rf *\": \"deny\"` 防止誤刪。",
            })

    # Check force push protection (only match --force / -f, not normal git push)
    FORCE_PUSH_PATTERNS = ["--force", " -f"]
    has_force_push_protection = False
    if isinstance(bash_perm, dict):
        for k in bash_perm:
            if bash_perm[k] in ("ask", "deny"):
                if any(fp in k for fp in FORCE_PUSH_PATTERNS):
                    has_force_push_protection = True
                    break
    if isinstance(bash_perm, dict) and not has_force_push_protection:
        findings.append({
            "area": "bash.force_push",
            "severity": "suggestion",
            "detail": "未對 force push 設保護。建議加入 `\"git push --force*\": \"ask\"`"
                      "以避免意外強推，不影響一般 `git push`。",
        })

    # Check .env read
    read_perm = perm.get("read", {})
    if isinstance(read_perm, dict):
        if "*.env" not in read_perm or read_perm.get("*.env") != "deny":
            if "*.env.*" not in read_perm or read_perm.get("*.env.*") != "deny":
                findings.append({
                    "area": "read.env",
                    "severity": "info",
                    "detail": ".env 檔案的讀取權限未明確 deny。opencode 預設已阻止，此為確認性通知。",
                })

    # Check bash safety whitelist (avoid over-protection)
    SAFE_BASH_PATTERNS = [
        ("ls *", "目錄列表"),
        ("pwd", "當前路徑"),
        ("head *", "檔案預覽"),
        ("tail *", "檔案尾部"),
        ("grep *", "內容搜尋"),
        ("rg *", "內容搜尋（ripgrep）"),
        ("find *", "檔案搜尋"),
        ("git status", "版本控制狀態"),
        ("git diff *", "版本控制 diff"),
        ("git log *", "版本控制歷史"),
        ("git branch *", "版本控制 branch"),
        ("npm test", "執行測試"),
        ("npm run lint", "執行 linter"),
        ("pnpm test", "執行測試（pnpm）"),
        ("pnpm lint", "執行 linter（pnpm）"),
        ("python -m pytest *", "執行 Python 測試"),
    ]
    # cat is only safe if .env is already denied
    read_perm = perm.get("read", {})
    env_denied = False
    if isinstance(read_perm, dict):
        env_denied = read_perm.get("*.env") == "deny" or read_perm.get("*.env.*") == "deny"
    SAFE_BASH_CAT = [("cat *", "檔案閱讀")] if env_denied else []

    if isinstance(bash_perm, dict):
        has_catch_all_ask = bash_perm.get("*") == "ask"
        if has_catch_all_ask:
            all_safe = SAFE_BASH_PATTERNS + SAFE_BASH_CAT
            missing_safe = [f"`{p}`" for p, _ in all_safe
                           if not any(k.replace("*", "") in p.replace("*", "") for k in bash_perm)]
            if missing_safe:
                note = "" if env_denied else "（不含 `cat *`，因 `.env` 讀取尚未 deny）"
                findings.append({
                    "area": "bash.safe_whitelist",
                    "severity": "suggestion",
                    "detail": "bash 設為 `\"*\": \"ask\"`，但未對安全指令設例外："
                              f"{', '.join(missing_safe[:8])}{' 等' if len(missing_safe)>8 else ''}"
                              f"{note}。建議加入 allow 以減少日常操作的中斷。",
                })

    # Check external_directory wildcard allow
    ext_dir = perm.get("external_directory", {})
    if isinstance(ext_dir, dict) and ext_dir.get("*") == "allow":
        findings.append({
            "area": "external_directory",
            "severity": "warning",
            "detail": "external_directory 設為 `\"*\": \"allow\"`（全域開放外部目錄）。"
                      "建議限縮到具體路徑如 `\"/tmp/*\"`。",
        })

    return findings


# ── New analysis: Agent Audit ──────────────────────────────────────────
def analyze_agents(global_config: dict) -> list[dict]:
    """Audit custom agent definitions."""
    findings: list[dict] = []

    agents = global_config.get("agent", {})
    for name, cfg in agents.items():
        if cfg.get("disable"):
            continue

        desc = cfg.get("description") or cfg.get("prompt", "")[:80]
        if not cfg.get("description"):
            findings.append({
                "area": f"agent.{name}",
                "severity": "suggestion",
                "detail": f"agent '{name}' 缺少必填欄位 `description`。建議補上以利自動選用。",
            })

        mode = cfg.get("mode", "all")
        perm = cfg.get("permission", {})
        edit_perm = perm.get("edit") if isinstance(perm, dict) else None

        if edit_perm == "deny" and mode == "primary":
            findings.append({
                "area": f"agent.{name}",
                "severity": "warning",
                "detail": f"agent '{name}' 為 primary 模式但 edit 設為 deny。"
                          f"primary agent 無法編輯檔案可能會造成混淆，建議改為 subagent 模式。",
            })

        # Check prompt file size
        prompt = cfg.get("prompt", "")
        file_match = re.match(r"\{file:(.+)\}", prompt)
        if file_match:
            prompt_path = Path(file_match.group(1))
            if not prompt_path.is_absolute():
                prompt_path = Path.home() / ".config" / "opencode" / prompt_path
            if prompt_path.exists():
                text = prompt_path.read_text(encoding="utf-8", errors="replace")
                tokens = round(len(text) / 2.2)
                if tokens > 2000:
                    findings.append({
                        "area": f"agent.{name}.prompt_size",
                        "severity": "warning",
                        "detail": f"agent '{name}' 的 prompt 檔案（{prompt_path.name}）約 {tokens} tokens。"
                                  f"超過 2000 建議線，每次 session 都會載入，建議精簡。",
                    })

    return findings


# ── New analysis: AGENTS.md Health ────────────────────────────────────
COMMON_COMMANDS = {
    "npm install", "npm ci", "npm run build", "npm run test", "npm run start",
    "npm run dev", "npm run lint", "npm test", "npm start",
    "yarn install", "yarn build", "yarn test", "yarn start",
    "pnpm install", "pnpm build", "pnpm test", "pnpm start",
    "pip install", "pip install -r", "cargo build", "cargo test",
    "cargo run", "go build", "go test", "go run",
    "python -m pytest", "python manage.py", "make build", "make test",
}

AGENTS_MD_SECTION_PATTERNS = {
    "changelog": re.compile(r"^##\s*(changelog|history|what'?s\s+new)", re.IGNORECASE),
    "progress": re.compile(r"^##\s*(progress|status|已完成|目前進度)", re.IGNORECASE),
    "dynamic": re.compile(r"^##\s*(todo|known\s+issues|open\s+questions|待辦|已知問題)", re.IGNORECASE),
    "file_structure": re.compile(r"^##\s*(file\s*(structure|tree)|directory\s*(structure|tree)|目錄結構)", re.IGNORECASE),
}

TREE_LINE = re.compile(r"[│├└─]+|^\s{2,}[\/\w]")
ABSOLUTE_PATH = re.compile(r"(?:^|\s)(/home/|/Users/|/root/|/var/www)")
INLINE_TODO = re.compile(r"(TODO|FIXME|HACK|XXX|BUG)\s*[:：]")


def _estimate_tokens(text: str) -> int:
    return round(len(text) / 2.2)


def analyze_agents_md_health(project_dir: Path) -> list[dict]:
    """Scan AGENTS.md for content that wastes context."""
    findings: list[dict] = []

    agents_path = None
    for name in ["AGENTS.md", "CLAUDE.md"]:
        p = project_dir / name
        if p.exists():
            agents_path = p
            break

    if not agents_path:
        return findings

    text = agents_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    tokens = _estimate_tokens(text)

    # 1. Token count warning
    if tokens > 4000:
        findings.append({
            "area": "token_count",
            "severity": "warning",
            "detail": f"AGENTS.md 約 {tokens} tokens，超過 4000 建議線。"
                      f"過大會消耗 session context，建議移除用不到的內容。",
        })

    # 2-5: Scan sections by headers + context
    critical_sections: dict[str, tuple[str, str]] = {
        "changelog": ("## Changelog / History", "回溯性紀錄，開發中用不到"),
        "progress": ("## Progress / Status", "動態內容，session 啟動即已過時"),
    }

    for section_type, (label, reason) in critical_sections.items():
        for i, line in enumerate(lines):
            m = AGENTS_MD_SECTION_PATTERNS[section_type].search(line)
            if not m:
                continue
            # Estimate token count for this section
            section_tokens = 0
            for j in range(i + 1, min(i + 200, len(lines))):
                if lines[j].startswith("## ") and not lines[j].startswith(line):
                    break
                section_tokens += len(lines[j])
            section_tokens = round(section_tokens / 2.2)
            if section_tokens < 20:
                continue

            findings.append({
                "area": f"section.{section_type}",
                "severity": "warning",
                "detail": f"{label} 區段（約 {section_tokens} tokens）→ {reason}，建議移除。",
            })
            break

    # 3 (separate). Inline TODO without standalone file
    has_standalone_todo = any(
        (project_dir / f).exists()
        for f in ["AGENTS_TODO.md", "TODO.md", "KNOWN_ISSUES.md", "AGENTS_KNOWN_ISSUES.md"]
    )
    for i, line in enumerate(lines):
        m = AGENTS_MD_SECTION_PATTERNS["dynamic"].search(line)
        if not m:
            continue
        if has_standalone_todo:
            continue
        section_tokens = 0
        for j in range(i + 1, min(i + 200, len(lines))):
            if lines[j].startswith("## ") and not lines[j].startswith(line):
                break
            section_tokens += len(lines[j])
        section_tokens = round(section_tokens / 2.2)
        if section_tokens < 20:
            continue
        findings.append({
            "area": "section.dynamic_inline",
            "severity": "warning",
            "detail": f"TODO/Known Issues 區段直接內嵌（約 {section_tokens} tokens）"
                      f"→ 建議移到獨立檔案（如 AGENTS_TODO.md）。",
        })
        break

    # 4. Trivial commands in bullet lists
    in_code_block = False
    trivial_cmds_found: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Check bullet lines for trivial commands
        if stripped.startswith("- ") or stripped.startswith("* "):
            cmd = stripped[2:].strip()
            # Remove backticks
            cmd_clean = cmd.strip("`").strip()
            if cmd_clean in COMMON_COMMANDS:
                trivial_cmds_found.append(cmd_clean)

    if trivial_cmds_found:
        count = len(trivial_cmds_found)
        examples = ", ".join(trivial_cmds_found[:5])
        suffix = " 等" if count > 5 else ""
        findings.append({
            "area": "trivial_commands",
            "severity": "info" if count <= 3 else "suggestion",
            "detail": f"含 {count} 個常識級指令（{examples}{suffix}）→ "
                      f"AI 已知基本操作，建議精簡，只保留有特殊 flag 或客製化的指令。",
        })

    # 5. File structure / directory tree
    for i, line in enumerate(lines):
        if AGENTS_MD_SECTION_PATTERNS["file_structure"].search(line):
            tree_tokens = 0
            for j in range(i + 1, min(i + 200, len(lines))):
                if lines[j].startswith("## ") and not lines[j].startswith(line):
                    break
                tree_tokens += len(lines[j])
            tree_tokens = round(tree_tokens / 2.2)
            if tree_tokens >= 40:
                findings.append({
                    "area": "section.file_tree",
                    "severity": "info",
                    "detail": f"完整目錄樹區段（約 {tree_tokens} tokens）→ "
                              f"大部分時間用不到，建議只保留重要入口路徑。",
                })
            break

    # 6. Long prose paragraphs (> 50 consecutive non-bullet, non-code lines)
    prose_lines = 0
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_block = not in_block
            prose_lines = 0
            continue
        if in_block:
            continue
        if stripped == "" or stripped.startswith(("- ", "* ", "##", "|", ">")):
            prose_lines = 0
            continue
        prose_lines += 1
        if prose_lines >= 50:
            findings.append({
                "area": "long_prose",
                "severity": "info",
                "detail": f"偵測到連續 {prose_lines}+ 行敘述性文字 → "
                          f"大段教學或說明建議移到 reference 文件或做成 skill。",
            })
            break

    # 7. Inline TODO/FIXME/HACK comments
    inline_count = 0
    for line in lines:
        if INLINE_TODO.search(line):
            inline_count += 1
    if inline_count >= 3:
        findings.append({
            "area": "inline_todos",
            "severity": "info",
            "detail": f"含 {inline_count} 處 TODO/FIXME/HACK 殘留註解 → "
                      f"建議清理或移到追蹤檔案。",
        })

    # 8. Machine-specific absolute paths
    abs_paths: set[str] = set()
    for line in lines:
        for m in ABSOLUTE_PATH.finditer(line):
            abs_paths.add(m.group(0).strip())
    if abs_paths:
        paths_str = ", ".join(sorted(abs_paths)[:3])
        findings.append({
            "area": "absolute_paths",
            "severity": "warning",
            "detail": f"含機器專屬絕對路徑（{paths_str}）→ "
                      f"建議改為相對路徑或移除，避免在其他環境失效。",
        })

    return findings


# ── New analysis: Custom Commands ─────────────────────────────────────
COMMAND_SUGGESTIONS: list[dict] = [
    {
        "name": "branch",
        "description": "建立或切換 Git branch",
        "trigger": "git",
        "condition": "has_git",
        "template": (
            "列出目前所有 branches：\n"
            "!`git branch -a`\n\n"
            "目前所在 branch：\n"
            "!`git branch --show-current`\n\n"
            "$ARGUMENTS\n\n"
            "若使用者有指定 branch 名稱，切換到該 branch（`git switch <name>`）。\n"
            "若未指定，根據目前進行中的工作建議 branch 名稱，詢問使用者確認後建立（`git switch -c <name>`）。"
        ),
    },
    {
        "name": "pr",
        "description": "產生 Pull Request 描述",
        "trigger": "git + remote",
        "condition": "has_git_remote",
        "template": (
            "最近 commits（與 base branch 比較）：\n"
            "!`git log $(git config init.defaultBranch || echo main)..HEAD --oneline`\n\n"
            "變更檔案：\n"
            "!`git diff --stat $(git config init.defaultBranch || echo main)`\n\n"
            "$ARGUMENTS\n\n"
            "根據以上 commits 與變更，產生一條 PR description，包含：\n"
            "- 變更摘要\n"
            "- 主要改動項目\n"
            "- 測試說明\n"
            "- 相關 issue（若有）\n"
            "格式參考 conventional commits，產出後直接輸出 markdown。"
        ),
    },
    {
        "name": "sync",
        "description": "Git + SVN 雙重同步提交",
        "trigger": "git + svn",
        "condition": "has_git_svn",
        "template": (
            "目前變更：\n"
            "!`git status --short`\n"
            "!`git diff --stat`\n\n"
            "$ARGUMENTS\n\n"
            "依序執行：\n"
            "1. `git add -A`\n"
            "2. `git commit -m \"<message>\"`（訊息由使用者提供或自動產生 conventional commit message）\n"
            "3. `svn add . --force`（錯誤可忽略）\n"
            "4. `svn commit -m \"<相同訊息>\"`\n"
            "最後用表格回報每項指令的結果。"
        ),
    },
    {
        "name": "clean",
        "description": "清理 build 產物並重新安裝依賴",
        "trigger": "node",
        "condition": "has_package_json",
        "template": (
            "$ARGUMENTS\n\n"
            "1. 移除 `node_modules/`、`dist/`、`build/`、`.next/` 等可重建目錄\n"
            "2. 執行 `npm install`（或偵測 lockfile 使用對應工具）\n"
            "3. 確認安裝完成\n"
            "每步完成後回報結果。"
        ),
    },
    {
        "name": "test",
        "description": "跑測試並分析失敗",
        "trigger": "test framework",
        "condition": "has_test_framework",
        "template": (
            "執行測試並顯示結果：\n"
            "!`npm test 2>&1 || true`\n\n"
            "分析測試輸出：\n"
            "- 哪些測試失敗\n"
            "- 失敗原因歸納\n"
            "- 建議修復方向\n"
            "每項列出。"
        ),
    },
    {
        "name": "lint",
        "description": "跑 linter 並自動修復",
        "trigger": "linter",
        "condition": "has_linter",
        "template": (
            "執行 linter 檢查：\n"
            "!`npx eslint . --fix 2>&1 || true`\n\n"
            "若仍有無法自動修復的問題，列出依嚴重度分組的殘留問題。"
        ),
    },
    {
        "name": "release",
        "description": "執行發佈流程",
        "trigger": "AGENTS.md 提及發佈",
        "condition": "agents_mentions_release",
        "template": (
            "參照以下 AGENTS.md 描述的發佈流程逐步執行。\n"
            "若流程不明確，先詢問使用者確認順序與版本號。\n\n"
            "$ARGUMENTS\n\n"
            "典型步驟包含但不限於：\n"
            "- bump 版本號\n"
            "- 更新 changelog\n"
            "- 執行 build\n"
            "- 打 git tag\n"
            "- push 到 remote\n"
            "每步完成後回報結果與下一步。"
        ),
    },
    {
        "name": "review",
        "description": "Code review 未提交變更",
        "trigger": "AGENTS.md 提及 code review",
        "condition": "agents_mentions_review",
        "template": (
            "尚未提交的變更：\n"
            "!`git diff`\n\n"
            "已暫存的變更：\n"
            "!`git diff --cached`\n\n"
            "逐項審查以下面向：\n"
            "- 正確性：邏輯是否有 edge case 遺漏\n"
            "- 安全性：是否有注入或權限問題\n"
            "- 效能：是否有不必要的計算或查詢\n"
            "- 可維護性：命名、註解、結構是否合理\n"
            "對每個問題給出具體改善建議與範例。"
        ),
    },
    {
        "name": "sync-deps",
        "description": "依鎖檔重新同步依賴",
        "trigger": "package manager",
        "condition": "has_package_json",
        "template": (
            "專案依賴可能已過期或與鎖檔不一致。\n\n"
            "!`ls package.json`\n\n"
            "$ARGUMENTS\n\n"
            "依專案偵測到的套件管理工具執行對應指令：\n"
            "- 有 `package-lock.json` → `npm ci`\n"
            "- 有 `yarn.lock` → `yarn install --frozen-lockfile`\n"
            "- 有 `pnpm-lock.yaml` → `pnpm install --frozen-lockfile`\n"
            "執行後確認無錯誤。"
        ),
    },
    {
        "name": "debug",
        "description": "檢視最近日誌並協助定位問題",
        "trigger": "logs directory",
        "condition": "has_logs_dir",
        "template": (
            "最近日誌內容：\n"
            "!`ls -t logs/ 2>/dev/null || ls -t storage/logs/ 2>/dev/null | head -5`\n"
            "!`tail -n 100 $(ls -t logs/*.log 2>/dev/null storage/logs/*.log 2>/dev/null | head -1) 2>/dev/null || echo '無日誌檔'`\n\n"
            "分析以上日誌：\n"
            "- 是否有 error / exception / 關鍵錯誤\n"
            "- 錯誤發生的時間點與可能原因\n"
            "- 建議的下一步排查方向"
        ),
    },
    {
        "name": "skill-check",
        "description": "檢查所有 SKILL.md frontmatter 完整性",
        "trigger": "Skill repo",
        "condition": "is_skill_repo",
        "template": (
            "掃描專案內所有 `SKILL.md` 檔案，檢查 frontmatter 的 `name` 與 `description` 是否皆存在。\n\n"
            "對每個缺少必填欄位的 SKILL.md：\n"
            "- 列出檔案路徑\n"
            "- 標示缺少的欄位\n"
            "- 建議補上"
        ),
    },
]


def _collect_existing_commands(global_config: dict, project_config: dict, project_dir: Path) -> set[str]:
    """Collect all existing custom command names from all sources."""
    names: set[str] = set()

    for cfg in (global_config, project_config):
        cmds = cfg.get("command", {})
        if isinstance(cmds, dict):
            names.update(cmds.keys())

    for base_dir in (Path.home() / ".config" / "opencode" / "commands", project_dir / ".opencode" / "commands"):
        if base_dir.is_dir():
            for f in base_dir.iterdir():
                if f.suffix in (".md", ".mdx"):
                    names.add(f.stem)

    return names


def _has_git_remote(project_dir: Path) -> bool:
    git_dir = project_dir / ".git"
    if not git_dir.exists():
        return False
    config_file = git_dir / "config"
    if config_file.exists():
        content = config_file.read_text(encoding="utf-8", errors="ignore")
        return '[remote "origin"]' in content
    return False


def analyze_custom_commands(
    project_dir: Path,
    global_config: dict,
    project_config: dict,
    project_type: str,
    agents_content: str | None,
) -> list[dict]:
    """Suggest missing custom commands based on project tooling."""
    existing = _collect_existing_commands(global_config, project_config, project_dir)

    has_git = (project_dir / ".git").exists()
    has_git_remote = _has_git_remote(project_dir)
    svn_dir = project_dir / ".svn"
    has_svn = svn_dir.exists() and svn_dir.is_dir() and shutil.which("svn") is not None
    has_package_json = (project_dir / "package.json").exists()
    has_requirements_txt = (project_dir / "requirements.txt").exists()
    has_logs_dir = (project_dir / "logs").is_dir() or (project_dir / "storage" / "logs").is_dir()
    has_test_framework = False
    has_linter = False

    if has_package_json:
        pkg = read_jsonc(project_dir / "package.json")
        scripts = pkg.get("scripts", {})
        if any(k in scripts for k in ("test", "jest", "vitest", "mocha")):
            has_test_framework = True
        if any(k in scripts for k in ("lint", "eslint")):
            has_linter = True
        for dep_name in {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}:
            if not has_test_framework and dep_name in ("jest", "vitest", "mocha", "ava", "tap"):
                has_test_framework = True
            if not has_linter and dep_name in ("eslint", "prettier", "typescript"):
                has_linter = True

    for config_file in [".eslintrc", ".eslintrc.json", ".eslintrc.js", ".eslintrc.yaml",
                         ".eslintrc.yml", ".ruff.toml", ".golangci.yml", ".golangci.yaml"]:
        if (project_dir / config_file).exists():
            has_linter = True

    for config_file in ["pytest.ini", "pyproject.toml", "Cargo.toml", "go.mod"]:
        if (project_dir / config_file).exists():
            has_test_framework = True

    agents_mentions_release = False
    agents_mentions_review = False
    if agents_content:
        low = agents_content.lower()
        if any(kw in low for kw in ["release", "deploy", "publish", "發佈", "部署", "發布", "版本發布"]):
            agents_mentions_release = True
        if any(kw in low for kw in ["review", "code review", "審查", "程式碼審查"]):
            agents_mentions_review = True

    is_skill_repo = project_type == "Agent Skills Repository"

    # Evaluate conditions
    conditions: dict[str, bool] = {
        "has_git": has_git,
        "has_git_remote": has_git_remote,
        "has_git_svn": has_git and has_svn,
        "has_package_json": has_package_json,
        "has_requirements_txt": has_requirements_txt,
        "has_logs_dir": has_logs_dir,
        "has_test_framework": has_test_framework,
        "has_linter": has_linter,
        "agents_mentions_release": agents_mentions_release,
        "agents_mentions_review": agents_mentions_review,
        "is_skill_repo": is_skill_repo,
    }

    findings: list[dict] = []
    for suggestion in COMMAND_SUGGESTIONS:
        name = suggestion["name"]
        if name in existing:
            continue
        cond = suggestion["condition"]
        if not conditions.get(cond):
            continue
        findings.append({
            "name": name,
            "description": suggestion["description"],
            "trigger": suggestion["trigger"],
            "template": suggestion["template"],
        })

    return findings


# ── New analysis: Instructions Load ───────────────────────────────────
def analyze_instructions(global_config: dict, project_dir: Path) -> list[dict]:
    """Check how many files instructions patterns load."""
    findings: list[dict] = []

    instructions = global_config.get("instructions")
    if not instructions:
        return findings

    matched_files: list[Path] = []
    for pattern in instructions:
        # Resolve relative to project dir
        p = project_dir / pattern
        if p.exists():
            matched_files.append(p)
        else:
            # Try as glob
            globbed = list(project_dir.glob(pattern))
            matched_files.extend(globbed)

    # Deduplicate
    seen: set[Path] = set()
    matched_files = [f for f in matched_files if not (f in seen or seen.add(f))]

    if len(matched_files) > 5:
        total_tokens = sum(round(len(f.read_text(encoding="utf-8", errors="replace")) / 2.2)
                          for f in matched_files if f.is_file())
        findings.append({
            "area": "instructions_load",
            "severity": "suggestion",
            "detail": f"instructions 匹配到 {len(matched_files)} 個檔案（約 {total_tokens} tokens）。"
                      f"超過 5 個建議線，每次 session 都會載入，建議合併或精簡。",
        })

    return findings


def main():
    parser = argparse.ArgumentParser(description="opencode-optimizer analyzer")
    parser.add_argument("--project-dir", default=".", help="Path to the project directory")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.is_dir():
        print(json.dumps({"error": f"Not a directory: {project_dir}"}))
        sys.exit(1)

    # ── Scan ──────────────────────────────────────────────────────────
    global_config = read_jsonc(GLOBAL_CONFIG)
    global_mcp = global_config.get("mcp", {})

    project_config = read_jsonc(project_dir / "opencode.json") or read_jsonc(project_dir / "opencode.jsonc")
    project_mcp = project_config.get("mcp", {})

    # Global skills
    global_skills: list[dict] = []
    if GLOBAL_SKILLS_DIR.is_dir():
        for entry in sorted(GLOBAL_SKILLS_DIR.iterdir()):
            if entry.is_dir():
                info = read_skill_info(entry)
                if info:
                    global_skills.append(info)

    # Project analysis
    project_dbs = has_database_indicator(project_dir)
    project_type = classify_project(project_dir, None)
    agents_content = read_agents_md(project_dir)
    agents_domains = extract_agents_domains(agents_content) if agents_content else {}
    frontend_framework = detect_frontend_framework(project_dir)
    project_types_list = detect_project_type(project_dir)

    # ── Analyze ───────────────────────────────────────────────────────
    # Duplicates
    duplicates = check_duplicates(global_mcp, project_mcp)

    # MCP ratings
    mcp_ratings = {}
    for name in global_mcp:
        mcp_ratings[name] = rate_mcp(name, global_mcp[name], project_dbs, agents_domains)

    mcp_enabled_count = sum(1 for r in mcp_ratings.values() if r["grade"] in ("A", "B"))

    # Skill ratings
    skill_ratings = {}
    for info in global_skills:
        name = info["name"]
        skill_ratings[name] = rate_skill(name, info, project_dbs, agents_domains, project_type)

    # Safe paths
    safe_paths = suggest_safe_paths(project_dir)

    # New analysis modules
    provider_findings = analyze_provider_model(global_config)
    feature_findings = analyze_feature_toggles(project_dir, global_config)
    resource_findings = analyze_resource_usage(global_config, mcp_enabled_count)
    safety_findings = analyze_safety_checks(global_config)
    agent_findings = analyze_agents(global_config)
    agents_md_findings = analyze_agents_md_health(project_dir)
    instructions_findings = analyze_instructions(global_config, project_dir)

    custom_cmd_findings = analyze_custom_commands(
        project_dir, global_config, project_config, project_type, agents_content,
    )

    # ── Build project config suggestion ────────────────────────────────
    project_suggestion: dict = {}
    if project_config:
        project_suggestion = dict(project_config)

    # Add enabled: false for D-grade MCPs
    mcp_overrides = {}
    for name, rating in sorted(mcp_ratings.items()):
        if rating["project_override"] is not None:
            mcp_overrides[name] = rating["project_override"]
    if mcp_overrides:
        project_suggestion.setdefault("mcp", {}).update(mcp_overrides)

    # Add safe paths
    ext_dir: dict[str, str] = {}
    for sp in safe_paths:
        ext_dir[sp["path"]] = sp["action"]
    if ext_dir:
        permission = project_suggestion.setdefault("permission", {})
        existing_ext = permission.get("external_directory", {})
        if isinstance(existing_ext, dict):
            existing_ext.update(ext_dir)
        permission["external_directory"] = ext_dir

    # ── Output ────────────────────────────────────────────────────────
    report = {
        "timestamp": __import__("datetime").datetime.now().isoformat(timespec="minutes"),
        "project": {
            "path": str(project_dir),
            "type": project_type,
            "types": project_types_list,
            "frontend_framework": frontend_framework,
            "databases": sorted(project_dbs),
            "has_agents_md": agents_content is not None,
        },
        "agents_domains": agents_domains,
        "duplicates": duplicates,
        "mcp_ratings": dict(sorted(mcp_ratings.items())),
        "skill_ratings": dict(sorted(skill_ratings.items())),
        "safe_paths": safe_paths,
        "provider_findings": provider_findings,
        "feature_findings": feature_findings,
        "resource_findings": resource_findings,
        "safety_findings": safety_findings,
        "agent_findings": agent_findings,
        "agents_md_findings": agents_md_findings,
        "instructions_findings": instructions_findings,
        "custom_cmd_findings": custom_cmd_findings,
        "suggested_project_config": project_suggestion,
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()