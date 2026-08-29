#!/usr/bin/env bash
# Source from bootstrap.sh. Provisions Node 18+ + npm when missing so
# designers do not need a pre-installed toolchain. No sudo.
# Keep in sync with partner-prototype/scripts/ensure-toolchain.sh

# PARENT must be set by the caller (IMPACT_PROTOTYPE_HOME / --parent).
IMPACT_NODE_VERSION="${IMPACT_NODE_VERSION:-v22.14.0}"

if ! declare -f die >/dev/null; then
  die() { echo "ERROR: $*" >&2; exit 1; }
fi
if ! declare -f info >/dev/null; then
  info() { echo "→ $*"; }
fi

_impact_augment_path() {
  export PATH="/opt/homebrew/bin:/usr/local/bin:${HOME}/.local/bin:${PATH}"
  if [[ -d "${HOME}/.volta/bin" ]]; then
    export PATH="${HOME}/.volta/bin:${PATH}"
  fi
  if [[ -d "${HOME}/.fnm" ]]; then
    export PATH="${HOME}/.fnm:${PATH}"
  fi
  if [[ -d "${HOME}/.local/share/fnm" ]]; then
    export PATH="${HOME}/.local/share/fnm:${PATH}"
  fi
  if command -v fnm >/dev/null 2>&1; then
    eval "$(fnm env --shell bash 2>/dev/null)" || true
  fi
  if [[ -s "${HOME}/.nvm/nvm.sh" ]]; then
    # shellcheck disable=SC1091
    . "${HOME}/.nvm/nvm.sh"
  fi
  if [[ -s "${HOME}/.asdf/asdf.sh" ]]; then
    # shellcheck disable=SC1091
    . "${HOME}/.asdf/asdf.sh"
  fi
  if [[ -n "${PARENT:-}" && -d "${PARENT}/.toolchain" ]]; then
    local d
    for d in "${PARENT}/.toolchain"/node-v*/; do
      [[ -x "${d}bin/node" ]] && export PATH="${d}bin:${PATH}"
    done
  fi
}

_impact_node_ok() {
  command -v node >/dev/null 2>&1 || return 1
  command -v npm >/dev/null 2>&1 || return 1
  local major
  major="$(node -p "process.versions.node.split('.')[0]" 2>/dev/null)" || return 1
  [[ "${major}" -ge 18 ]]
}

_impact_platform() {
  local os arch
  os="$(uname -s)"
  arch="$(uname -m)"
  case "${os}" in
    Darwin)
      case "${arch}" in
        arm64) echo "darwin-arm64" ;;
        x86_64) echo "darwin-x64" ;;
        *) return 1 ;;
      esac
      ;;
    Linux)
      case "${arch}" in
        x86_64) echo "linux-x64" ;;
        aarch64|arm64) echo "linux-arm64" ;;
        *) return 1 ;;
      esac
      ;;
    *) return 1 ;;
  esac
}

_impact_download() {
  local url="$1" dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 3 --retry-delay 2 "${url}" -o "${dest}"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "${url}" -O "${dest}"
  else
    die "Need curl or wget to download Node automatically.
Install Node 18+ from https://nodejs.org then re-run."
  fi
}

impact_ensure_node() {
  [[ -n "${PARENT:-}" ]] || die "ensure-toolchain: PARENT is not set"
  mkdir -p "${PARENT}"
  _impact_augment_path
  if _impact_node_ok; then
    info "Using Node $(node -v) ($(command -v node)) and npm $(npm -v)"
    return 0
  fi

  info "Node 18+ not on PATH — installing a local copy (no sudo, no Homebrew required)…"
  local plat
  plat="$(_impact_platform)" || die "Cannot auto-install Node on this OS/arch ($(uname -s) $(uname -m)).
Install Node 18+ from https://nodejs.org then re-run."

  local ver="${IMPACT_NODE_VERSION}"
  local dest="${PARENT}/.toolchain/node-${ver}"
  mkdir -p "${PARENT}/.toolchain"

  if [[ ! -x "${dest}/bin/node" ]]; then
    local tarball="node-${ver}-${plat}.tar.gz"
    local url="https://nodejs.org/dist/${ver}/${tarball}"
    local tmp
    tmp="$(mktemp -d)"
    info "Downloading ${url}"
    if ! _impact_download "${url}" "${tmp}/${tarball}"; then
      rm -rf "${tmp}"
      die "Failed to download Node from ${url}
Install Node 18+ from https://nodejs.org then re-run."
    fi
    tar -xzf "${tmp}/${tarball}" -C "${tmp}"
    rm -rf "${dest}"
    mv "${tmp}/node-${ver}-${plat}" "${dest}"
    rm -rf "${tmp}"
  fi

  export PATH="${dest}/bin:${PATH}"
  if ! _impact_node_ok; then
    die "Local Node at ${dest} did not work. Install Node 18+ from https://nodejs.org then re-run."
  fi
  info "Provisioned Node $(node -v) at ${dest}"
}

impact_verify_vite() {
  if [[ ! -f package.json ]]; then
    return 0
  fi
  if grep -q '"vite"' package.json; then
    if [[ ! -e node_modules/vite && ! -e node_modules/.bin/vite ]]; then
      die "Vite did not install into node_modules.
Re-run this skill with sandbox off / full permissions (Cursor: required_permissions [\"all\"]).
If it still fails, check network / VPN and re-run."
    fi
    info "Vite is installed ($(node -p "require('./node_modules/vite/package.json').version" 2>/dev/null || echo present))"
  fi
}
