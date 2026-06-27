#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# 微购设计系统 Skill — 一键安装脚本
# 支持: Codex / Claude Code / Trae (全部作为 Skill)
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/zhoujieh/wego-ux-design-skill/main/wego-ux-design/install.sh | bash
#   或本地执行: bash install.sh
# ============================================================

SKILL_NAME="wego-ux-design"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "/tmp")"
# 优先使用脚本所在目录作为源目录
SKILL_SRC_DIR="$SCRIPT_DIR"
# 如果脚本不在源目录，则保留为空触发自动发现
if [ ! -f "$SKILL_SRC_DIR/SKILL.md" ]; then
    SKILL_SRC_DIR=""
fi

# ---- 颜色 ----
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' NC=''
fi

# ---- 获取各平台安装路径 ----
get_platform_dir() {
    case "$1" in
        # Codex: Skill 安装到 ~/.codex/skills/
        codex)  echo "$HOME/.codex/skills/$SKILL_NAME" ;;
        # Claude Code: Skill 目录
        claude) echo "$HOME/.claude/skills/$SKILL_NAME" ;;
        # Trae: Skill 目录
        trae)   echo "$HOME/.trae-cn/skills/$SKILL_NAME" ;;
        *)      echo "" ;;
    esac
}

# ---- 帮助信息 ----
show_help() {
    echo "用法: bash install.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --all        安装到所有检测到的 AI 编码平台 (默认)"
    echo "  --codex      仅安装到 Codex"
    echo "  --claude     仅安装到 Claude Code"
    echo "  --trae       仅安装到 Trae"
    echo "  --update     强制覆盖更新"
    echo "  --uninstall  卸载所有平台的 skill"
    echo "  --help       显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  bash install.sh                    # 安装到所有已安装的平台"
    echo "  bash install.sh --codex --update   # 更新 Codex skill"
    echo "  bash install.sh --uninstall        # 卸载所有平台"
}

# ---- 检测已安装的平台 ----
detect_platforms() {
    local detected=""
    if command -v codex >/dev/null 2>&1 || [ -d "$HOME/.codex" ]; then
        detected="$detected codex"
    fi
    if command -v claude >/dev/null 2>&1 || [ -d "$HOME/.claude" ]; then
        detected="$detected claude"
    fi
    if [ -d "$HOME/.trae-cn" ]; then
        detected="$detected trae"
    fi
    echo "$detected" | sed 's/^ *//'
}

# ---- 验证 skill 源目录 ----
validate_source() {
    if [ ! -f "$SKILL_SRC_DIR/SKILL.md" ]; then
        echo "${RED}✗ 错误: 未找到 SKILL.md，请确保在正确的目录下运行此脚本${NC}"
        echo "   当前目录: $SKILL_SRC_DIR"
        exit 1
    fi
}

# ---- 安装到单个平台 ----
install_to_platform() {
    local platform="$1"
    local force="$2"
    local dest
    dest="$(get_platform_dir "$platform")"

    if [ -z "$dest" ]; then
        echo "  ${RED}未知平台: $platform${NC}"
        return 1
    fi

    echo "${CYAN}→ 正在安装到 ${platform}...${NC}"

    # Codex: 安装前清理旧插件位置
    if [ "$platform" = "codex" ]; then
        local old_plugin="$HOME/.codex/plugins/$SKILL_NAME"
        if [ -d "$old_plugin" ]; then
            echo "  ${YELLOW}检测到旧插件安装: ${old_plugin}${NC}"
            echo "  ${YELLOW}  → 已迁移到 skills 目录${NC}"
            rm -rf "$old_plugin"
        fi
        rm -rf "$HOME/.codex/skills/.system/$SKILL_NAME" 2>/dev/null || true
    fi

    if [ -d "$dest" ]; then
        if [ "$force" = "true" ]; then
            echo "  ${YELLOW}已存在，覆盖更新...${NC}"
            rm -rf "$dest"
        else
            echo "  ${YELLOW}已存在，跳过 (使用 --update 强制覆盖)${NC}"
            return 1
        fi
    fi

    mkdir -p "$(dirname "$dest")"
    cp -r "$SKILL_SRC_DIR" "$dest"

    # 清理不需要复制的文件 (skill 目录只需要 SKILL.md 和相关内容)
    rm -rf "$dest/.git" "$dest/.github" 2>/dev/null || true
    rm -f "$dest/install.sh" "$dest/uninstall.sh" 2>/dev/null || true

    echo "  ${GREEN}✓ 已安装到 ${dest}${NC}"
    return 0
}

# ---- 卸载单个平台 ----
uninstall_from_platform() {
    local platform="$1"
    local dest
    dest="$(get_platform_dir "$platform")"

    if [ -z "$dest" ]; then
        return
    fi

    if [ "$platform" = "codex" ]; then
        # 清理 skill 位置
        if [ -d "$dest" ]; then
            rm -rf "$dest"
            echo "  ${GREEN}✓ 已从 ${platform} 卸载 (${dest})${NC}"
        fi
        # 同时清理可能的旧插件位置
        if [ -d "$HOME/.codex/plugins/$SKILL_NAME" ]; then
            rm -rf "$HOME/.codex/plugins/$SKILL_NAME"
            echo "  ${YELLOW}  同时清理了旧插件位置${NC}"
        fi
        if [ -d "$HOME/.codex/skills/.system/$SKILL_NAME" ]; then
            rm -rf "$HOME/.codex/skills/.system/$SKILL_NAME"
            echo "  ${YELLOW}  同时清理了旧 .system 位置${NC}"
        fi
    else
        if [ -d "$dest" ]; then
            rm -rf "$dest"
            echo "  ${GREEN}✓ 已从 ${platform} 卸载 (${dest})${NC}"
        fi
    fi
}

