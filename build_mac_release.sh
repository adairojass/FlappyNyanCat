#!/usr/bin/env bash
set -euo pipefail

./build_mac.sh
./scripts/package_macos_dmg.sh

echo "Release artifacts ready in dist/:"
echo "- FlappyNyanCat.app"
echo "- FlappyNyanCat-macOS.dmg"
