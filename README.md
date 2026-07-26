# Tuvix Shih (ninthday) Skills

[Agent Skills](https://agentskills.io/) curated by [Tuvix Shih](https://github.com/ninthday) for practical software development workflows.

## Installation

Install every packaged skill:

```bash
npx skills@latest add ninthday/skills-base --skill='*'
```

Install them globally:

```bash
npx skills@latest add ninthday/skills-base --skill='*' -g
```

## Skills

### Vendored Skills

The following skills are currently packaged in `skills/`.

| Skill | Description | Source |
|-------|-------------|--------|
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | Stress-test a plan or design while creating ADRs and glossary entries. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [grilling](skills/grilling/SKILL.md) | Relentlessly question a plan, decision, or idea to expose unresolved assumptions. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [domain-modeling](skills/domain-modeling/SKILL.md) | Build and refine a project's domain model, terminology, and architectural decisions. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [tdd](skills/tdd/SKILL.md) | Build features and fixes with a test-driven development workflow. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | Apply a disciplined diagnosis loop to bugs and performance regressions. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | Identify codebase deepening opportunities and present them in a visual report. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [prototype](skills/prototype/SKILL.md) | Build a throwaway prototype to answer a design question. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [to-spec](skills/to-spec/SKILL.md) | Synthesize the current conversation into a specification and publish it to the issue tracker. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [handoff](skills/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [writing-great-skills](skills/writing-great-skills/SKILL.md) | Apply predictable vocabulary and principles when writing or editing skills. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [chinese-content-writing-guideline](skills/chinese-content-writing-guideline/SKILL.md) | Write and review Traditional Chinese content using Taiwan terminology and conventions. | [jim60105/copilot-prompt](https://github.com/jim60105/copilot-prompt) |
| [drawio-diagrams-enhanced](skills/drawio-diagrams-enhanced/SKILL.md) | Create draw.io diagrams, including flowcharts, UML, WBS, and RACI matrices. | [jim60105/copilot-prompt](https://github.com/jim60105/copilot-prompt) |
| [python-security](skills/python-security/SKILL.md) | Design, implement, and verify secure Python applications following OWASP guidance. | [jim60105/copilot-prompt](https://github.com/jim60105/copilot-prompt) |
| [git-commit](skills/git-commit/SKILL.md) | Analyze changes, stage them logically, and create Conventional Commits. | [github/awesome-copilot](https://github.com/github/awesome-copilot) |
| [readme-blueprint-generator](skills/readme-blueprint-generator/SKILL.md) | Generate repository README files from project documentation and conventions. | [github/awesome-copilot](https://github.com/github/awesome-copilot) |

## Usage

Install one skill by name:

```bash
npx skills@latest add ninthday/skills-base --skill=git-commit
```

Once installed, your agent loads a skill when its description matches the task. Review the skill's `SKILL.md` for its trigger conditions and workflow.

## Generate Skills

1. Clone this repository.
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Configure skill sources in `meta.py`.
4. Initialize configured Git submodules:

   ```bash
   uv run skills-manager init --yes
   ```

5. Sync vendored skills from the initialized submodules:

   ```bash
   uv run skills-manager sync
   ```

6. For generated source projects, create or update skills according to [AGENTS.md](AGENTS.md).

## Archived Vendored Skills

When a vendored skill is removed upstream, `skills-manager` will not delete it. Instead, the next `check` or `sync` records the disappearance, then archives the local copy so the history is preserved.

### Detection

`uv run skills-manager check` always fetches the remote tracking ref before reporting. Any configured vendor source whose `skills/<source>` directory is gone from `@{u}` is listed in an `Invalid vendor skills:` block, e.g.:

```text
All submodules are up to date
Invalid vendor skills:
- example-skill: vendor/example/skills/engineering/example
```

`check` still exits `0`; it is purely informational.

### Archiving

`uv run skills-manager sync` runs the same detection against the updated working tree. For every missing source it:

1. Appends `- **Upstream Removed:** <timestamp>` to the skill's `SYNC.md` (UTC `YYYYMMDDTHHMMSSZ`). If a previous archive already recorded the removal timestamp, that timestamp is reused so the snapshot is idempotent.
2. Moves the active `skills/<output>/` directory to `archived-skills/<output>/<timestamp>/`. If a destination with that timestamp already exists, a `-2`, `-3`, … suffix is appended — archives are never overwritten.
3. Prints `Archived invalid vendor skill: <output> → archived-skills/<output>/<timestamp>`.

Running `sync` again on a still-missing source prints `Already archived invalid vendor skill: <output>` and leaves the archive untouched:

```text
Archived invalid vendor skill: example-skill → archived-skills/example-skill/20260725T120000Z
```

If the active output is missing but no archive exists yet, `sync` reports `Invalid vendor skill has no local output: <output>` and does not create an empty directory.

### Behaviour guarantees

- Historical archives are immutable. If the upstream skill reappears later, the normal sync flow recreates `skills/<output>/`; the previous archive is never overwritten or removed.
- `uv run skills-manager cleanup --yes` only inspects `skills/` for entries not declared in `meta.py`. The `archived-skills/` directory is never listed for removal.


## Credits

- The Skills Manager CLI is adapted from [antfu/skills](https://github.com/antfu/skills) — thanks [Anthony Fu](https://github.com/antfu).

## Author

Tuvix Shih (tuvix@ninthday.info)

## License

[GNU Free Documentation License 1.3](LICENSE.md)
