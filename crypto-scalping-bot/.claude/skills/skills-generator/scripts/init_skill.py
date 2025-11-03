#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <directory>
"""
import sys
from pathlib import Path

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete explanation of what the skill does and when to use it.]
---

# {skill_title}

## Overview

[TODO: Explain what this skill enables]

## Instructions

[TODO: Add guidance for Claude to follow when using this skill]

## Examples

[TODO: Provide concrete examples]
"""

EXAMPLE_SCRIPT = """#!/usr/bin/env python3
def main():
    print("Example script for {skill_name}")

if __name__ == "__main__":
    main()
"""

def title_case_skill_name(skill_name):
    return ' '.join(word.capitalize() for word in skill_name.split('-'))

def init_skill(skill_name, path):
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    skill_dir.mkdir(parents=True)
    print(f"Created skill directory: {skill_dir}")

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    (skill_dir / 'SKILL.md').write_text(skill_content)
    print("Created SKILL.md")

    scripts_dir = skill_dir / 'scripts'
    scripts_dir.mkdir()
    (scripts_dir / 'example.py').write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))

    (skill_dir / 'references').mkdir()
    (skill_dir / 'assets').mkdir()

    return skill_dir

def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <directory>")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    init_skill(skill_name, path)

if __name__ == "__main__":
    main()
