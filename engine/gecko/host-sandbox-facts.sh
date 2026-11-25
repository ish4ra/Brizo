#!/usr/bin/env bash
# Record host facts that determine Firefox's Linux sandbox capabilities.
for k in kernel.apparmor_restrict_unprivileged_userns kernel.unprivileged_userns_clone user.max_user_namespaces kernel.yama.ptrace_scope; do
  printf '%s = %s\n' "$k" "$(sysctl -n "$k" 2>/dev/null || echo n/a)"
done
uname -r
grep -E '^(Seccomp|NoNewPrivs)' /proc/self/status || true
