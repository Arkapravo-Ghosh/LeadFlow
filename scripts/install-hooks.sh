#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
git -C "$root" config core.hooksPath "$root/.githooks"
for app in frontend backend; do git -C "$root/$app" config core.hooksPath "$root/.githooks"; done
