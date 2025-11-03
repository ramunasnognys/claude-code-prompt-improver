---
name: skills-generator
description: Generate new Claude skills with proper structure, YAML frontmatter, and progressive disclosure. Use when users want to create, build, or generate a new skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skills Generator

This skill guides the creation of effective Claude skills from concept to packaged deliverable.

## Overview

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. This skill automates the entire skill creation process, from understanding requirements to generating a validated, distributable skill package.

## Workflow

### Step 1: Understand the Skill Requirements

Ask focused questions to understand the skill's purpose:

- "What specific task or workflow should this skill handle?"
- "Can you provide concrete examples of how this skill would be used?"
- "What would trigger this skill to activate?"
- "Does this skill need any scripts, reference documentation, or asset files?"

Avoid overwhelming the user with too many questions at once. Start with 2-3 key questions and follow up as needed.

### Step 2: Determine Skill Components

Based on the examples and requirements, identify what components the skill needs:

**Scripts (`scripts/`)** - Include when:
- The same code is repeatedly rewritten
- Deterministic reliability is critical
- Token efficiency is important
- Examples: PDF manipulation scripts, data processing utilities, API helpers

**References (`references/`)** - Include when:
- Detailed documentation should be loaded on demand
- Information is too lengthy for SKILL.md
- Domain-specific knowledge is needed
- Examples: API documentation, database schemas, workflow guides, company policies

**Assets (`assets/`)** - Include when:
- Files will be used in the final output
- Templates or boilerplate code is needed
- Examples: Brand logos, PowerPoint templates, HTML/React boilerplate, font files

### Step 3: Initialize the Skill Structure

Use the initialization script to create the skill directory:

```bash
python scripts/init_skill.py <skill-name> --path <directory>
```

This creates:
- Proper directory structure
- SKILL.md template with YAML frontmatter
- Example files in scripts/, references/, and assets/

**Naming conventions:**
- Use hyphen-case (e.g., "data-analyzer", "pdf-editor")
- Lowercase letters, digits, and hyphens only
- Max 40 characters
- Must match directory name exactly

### Step 4: Write the SKILL.md Content

The SKILL.md file is the core of the skill. It must include:

#### YAML Frontmatter (Required)

```yaml
---
name: skill-name
description: Complete explanation of what the skill does and when to use it. Include specific scenarios, file types, or tasks that trigger it.
---
```

**Critical requirements:**
- `name`: Matches directory name, hyphen-case, max 64 characters
- `description`: Comprehensive explanation, max 1024 characters, written in third person

#### Markdown Body (Required)

Choose the appropriate structure based on skill type:

**Workflow-Based** (sequential processes):
- Works for step-by-step procedures
- Structure: Overview → Workflow Decision Tree → Step 1 → Step 2...
- Example: Document creation with reading → creating → editing

**Task-Based** (tool collections):
- Works for different operations/capabilities
- Structure: Overview → Quick Start → Task Category 1 → Task Category 2...
- Example: PDF tools with merge → split → extract

**Reference/Guidelines** (standards or specifications):
- Works for brand guidelines, coding standards, requirements
- Structure: Overview → Guidelines → Specifications → Usage
- Example: Brand styling with colors → typography → assets

**Capabilities-Based** (integrated systems):
- Works for multiple interrelated features
- Structure: Overview → Core Capabilities → Feature 1 → Feature 2...
- Example: Product management with numbered capability list

**Writing style:**
- Use imperative/infinitive form (verb-first instructions)
- Avoid second person ("you should")
- Use objective, instructional language
- Example: "To accomplish X, do Y" rather than "You should do X"

#### Progressive Disclosure

Keep SKILL.md under 500 lines. Use the three-level loading system:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (unlimited)

Reference additional files from SKILL.md:
- "For advanced usage, see [reference.md](references/reference.md)"
- "Run the helper script using Python"
- "Use the template from assets directory"

### Step 5: Create Bundled Resources

#### Scripts

Create executable Python or Bash scripts in `scripts/` directory. Scripts should be well-documented and handle errors gracefully.

Make scripts executable: `chmod +x scripts/script.py`

#### References

Create markdown documentation in `references/` directory with detailed information that Claude should load on demand.

#### Assets

Add template files, images, fonts, or boilerplate code in `assets/` directory:
- Templates: .pptx, .docx, HTML/React projects
- Images: .png, .jpg, .svg
- Fonts: .ttf, .woff2
- Data: .csv, .json

### Step 6: Validate and Package

Run the packaging script which includes validation. This will validate YAML frontmatter format, check naming conventions, verify directory structure, check description completeness, and create a distributable .zip file.

If validation fails, fix errors and run again.

### Step 7: Test and Iterate

After creating the skill:
1. Test with real use cases
2. Notice inefficiencies or gaps
3. Update SKILL.md or bundled resources
4. Re-validate and re-package
5. Repeat until the skill performs reliably

## Best Practices

**Metadata Quality:**
- Write descriptions that help Claude determine when to use the skill
- Include specific triggers: file types, keywords, task types
- Use third person: "This skill should be used when..."

**Avoid Duplication:**
- Information should live in either SKILL.md or references, not both
- Keep SKILL.md lean with essential procedural instructions
- Move detailed reference material to references/

**Token Efficiency:**
- Keep SKILL.md under 500 lines
- Split large content into separate reference files
- Use grep search patterns for files >10k words

**Security:**
- Only create skills from trusted requirements
- Audit any scripts before execution
- Document all dependencies

**Composability:**
- Design skills to work together
- Reference other skills when appropriate
- Keep skills focused on single workflows

## Common Patterns

**Document Processing Skill:**
- Scripts: File manipulation utilities
- References: File format specifications
- Assets: Document templates

**API Integration Skill:**
- Scripts: API client wrappers
- References: API documentation, schemas
- Assets: Configuration templates

**Brand Guidelines Skill:**
- Scripts: None typically needed
- References: Style guides, tone documentation
- Assets: Logos, fonts, color swatches, templates

**Data Analysis Skill:**
- Scripts: Data processing, visualization utilities
- References: Schema documentation, analysis guides
- Assets: Sample datasets, report templates

## Resources

This skill uses the official scripts from Anthropic's skills repository:

### scripts/init_skill.py
Creates new skill directories with proper structure and template files.

### scripts/package_skill.py
Validates and packages skills into distributable .zip files.

### references/skill_spec.md
Complete specification for Claude skill format and requirements.

---

**Note:** Generated skills are specific to the user's requirements and should be thoroughly tested before production use.
