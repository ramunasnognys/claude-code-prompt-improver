# Claude Skills Specification

## Overview

This document provides the complete specification for Claude Skills format and requirements based on Anthropic's official documentation.

## Skill Structure

Every skill consists of a directory containing at minimum a SKILL.md file:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required)
│   └── Markdown body (required)
├── scripts/ (optional)
│   └── Executable code files
├── references/ (optional)
│   └── Documentation files
└── assets/ (optional)
    └── Template/resource files
```

## SKILL.md Requirements

### YAML Frontmatter

Required fields at the start of SKILL.md:

```yaml
---
name: skill-name
description: Complete description of what the skill does and when to use it
---
```

**Field Requirements:**

- **name**:
  - Lowercase letters, digits, and hyphens only
  - Must match containing directory name
  - Maximum 64 characters
  - Example: `pdf-editor`, `data-analyzer`

- **description**:
  - Maximum 1024 characters
  - Must be comprehensive and informative
  - Include WHEN to use the skill (triggers)
  - Written in third person
  - Example: "This skill should be used when users need to create and edit PDF documents. Use for PDF manipulation, form filling, and document merging."

### Optional Frontmatter Fields

```yaml
---
name: skill-name
description: Description text
version: 1.0.0
dependencies: python>=3.8, pandas>=1.5.0
allowed-tools: Read, Grep, Glob
license: Apache-2.0
---
```

- **version**: Track skill versions as you iterate
- **dependencies**: Software packages required by the skill
- **allowed-tools**: Restrict which tools Claude can use when skill is active
- **license**: License information for the skill

### Markdown Body

The markdown body contains instructions, workflows, and guidance for Claude.

**Writing Style:**
- Use imperative/infinitive form (verb-first instructions)
- Avoid second person ("you" or "your")
- Use objective, instructional language
- Example: "To accomplish X, do Y" not "You should do X"

**Structure Patterns:**

1. **Workflow-Based** (sequential processes)
   - Overview → Workflow Decision Tree → Step 1 → Step 2...

2. **Task-Based** (tool collections)
   - Overview → Quick Start → Task 1 → Task 2...

3. **Reference/Guidelines** (standards)
   - Overview → Guidelines → Specifications → Usage

4. **Capabilities-Based** (integrated features)
   - Overview → Core Capabilities → Feature 1 → Feature 2...

**Size Limits:**
- Keep SKILL.md under 500 lines for optimal performance
- Total size should be under 5,000 words
- Split larger content into reference files

## Progressive Disclosure

Skills use a three-level loading system:

1. **Level 1: Metadata (Always Loaded)**
   - Just the name and description from YAML frontmatter
   - ~100 words
   - Loaded into system prompt at startup
   - Used by Claude to determine skill relevance

2. **Level 2: SKILL.md Body (Loaded When Triggered)**
   - Full markdown content of SKILL.md
   - <5,000 words recommended
   - Loaded when Claude determines skill is relevant
   - Contains core instructions and workflows

3. **Level 3: Bundled Resources (Loaded On Demand)**
   - Scripts, references, assets
   - Unlimited size (scripts can execute without loading)
   - Claude loads only what it needs for specific scenarios

## Bundled Resources

### Scripts Directory (scripts/)

**Purpose:** Executable code for deterministic operations

**When to Include:**
- Same code is repeatedly rewritten
- Deterministic reliability is critical
- Token efficiency is important

**File Types:**
- Python scripts (.py)
- Shell scripts (.sh, .bash)
- JavaScript (.js)
- Any executable code

**Benefits:**
- May be executed without loading into context
- Token efficient
- Deterministic results
- Reduces AI generation errors

**Example:**
```
scripts/
├── rotate_pdf.py
├── extract_text.py
└── merge_documents.sh
```

### References Directory (references/)

**Purpose:** Documentation loaded into context as needed

**When to Include:**
- Detailed documentation too long for SKILL.md
- API specifications
- Database schemas
- Company policies
- Workflow guides

**File Types:**
- Markdown files (.md)
- Text documentation (.txt)
- JSON schemas (.json)
- YAML specifications (.yaml)

**Benefits:**
- Keeps SKILL.md lean
- Loaded only when Claude determines it's needed
- Progressive disclosure of detailed information

**Best Practice:**
- For files >10k words, include grep search patterns in SKILL.md
- Avoid duplicating information between SKILL.md and references
- Prefer references for detailed material

**Example:**
```
references/
├── api_documentation.md
├── database_schema.md
└── company_policies.md
```

### Assets Directory (assets/)

**Purpose:** Files used in output, not loaded into context

**When to Include:**
- Templates needed for output
- Boilerplate code to copy/modify
- Images, logos, icons
- Fonts
- Sample documents

**File Types:**
- Document templates (.pptx, .docx)
- Images (.png, .jpg, .svg)
- Fonts (.ttf, .woff2)
- Boilerplate code (HTML/React directories)
- Sample data (.csv, .json)

**Benefits:**
- Separates output resources from documentation
- Claude uses files without loading into context
- No token cost for asset files

**Example:**
```
assets/
├── logo.png
├── slide_template.pptx
├── frontend-boilerplate/
│   ├── index.html
│   └── app.js
└── brand-font.ttf
```

## Naming Conventions

**Skill Names:**
- Use hyphen-case: `pdf-editor`, `data-analyzer`
- Lowercase only
- No spaces or underscores
- Max 40 characters
- Must match directory name exactly

**File Names:**
- Scripts: Use snake_case: `rotate_pdf.py`, `extract_data.sh`
- References: Use snake_case or hyphenated: `api_reference.md`, `schema-docs.md`
- Assets: Any convention, but be consistent

## Validation Requirements

Before packaging, skills must pass validation:

1. **YAML Frontmatter:**
   - Starts with `---`
   - Contains `name` field
   - Contains `description` field
   - Ends with `---`

2. **Directory Structure:**
   - Skill directory name matches `name` field
   - SKILL.md exists in root
   - Any referenced files exist

3. **Description Quality:**
   - Comprehensive explanation of skill purpose
   - Includes when/why to use the skill
   - Written in third person
   - No XML tags

4. **File Organization:**
   - Scripts in scripts/ directory
   - Documentation in references/ directory
   - Templates/resources in assets/ directory

## Security Considerations

**Important Safety Guidelines:**

1. Only use skills from trusted sources:
   - Skills you created yourself
   - Skills from Anthropic
   - Thoroughly audited third-party skills

2. Audit skills before use:
   - Review all scripts for malicious code
   - Check for hidden dependencies
   - Verify external API calls
   - Review file system access

3. Skills can direct Claude to:
   - Execute code
   - Access files
   - Make API calls
   - Modify data

4. Use `allowed-tools` to restrict capabilities:
   ```yaml
   allowed-tools: Read, Grep, Glob
   ```

## Distribution

Skills are distributed as .zip files:

1. Package using validation tool
2. Zip file includes entire skill directory
3. Maintains proper directory structure
4. Name: `skill-name.zip`

## Usage Across Claude Products

Skills work across:

- **Claude.ai** - Upload zip files in Settings → Capabilities → Skills
- **Claude Code** - Install via plugin marketplace or local directory
- **Claude API** - Upload via `/v1/skills` endpoint

## Best Practices Summary

1. **Keep SKILL.md lean** (<500 lines)
2. **Write clear descriptions** with specific triggers
3. **Use progressive disclosure** - split large content
4. **Avoid duplication** between SKILL.md and references
5. **Include concrete examples** in instructions
6. **Test on real tasks** before distribution
7. **Iterate based on usage** - update and improve
8. **Document dependencies** clearly
9. **Use appropriate structure** for skill type
10. **Follow naming conventions** consistently

## Common Pitfalls

- Description too vague - Claude won't know when to use it
- SKILL.md too long - slows down loading
- Duplicating content between SKILL.md and references
- Using second person instead of imperative form
- Not including concrete examples
- Forgetting to test with real use cases
- Missing or incorrect YAML frontmatter
- Directory name doesn't match skill name

## Resources

- Anthropic Skills Documentation: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Skills Repository: https://github.com/anthropics/skills
- Best Practices Guide: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
