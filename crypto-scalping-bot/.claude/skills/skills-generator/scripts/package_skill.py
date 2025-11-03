#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable zip file of a skill folder

Usage:
    python package_skill.py <skill-path> [output-directory]
"""
import sys
import zipfile
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of skill structure."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "SKILL.md missing YAML frontmatter"

    if 'name:' not in content or 'description:' not in content:
        return False, "SKILL.md missing required name or description"

    return True, "Skill validation passed"

def package_skill(skill_path, output_dir=None):
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists() or not skill_path.is_dir():
        print(f"Error: Skill folder not found: {skill_path}")
        return None

    # Validate before packaging
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"Validation failed: {message}")
        return None

    print(f"Validation passed: {message}")

    skill_name = skill_path.name
    output_path = Path(output_dir).resolve() if output_dir else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)

    zip_filename = output_path / f"{skill_name}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

    print(f"\nSuccessfully packaged skill to: {zip_filename}")
    return zip_filename

def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill-path> [output-directory]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    package_skill(skill_path, output_dir)

if __name__ == "__main__":
    main()
