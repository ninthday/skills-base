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

## Credits

- The Skills Manager CLI is adapted from [antfu/skills](https://github.com/antfu/skills) — thanks [Anthony Fu](https://github.com/antfu).

## Author

Tuvix Shih (tuvix@ninthday.info)

## License

[GNU Free Documentation License 1.3](LICENSE.md)
