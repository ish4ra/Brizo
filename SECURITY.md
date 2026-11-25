# Security Policy

## Current status

Brizo has **no released software**. There is no browser build to attack yet.
The repository holds documentation and asset tooling only.

## Reporting a vulnerability

If you find a security problem in this repository (for example in the build
scripts, CI workflows or a dependency), please report it privately using
GitHub's **"Report a vulnerability"** button (private security advisories)
on the repository's *Security* tab. Do not open a public issue.

Please include the affected file or component, reproduction steps and impact.
The project is maintained by volunteers, so response times are best-effort.

## Security principles for future development

- Sandboxing, site isolation, certificate validation and update signature
  verification are never disabled or weakened, including to save memory.
- Upstream engine security fixes must be tracked and shipped promptly.
- Extensions run under an explicit, least-privilege permission model.
- No secrets in the repository. CI uses GitHub's encrypted secrets only when
  necessary, with minimal workflow `permissions`.

## Supported versions

None yet. This section will list supported releases once they exist.
