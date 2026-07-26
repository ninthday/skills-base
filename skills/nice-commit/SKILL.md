---
name: nice-commit
description: Use when the user asks to commit staged Git changes with a Conventional Commit. Analyze staged changes, propose a message, then execute git commit only after explicit confirmation. Defaults to a Traditional Chinese Conventional Commit.
metadata:
  author: Tuvix Shih
  version: "2026.07.26"
---

# Git Commit Message Guidelines

First read `references/conventional-commits.md`, the source of truth for Conventional Commits structure, footers, and breaking-change rules. Run `git commit` only after the user confirms the current proposed message for an unchanged staged snapshot, and follow the Git Safety Protocol below at all times.

## Git Safety Protocol

These rules are absolute and are not relaxed by any user request. This skill's only state-changing action is `git commit` on already-staged changes.

- NEVER change Git configuration.
- NEVER stage changes or touch anything not already staged (`git add` is forbidden).
- NEVER run destructive or history-rewriting commands (`--force`, `reset --hard`, `rebase`, `filter-branch`), and never push or force-push to any branch, including `main` and `master`.
- NEVER use `--no-verify`, or amend, reset, or otherwise alter existing commits.
- NEVER switch or check out branches; commit only on the current branch.
- NEVER override commit identity or timestamps (`--author`, `--date`).
- If a commit is rejected, for example by a hook, return Git's error and stop. Never amend; a fix requires the user to re-stage and re-confirm, producing a NEW commit.
- If the staged diff appears to contain secrets or credentials (keys, tokens, passwords), warn the user and do not commit until they explicitly confirm.

## Analyze Changes

Follow this process in order:

1. Run `git diff --cached`.
2. If it fails, return Git's error output and stop.
3. If it is empty, output exactly `No staged changes. Stage one logical change, then invoke this skill again.` Do not inspect or summarize `git diff`, Git status, or untracked files, and do not stage anything.
4. If it is non-empty, store the exact diff as the proposal snapshot and generate the message only from it. Ignore unstaged and untracked changes entirely.
5. Base the subject in this order: known conversational intent, observable result of the staged changes, then implementation details. Do not invent motivation, behavior, or functionality unsupported by the diff.

If several independent staged changes cannot be honestly summarized in one commit, stop and ask the user to stage one logical unit first.

## Types and Default Format

By default, output exactly one line:

`<type>[optional scope]: <Traditional Chinese imperative description>`

- `feat`: Add user-facing functionality.
- `fix`: Correct faulty behavior.
- `docs`: Change documentation only.
- `style`: Change formatting or code style without affecting logic.
- `refactor`: Restructure code without adding a feature or fixing a bug.
- `perf`: Improve performance.
- `test`: Add or modify tests.
- `build`: Change the build system, dependencies, or external tooling.
- `ci`: Change continuous-integration configuration or scripts.
- `chore`: Perform maintenance not covered by another type.
- `revert`: Revert a previous commit.

Use a scope only when the changes clearly belong to one concisely named module; omit it for cross-module changes or when no clear name exists. Descriptions must be imperative. Measure the whole subject line, including the `<type>[scope]:` prefix, and keep it to 50 characters or fewer; because full-width Chinese characters are dense, aim for about 25 or fewer in the default Traditional Chinese format.

When the change definitely removes a public API or supported behavior, use `<type>[optional scope]!: <description>`. Add `BREAKING CHANGE: <description>` after a blank line only when the user explicitly asks for a multi-line message or footer. Never add a body or footer automatically.

For a `revert`, use `revert: <description>` naming what is undone. Only when the user asks for a multi-line message and the reverted commit's short SHA is known, add `This reverts commit <SHA>.` as the body. Never fabricate the SHA.

## Format Selection, Proposal, and Confirmation

Choose the format using this precedence:

1. If the user explicitly asks for both English and Conventional Commits, use `<type>[optional scope]: <English imperative description>` in fewer than 72 characters.
2. If the user explicitly asks for English, use an English imperative sentence without a prefix in fewer than 72 characters.
3. If the user explicitly asks for “no prefix” or a “plain commit title,” use an imperative sentence without a prefix. Use English unless the user specifies another language.
4. If the user explicitly requests another format, follow it without contradicting the observed staged changes.
5. Without an explicit format request, use the default Traditional Chinese Conventional Commit format above.

Output a multi-line Conventional Commit only when the user explicitly requests a body or footer, and preserve the message exactly, including blank lines and paragraphs.

For every non-empty staged snapshot, render exactly:

Proposed commit message:
```
<complete final message>
```
Reply `yes` to commit only these staged changes, or provide a revised message.

No state-changing command may run before a separate response. Treat only an unambiguous affirmative to the current proposal, such as `yes`, as authorization; any refusal, ambiguity, or other response leaves Git unchanged.

If the user supplies a replacement message, verify it is supported by the stored staged diff. If supported, render it with the same template and require fresh confirmation. If not, explain the mismatch, generate a supported replacement, render it with the template, and do not commit.

After authorization, run `git diff --cached` again and compare it verbatim with the stored snapshot. If it fails, return Git's error output and require a new proposal once the issue is resolved. If it differs or is empty, output `The staged changes changed after the message was proposed. A new confirmation is required.`, regenerate the proposal from the current staged diff when non-empty, and render the template again. Do not commit.

If the snapshot is identical, run `git commit` without `--no-verify`, passing the full confirmed message through a single `-m`. Use a single-line `-m` for a subject-only message and a quoted heredoc for a multi-line one, so the exact blank lines, paragraphs, and footers are preserved verbatim:

```bash
# Single line
git commit -m "<type>[scope]: <description>"

# Multi-line with body/footer
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

<optional footer>
EOF
)"
```

The quoted `<<'EOF'` delimiter prevents shell expansion, keeping backticks, `$`, and `!` literal. On success, run `git rev-parse --short HEAD` and output exactly `Committed <short SHA>: <subject>`. If Git rejects the commit, return its error and do not claim success.

## Examples

Initial proposal:

Proposed commit message:
```
docs(nice-commit): 新增已暫存變更確認提交流程
```
Reply `yes` to commit only these staged changes, or provide a revised message.

User reply: `yes`

Successful result:

`Committed a1b2c3d: docs(nice-commit): 新增已暫存變更確認提交流程`
