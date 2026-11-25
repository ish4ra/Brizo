#!/usr/bin/env bash
# Grant user namespaces to ONE Firefox install path, the same way Ubuntu's own
# firefox AppArmor profile does (flags=(unconfined) + userns). This ENABLES
# Firefox's namespace sandbox layer on hosts that set
# kernel.apparmor_restrict_unprivileged_userns=1; it does not relax anything else.
#   install-apparmor-profile.sh <app-dir-containing-firefox-binary>
set -euo pipefail
APP="$(cd "$1" && pwd -P)"
PROFILE=/etc/apparmor.d/brizo-experiment
sudo tee "$PROFILE" >/dev/null <<PROF
abi <abi/4.0>,
include <tunables/global>
profile brizo-experiment "${APP}/{firefox,firefox-bin,glxtest,vaapitest,pingsender}" flags=(unconfined) {
  userns,
}
PROF
sudo apparmor_parser -r "$PROFILE"
echo "AppArmor profile loaded for ${APP}"
