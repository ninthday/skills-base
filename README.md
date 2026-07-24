# Lucas Yang's Skills

[Agent skills](https://agentskills.io/) built around [Lucas Yang](https://github.com/ycs77)'s personal preferences and development style.

## Installation

Install using the `skills` CLI with the all skills:

```bash
npx skills add ycs77/skills --skill='*'
# To install all skills globally:
npx skills add ycs77/skills --skill='*' -g
```

## Skills

### Self-maintained Skills

| Name | Description |
|------|-------------|
| [commit-message](./skills/commit-message/SKILL.md) | Generate concise Git commit messages |
| [github-release-notes](./skills/github-release-notes/SKILL.md) | Generate GitHub release notes following Keep a Changelog spec |
| [scan-repo](./skills/scan-repo/SKILL.md) | Security scan of GitHub open source projects |
| [scan-skill](./skills/scan-skill/SKILL.md) | Security auditing tool for scanning skills |
| [write-social-post](./skills/write-social-post/SKILL.md) | Write strategic social media posts for articles, trends, news, or tech commentary |
| [ycs77-vue](./skills/ycs77-vue/SKILL.md) | Lucas Yang's Vue 3 conventions |

### Vendored Skills

Synced from external repositories that maintain their own skills.

| Skill | Description | Source |
|-------|-------------|--------|
| [grill-me](skills/grill-me) | Interview the user relentlessly to stress-test a plan or design | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [grill-with-docs](skills/grill-with-docs) | Grill a plan against the domain model, updating docs and ADRs inline | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [tdd](skills/tdd) | Test-driven development with the red-green-refactor loop | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [diagnose](skills/diagnose) | Disciplined diagnosis loop for hard bugs and performance regressions | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [zoom-out](skills/zoom-out) | Zoom out for broader context and a higher-level map of the code | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [improve-codebase-architecture](skills/improve-codebase-architecture) | Find deepening opportunities to make a codebase more testable and AI-navigable | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [caveman](skills/caveman) | Ultra-compressed communication mode that cuts token usage ~75% | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [handoff](skills/handoff) | Compact the conversation into a handoff document for another agent | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [prototype](skills/prototype) | Build a throwaway prototype to flesh out a design before committing | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [write-a-skill](skills/write-a-skill) | Create new agent skills with proper structure and progressive disclosure | [mattpocock/skills](https://github.com/mattpocock/skills) |

## Usage

### Vue Projects

First, install the required skills:

```bash
npx skills add antfu/skills \
  --skill vue \
  --skill vue-best-practices \
  --skill nuxt  # For Nuxt projects
```

Then add the following to `AGENTS.md` (or `CLAUDE.md`) in your project root to ensure the AI assistant loads the correct skills when working with Vue 3 SFCs:

```md
## Skills Activation Rules

`ycs77-vue` is the project-level convention. When rules conflict, `ycs77-vue` takes precedence.

- **When writing, modifying, or reviewing Vue 3 SFCs**, load ALL of the following skills:
  1. `vue`
  2. `vue-best-practices`
  3. `ycs77-vue`
```

> For Nuxt projects, also include `nuxt` in the list above.

## Generate Skills

1. Clone this repository
2. Install dependencies: `uv sync`
3. Update `meta.py` with your own projects and skill sources
4. Run `uv run skills-manager cleanup --yes` to remove existing submodules and skills
5. Run `uv run skills-manager init` to clone the submodules
6. Run `uv run skills-manager sync` to sync vendored skills
7. Ask your agent to `Generate skills for <project>` (recommended one at a time to manage token usage)

See [AGENTS.md](AGENTS.md) for detailed generation guidelines.

## Credits

- The Skills Generator and CLI are adapted from [antfu/skills](https://github.com/antfu/skills) — thanks [Anthony Fu](https://github.com/antfu)

## Author

Lucas Yang (yangchenshin77@gmail.com)

## License

[MIT License](LICENSE)
