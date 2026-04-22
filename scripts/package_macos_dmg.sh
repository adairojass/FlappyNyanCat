#!/usr/bin/env bash
set -euo pipefail

APP_NAME="FlappyNyanCat"
APP_PATH="dist/${APP_NAME}.app"
DMG_STAGING="build/dmg"
DMG_NAME="FlappyNyanCat-macOS.dmg"

if [[ ! -d "$APP_PATH" ]]; then
  echo "App not found at $APP_PATH. Run build first." >&2
  exit 1
fi

rm -rf "$DMG_STAGING"
mkdir -p "$DMG_STAGING"
cp -R "$APP_PATH" "$DMG_STAGING/"
ln -s /Applications "$DMG_STAGING/Applications"

hdiutil create \
  -volname "$APP_NAME" \
  -srcfolder "$DMG_STAGING" \
  -ov \
  -format UDZO \
  "dist/${DMG_NAME}"

echo "DMG created at dist/${DMG_NAME}"
