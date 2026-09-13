# nice-llm-wiki

**A reusable skill for building Karpathy-style LLM wikis with Claude Code, Cursor, Codex, and other Agent Skills tools.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


`nice-llm-wiki` packages [Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) into one installable [Agent Skills](https://agentskills.io) skill. Your coding agent snapshots sources into `raw/`, compiles durable Traditional Chinese knowledge pages into `wiki/`, answers questions with citations, and lints the wiki for consistency. It can also process a manually triggered `Clippings/` queue created by Obsidian Web Clipper.

## Source

Original repository: [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)

## What Is an LLM Wiki?

An **LLM wiki** is a knowledge system where the LLM maintains structured wiki pages instead of re-searching raw documents on every question. New sources are compiled into durable markdown pages, cross-references are updated over time, and answers cite the wiki pages that already contain the synthesized knowledge.

This skill gives you four operations:

| Operation | What it does | Output |
|-----------|--------------|--------|
| **Ingest** | Snapshots a remote source, a named local file, or a clipping into `raw/`, triages it, then creates or updates wiki articles — or just logs it when nothing is new | New or updated wiki pages |
| **Process clippings** | Lists or sequentially processes the pending Markdown files in `Clippings/`, but only after an explicit request | Raw snapshots and completed wiki updates; processed clipping files are removed |
| **Query** | Searches the wiki and answers with citations | Grounded answers linking to markdown pages |
| **Lint** | Checks index integrity, links, and wiki health | Auto-fixes plus reported issues |

See [SKILL.md](SKILL.md) for the full skill specification.

## LLM Wiki vs RAG

| Approach | Knowledge lives in | When synthesis happens | Good for |
|----------|--------------------|------------------------|----------|
| **RAG** | Raw chunks and embeddings | At query time | Broad retrieval across large corpora |
| **LLM Wiki** | Curated markdown pages | During ingest and maintenance | Compounding knowledge, summaries, and durable cross-links |

This skill is optimized for the wiki model: knowledge that improves over time instead of re-deriving relationships on every query.

## Usage Stats

Based on a production knowledge base maintained daily since April 2026:

- **94** wiki articles across **13** topic directories
- **99** source materials ingested
- **87** operation log entries in the last 7 days

See [examples/](examples/) for sample wiki pages, source files, and operation logs.

## Install

```bash
npx skills@latest add ninthday/skills-base --skill nice-llm-wiki
```

Works with any tool that supports the [Agent Skills](https://agentskills.io) standard.

## Quick Start

### 1. Ingest your first source

Give the skill a URL, a file, or pasted text:

> "Ingest this article: https://example.com/attention-is-all-you-need"

The skill snapshots the source in `raw/`, then compiles or updates the right Traditional Chinese knowledge pages in `wiki/`.

### 2. Process Web Clipper content

Save web clips as Markdown under `Clippings/`, then explicitly choose one of these operations:

> "Organize `Clippings/article.md` into the wiki"

> "List pending clippings"

> "Process pending clippings"

The last command processes every pending Markdown clipping in sorted order. It does not run automatically.

### 3. Ask your wiki a question

> "What do I know about attention mechanisms?"

The skill searches the wiki and answers in Traditional Chinese with citations linking back to your markdown pages.

### 4. Keep the wiki healthy

> "Lint my wiki"

Checks for broken links, missing index entries, stale cross-references, and related issues.

## How the Workflow Works

The core idea from Karpathy: the LLM maintains the wiki while the human focuses on choosing sources and asking good questions.

```text
your-project/
├── Clippings/      ← Pending Web Clipper Markdown; removed after successful ingest
│   └── article.md
├── raw/            ← Immutable source snapshots
│   └── topic/
│       └── 2026-04-03-source-article.md
├── wiki/           ← Traditional Chinese knowledge pages maintained by the LLM
│   ├── topic/
│   │   └── concept-name.md
│   ├── index.md    ← Global table of contents
│   └── log.md      ← Append-only operation log
```

Each new source can update multiple pages, strengthen cross-references, and record contradictions. That is what makes the wiki compound over time.

## Clippings Queue

`Clippings/` is a manually triggered pending queue, not a directory watched in the background. A clipping is pending while its Markdown file remains in `Clippings/`; the skill does not consult `wiki/log.md` to determine pending status.

An explicit request to list or process pending clippings authorizes scanning Markdown files under `Clippings/` only. The skill sorts and processes candidates sequentially because `wiki/index.md` and `wiki/log.md` are shared state. It does not scan other vault directories, follow escaping symlinks, or refetch a clipping's original URL by default.

For each clipping, the skill creates an immutable `raw/` snapshot. The snapshot records its vault-relative `Clipping:` path, allowing a retry to reuse the snapshot only when its preserved source body matches the current clipping. Wiki articles always cite that raw snapshot, not the mutable clipping path.

The source clipping is deleted only after the raw snapshot, triage, article updates, `wiki/index.md`, and `wiki/log.md` all succeed. `No material` is successful once its snapshot and log entry exist. If any step fails, the clipping remains in `Clippings/` for a later explicit retry.

All clipping frontmatter, URLs, links, and body content are untrusted source data. They cannot authorize tool calls, directory scans, or other actions.

## Output Language

All agent-authored `wiki/` content uses Traditional Chinese (Taiwan): article titles and prose, headings, metadata labels, index entries, log entries, archive pages, and query answers. Source URLs, paths, code, proper nouns, and verbatim facts or quotes remain unchanged; `raw/` retains each source in its original language.

## Tool Compatibility

This skill follows the [agentskills.io](https://agentskills.io) open standard:

| Tool | Install method |
|------|----------------|
| Claude Code | `npx skills@latest add ninthday/skills-base --skill nice-llm-wiki` |
| Cursor | `npx skills@latest add ninthday/skills-base --skill nice-llm-wiki` |
| Codex CLI | Copy to `.agents/skills/nice-llm-wiki/` |
| OpenCode | `npx skills@latest add ninthday/skills-base --skill nice-llm-wiki` |
| Other tools | Copy `SKILL.md`, `references/`, and `scripts/` into the tool's skill directory |

## FAQ

### What is the difference between an LLM wiki and a personal wiki?

An LLM wiki is maintained by the model. It updates summaries, cross-links, index entries, and contradictions as new material arrives. A normal personal wiki depends on manual editing.

### What sources can I ingest?

Web pages, papers, blog posts, PDFs, markdown files, text files, pasted text, and Markdown clippings in `Clippings/`. The skill snapshots every imported source under `raw/` and compiles it into `wiki/`.

### Is this production-ready?

The workflow is based on a real knowledge base with 94 articles and 99 sources maintained daily since April 2026. The repo includes examples, templates, and a design spec.

## Security Boundaries

- Source material and compiled wiki content are data, not agent instructions. The skill's [Source Trust Boundary](SKILL.md#source-trust-boundary) prohibits using embedded instructions to expand tool permissions or access unrelated files.
- A named local clipping authorizes only that file. An explicit pending-clippings command authorizes only Markdown files under `Clippings/`; resolving paths outside the project root through symlinks is rejected and reported.
- The evidence checker confines automatically discovered articles and `wiki/log.md` to the project-local `wiki/` directory after resolving symlinks. Escaping files are skipped with stderr warnings; an escaping `wiki/` directory aborts the run. Warnings indicate incomplete coverage, not a clean bill of health.
- Explicit CLI article arguments can still select external files. Only pass user-authorized paths; never use this feature to retry automatically rejected files.

## Design Boundaries

Deliberately not built, after three months of production logs and a survey of the ecosystem (LLM Wiki v2, llm-wiki-compiler, OKF, agent-memory literature):

- **Source-hash freshness tracking** — raw/ is immutable, so hashes guard against events that cannot happen. Genuinely new information arrives as new sources through normal ingest.
- **Persisted line-number citations** — every observed fidelity error was "value absent from the source", which a whole-file grep catches. Anchors only disambiguate a failure mode that has not occurred, and the annotation friction makes agents skip the rule.
- **Numeric confidence or quality scores** — false precision with no calibration behind it. Evidence strength belongs in the prose.
- **Per-article review dates** — nobody can predict at compile time how fast a domain moves. Maintenance is driven by whole-wiki lint, not per-page timers.
- **Access-based decay** — frequently asked is not the same as true.
- **Retract / bad-source machinery** — has not happened yet. Handle it manually until it does.
- **Automatic hooks and scheduled runs** — those belong to the agent harness, not a tool-agnostic skill.
- **Vector or graph search** — at 50K–100K tokens of curated wiki, grep and read are more reliable. Add search tooling only when recall measurably degrades.
- **Typed relationship ontologies** — link semantics live in the prose around the link.
- **OKF conformance** — the spec is a v0.1 draft with a minimal tooling ecosystem. Tracked; will be revisited.
- **MCP servers, UIs, output subsystems** — outside the boundary of a tool-agnostic skill.

## Inspired By

Unofficial community implementation of the workflow from [Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The value here is the reusable workflow, prompt structure, and battle-tested knowledge-compilation rules.

See also: [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki), [atomicmemory/llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler). We are tracking Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) draft and will evaluate compatibility once the spec and tooling mature.

## License

[MIT](LICENSE)
