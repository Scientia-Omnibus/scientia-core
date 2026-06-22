#!/usr/bin/env bash
set -euo pipefail

APP="scientia-core"
APP_PYPI="scientia-core"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

info()  { printf "${CYAN}::${NC} %s\n" "$*"; }
ok()    { printf "${GREEN}==>${NC} %s\n" "$*"; }
warn()  { printf "${YELLOW}==>${NC} %s\n" "$*"; }

run_with_spinner() {
    local pid=$1 msg=$2
    local spin='-\|/'
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        printf "\r${MAGENTA}::${NC} %s ${MAGENTA}%c${NC}" "$msg" "${spin:$i:1}"
        i=$(( (i+1) % 4 ))
        sleep 0.1
    done
    printf "\r${GREEN}::${NC} %s ${GREEN}done${NC}\n" "$msg"
}

install_git_if_missing() {
    if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
        echo "Windows support coming soon. Install Git from https://git-scm.com and run: uv tool install scientia-core"
        exit 1
    fi
    if command -v git &>/dev/null; then
        ok "Git already installed ($(git --version))"
        return 0
    fi
    warn "Git not found — installing..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        arch=$(uname -m)
        case "$arch" in
            x86_64)  url="https://github.com/ryanwoodsmall/static-git/releases/download/v2.47.1/git-linux-amd64-static.tar.gz" ;;
            aarch64) url="https://github.com/ryanwoodsmall/static-git/releases/download/v2.47.1/git-linux-arm64-static.tar.gz"  ;;
            *)       echo "Error: unsupported arch ($arch). Install git manually: https://git-scm.com"; exit 1 ;;
        esac
        mkdir -p "$HOME/.local/bin"
        info "Downloading git..."
        curl -# -fL "$url" | tar xz -C "$HOME/.local/bin"
        export PATH="$HOME/.local/bin:$PATH"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &>/dev/null; then
            brew install git > /dev/null 2>&1 &
            run_with_spinner $! "Installing git via Homebrew"
            wait $! 2>/dev/null || true
        else
            echo "Error: install Git manually: https://git-scm.com"
            exit 1
        fi
    else
        echo "Error: unsupported OS ($OSTYPE). Install git manually: https://git-scm.com"
        exit 1
    fi

    if ! command -v git &>/dev/null; then
        echo "Error: git installation failed."
        exit 1
    fi
    ok "Git installed ($(git --version))"
}

install_uv_if_missing() {
    if command -v uv &>/dev/null; then
        ok "uv already installed ($(uv --version))"
        return 0
    fi
    warn "uv not found — installing..."
    info "Downloading uv..."
    curl -# -fL https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv &>/dev/null; then
        echo "Error: uv installation failed. Add ~/.local/bin to PATH or install manually."
        exit 1
    fi
    ok "uv installed ($(uv --version))"
}

main() {
    echo ""
    printf "  ${CYAN}╭─────────────────────────────────────╮${NC}\n"
    printf "  ${CYAN}│${NC}  Installing ${GREEN}%s${NC}           ${CYAN}│${NC}\n" "$APP"
    printf "  ${CYAN}╰─────────────────────────────────────╯${NC}\n"
    printf "\n"

    install_git_if_missing
    install_uv_if_missing

    info "Installing $APP via uv..."
    uv tool install "$APP_PYPI" > /dev/null 2>&1 &
    run_with_spinner $! "Installing $APP with uv"
    wait $! 2>/dev/null || true

    echo ""
    ok "$APP installed! Run: $APP"
    echo ""
}

main "$@"
