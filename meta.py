from skills_manager.models import VendorSkillMeta

# Repositories to clone as submodules and generate skills from source.
submodules: dict[str, str] = {}

# Already generated skills, sync with their `skills/` directory.
vendors: dict[str, VendorSkillMeta] = {
    "mattpocock": VendorSkillMeta(
        source="https://github.com/mattpocock/skills",
        skills={
            "engineering/grill-with-docs": "grill-with-docs",
            "productivity/grilling": "grilling",
            "engineering/domain-modeling": "domain-modeling",
            "engineering/tdd": "tdd",
            "engineering/diagnosing-bugs": "diagnosing-bugs",
            "engineering/improve-codebase-architecture": "improve-codebase-architecture",
            "engineering/prototype": "prototype",
            "engineering/to-spec": "to-spec",
            "productivity/handoff": "handoff",
            "productivity/writing-great-skills": "writing-great-skills",
        },
    ),
    "JimChen": VendorSkillMeta(
        source="https://github.com/jim60105/copilot-prompt",
        skills={
            "chinese-content-writing-guideline": "chinese-content-writing-guideline",
            "drawio-diagrams-enhanced": "drawio-diagrams-enhanced",
            "python-security": "python-security",
        },
    ),
    "awesome-copilot": VendorSkillMeta(
        source="https://github.com/github/awesome-copilot",
        skills={
            "readme-blueprint-generator": "readme-blueprint-generator",
            "git-commit": "git-commit",
        },
    ),
}

# Self-maintained skills with Lucas Yang's preferences, tastes, and recommendations.
manual = (
    # "bruno-api-testing",
    # "chinese-content-writing-guideline",
    # "documentation-writer",
    # "drawio-diagrams-enhanced",
    # "git-commit",
    # "python-security",
    # "readme-blueprint-generator",
)
