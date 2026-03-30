#!/bin/bash

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.config/opencode"

echo "Sincronizando de: $SOURCE_DIR"
echo "Para: $TARGET_DIR"

mkdir -p "$TARGET_DIR"

cp -r "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/"
cp -r "$SOURCE_DIR/agents" "$TARGET_DIR/"
cp -r "$SOURCE_DIR/commands" "$TARGET_DIR/"
cp -r "$SOURCE_DIR/rules" "$TARGET_DIR/"
cp -r "$SOURCE_DIR/skills" "$TARGET_DIR/"
cp -r "$SOURCE_DIR/opencode.json" "$TARGET_DIR/"

echo "Sincronização concluída!"
