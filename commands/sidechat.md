---
description: "Quick reference for OpenCode-SideChat: floating side-chat panel for queries alongside your main session. Toggle via Alt+N, configurable position, history viewer, isolated agent."
---

## Quick Reference

| Keybind | Action |
|---------|--------|
| `Alt+N` | Abre/fecha o painel lateral |
| `Alt+C` | Limpa o chat / nova sessão |
| `Alt+T` | Mostra/esconde blocos de thinking |
| `Alt+H` | Abre visualizador de histórico |
| `Alt+D` | Deleta entrada selecionada (no histórico) |
| `Tab` | Alterna modelo |

## Config

`~/.config/opencode/sidechat.jsonc`:

```jsonc
{
  "model": null,
  "systemPrompt": "...",
  "keybind": "alt+n",
  "clearKeybind": "alt+c",
  "thinkToggleKeybind": "alt+t",
  "allowedTools": ["...", "..."],
  "width": 70,
  "transcriptHeight": 20,
  "tokenLimit": 45000,
  "position": "bottom-right",
  "think": {
    "defaultState": "collapsed",
    "showSummary": false
  }
}
```

Posições: `bottom-right`, `bottom-left`, `top-left`, `top-right`.

## Details

- Agente isolado da sessão principal (read-only tools, deny-by-default)
- Sessões são salvas automaticamente ao fechar o painel ou limpar o chat
- Histórico: até 50 entradas (FIFO) em `~/.local/share/opencode-sidechat/history.json`
- Para instalar: `npm install -g opencode-sidechat` + adicionar `"opencode-sidechat"` ao `~/.config/opencode/tui.json`