# ---- 主逻辑 ----
main() {
    local targets=""
    local force=false
    local do_uninstall=false

    # 解析参数
    for arg in "$@"; do
        case "$arg" in
            --all)      targets="" ;;
            --codex)    targets="$targets codex" ;;
            --claude)   targets="$targets claude" ;;
            --trae)     targets="$targets trae" ;;
            --update)   force=true ;;
            --uninstall) do_uninstall=true ;;
            --help)     show_help; exit 0 ;;
            *)          echo "${RED}未知选项: $arg${NC}"; show_help; exit 1 ;;
        esac
    done
    targets="$(echo "$targets" | sed 's/^ *//;s/ *$//')"

    # 如果没有指定平台
    if [ -z "$targets" ]; then
        if [ "$do_uninstall" = true ]; then
            targets="codex claude trae"
        else
            targets="$(detect_platforms)"
        fi
    fi

    if [ -z "$targets" ]; then
        echo "${YELLOW}未检测到任何支持的平台 (Codex / Claude Code / Trae)${NC}"
        echo "请确认至少安装了其中一个。"
        exit 0
    fi

    # 自动定位源目录（兼容 curl | bash 场景）
    if [ ! -f "$SKILL_SRC_DIR/SKILL.md" ]; then
        # 先尝试常见克隆位置
        for d in             /tmp/wego-ux-design-skill/wego-ux-design             /tmp/codex/skill-install-*/wego-ux-design             "$(pwd)/wego-ux-design"             "wego-ux-design"; do
            [ -f "$d/SKILL.md" ] && SKILL_SRC_DIR="$d" && break
        done
        # 如果还是找不到，自动从 GitHub 下载
        if [ ! -f "$SKILL_SRC_DIR/SKILL.md" ]; then
            echo "${YELLOW}未找到本地源文件，正在从 GitHub 下载...${NC}"
            DOWNLOAD_DIR="/tmp/wego-ux-design-skill-$$"
            mkdir -p "$DOWNLOAD_DIR"
            if command -v git >/dev/null 2>&1; then
                git clone --depth 1 https://github.com/zhoujieh/wego-ux-design-skill.git "$DOWNLOAD_DIR" >/dev/null 2>&1 || true
                if [ -f "$DOWNLOAD_DIR/wego-ux-design/SKILL.md" ]; then
                    SKILL_SRC_DIR="$DOWNLOAD_DIR/wego-ux-design"
                fi
            fi
            # git 不可用则用 curl + unzip 兜底
            if [ ! -f "$SKILL_SRC_DIR/SKILL.md" ] && command -v curl >/dev/null 2>&1; then
                curl -fsSL "https://codeload.github.com/zhoujieh/wego-ux-design-skill/zip/main" -o "$DOWNLOAD_DIR/repo.zip" 2>/dev/null || true
                if [ -f "$DOWNLOAD_DIR/repo.zip" ] && command -v unzip >/dev/null 2>&1; then
                    unzip -qo "$DOWNLOAD_DIR/repo.zip" -d "$DOWNLOAD_DIR" 2>/dev/null || true
                    if [ -f "$DOWNLOAD_DIR/wego-ux-design-skill-main/wego-ux-design/SKILL.md" ]; then
                        SKILL_SRC_DIR="$DOWNLOAD_DIR/wego-ux-design-skill-main/wego-ux-design"
                    fi
                fi
            fi
        fi
    fi

    validate_source

    if [ "$do_uninstall" = true ]; then
        echo "${CYAN}╔══════════════════════════════════════╗${NC}"
        echo "${CYAN}║   微购设计系统 Skill — 卸载          ║${NC}"
        echo "${CYAN}╚══════════════════════════════════════╝${NC}"
        echo ""
        for platform in $targets; do
            uninstall_from_platform "$platform"
        done
        echo ""
        echo "${GREEN}卸载完成。如需重新安装，运行: bash install.sh${NC}"
    else
        echo "${CYAN}╔══════════════════════════════════════╗${NC}"
        echo "${CYAN}║   微购设计系统 Skill — 安装          ║${NC}"
        echo "${CYAN}╚══════════════════════════════════════╝${NC}"
        echo ""
        echo "Skill: $SKILL_NAME"
        echo "来源: $SKILL_SRC_DIR"
        if [ "$force" = "true" ]; then
            echo "模式: 强制覆盖更新"
        fi
        echo ""

        local installed=0
        for platform in $targets; do
            if install_to_platform "$platform" "$force"; then
                installed=$((installed + 1))
            fi
        done

        echo ""
        if [ $installed -gt 0 ]; then
            echo "${GREEN}════════════════════════════════════════${NC}"
            echo "${GREEN}  安装完成!${NC}"
            echo "${GREEN}════════════════════════════════════════${NC}"
            echo ""
            echo "使用方式 (自然语言，在任意项目中):"
            echo "  \"帮我设计一个微购的商品列表页\""
            echo "  \"生成一个微购风格的登录页面\""
            echo "  \"审查这个页面的设计合规性\""
        else
            echo "${YELLOW}没有新的安装。使用 --update 来覆盖已存在的安装。${NC}"
        fi
    fi
}

main "$@"
