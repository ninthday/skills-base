---
name: nice-commit
description: Use when the user asks to write, generate, or suggest a commit message for current Git changes. Defaults to a Traditional Chinese Conventional Commit.
metadata:
  author: ninthday
  version: "2026.07.26"
---

# Git Commit Message Guidelines

First read `references/conventional-commits.md`, which is the source of truth for Conventional Commits structure, footers, and breaking-change rules. This skill only analyzes changes and generates messages. Do not run `git add`, `git commit`, change Git configuration, or perform any other operation that modifies Git state.

## Analyze Changes

Follow this process in order:

1. Run `git diff --cached` first.
2. If staged changes exist, generate the message exclusively from them. Do not read, mix in, or describe unstaged changes.
3. If there are no staged changes, run `git diff` and `git status --short`, then generate the message from the unstaged diff and status.
4. Read the contents of untracked source, configuration, manifest, documentation, and test files before judging them. Binary assets, lockfiles, and dependency artifacts may be inferred from their names or paths unless their purpose changes the message subject.
5. Base the subject in this order: known conversational intent, observable result of the changes, then implementation details. Do not invent motivation, behavior, or functionality unsupported by the diff.

If there are no describable changes, the directory is not a Git worktree, or several independent changes cannot be honestly summarized in one commit, stop and ask the user to provide the changes, choose one logical unit, or stage that unit first.

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

Use a scope only when the changes clearly belong to one concisely named module. Omit it for cross-module changes or when no clear name exists. Descriptions must be imperative and no longer than 50 characters.

When the change definitely removes a public API or supported behavior, use `<type>[optional scope]!: <description>`. Add `BREAKING CHANGE: <description>` after a blank line only when the user explicitly asks for a multi-line message or footer. Never add a body or footer automatically, even for complex changes.

## Format Selection and Output

Choose the format using this precedence:

1. If the user explicitly asks for both English and Conventional Commits, output `<type>[optional scope]: <English imperative description>` in fewer than 72 characters.
2. If the user explicitly asks for English, output an English imperative sentence without a prefix in fewer than 72 characters.
3. If the user explicitly asks for “no prefix” or a “plain commit title,” output an imperative sentence without a prefix. Use English unless the user specifies another language.
4. If the user explicitly requests another format, follow it without contradicting the observed changes.
5. Without an explicit format request, use the default Traditional Chinese Conventional Commit format above.

On success, output only the final commit message: no explanation, preface, list, or Markdown code fence. Output a multi-line Conventional Commit only when the user explicitly requests a body or footer.

## Examples

- Good (default): `feat(auth): <Traditional Chinese imperative description>`
- Good (English): `Validate login input before submitting credentials`
- Good (English Conventional Commits): `fix(auth): Validate login input before submitting credentials`
- Bad: `update code`
