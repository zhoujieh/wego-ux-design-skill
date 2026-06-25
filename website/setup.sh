#!/bin/bash
# Wego Design System Website — 资源同步脚本
# 从 wego-ux-design/ 复制 tokens.css 和字体文件到 website/

set -e
SKILL_DIR="$(cd "$(dirname "$0")/../wego-ux-design" && pwd)"
SITE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> 复制 tokens.css ..."
cp "$SKILL_DIR/02-tokens/tokens.css" "$SITE_DIR/styles/tokens.css"

echo "==> 复制字体文件 ..."
cp "$SKILL_DIR/resources/fonts/WegoKeyboardN9-Regular.otf" "$SITE_DIR/assets/fonts/"
cp "$SKILL_DIR/resources/fonts/WegoKeyboardN9-Medium.otf" "$SITE_DIR/assets/fonts/"
cp "$SKILL_DIR/resources/fonts/WegoKeyboardN9-Bold.otf" "$SITE_DIR/assets/fonts/"

echo "==> 复制 iconfont ..."
cp "$SKILL_DIR/resources/fonts/iconfont/"* "$SITE_DIR/assets/fonts/iconfont/"

echo ""
echo "✅ 同步完成！"
echo "运行: cd website && npm install && npm run dev"
echo "然后在浏览器打开 http://localhost:3000"
