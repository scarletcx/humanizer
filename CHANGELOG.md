# Changelog

## 2.11.2 - fork packaging (2026-10-22)

- Repackaged the skill under `skills/humanizer/` for cross-agent installation.
- Updated install URLs to `scarletcx/humanizer`.
- Moved the Claude plugin manifests to the repository root and pointed the
  manifest at `./skills/humanizer`.
- Added a package validator, tests, and a CI workflow.
- Added a root README, a Chinese README, and a source/licensing notice.
- No changes to the 35 patterns or the skill's behavior.
