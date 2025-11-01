- In all interactions and commit messages, be extremely concise and sacrifice grammar for the sake of concision.

## PR Comments

<pr-comment-rule>
When I say to add a comment to a PR with a TODO on it, use 'checkbox' markdown format to add the TODO. For instance:

<example>
- [ ] A description of the todo goes here
</example>
</pr-comment-rule>
- When tagging Claude in GitHub issues, use '@claude'

## Changesets

To add a changeset, write a new file to the `.changeset` directory.

The file should be named `0000-your-change.md`. Decide your change: make it a patch, minor, or major change.

The format of the file should be:

```md
---
“evalite”: patch
---
Description of the change.

The description of the change should be user-facing, describe what features were added or bugs were fixed.

## GitHub

- Your primary method for interacting with GitHub should be the GitHub CLI.

## Git

- When creating branches, prefix them with matt/ to indicate they came from me.

## Plans

- At the end of each plan, give me a list of unresolved questions to answer, if any. Make the questions extremely concise. Sacrifice grammar for the sake of concision.

- In all interactions and commit messages, be extremely concise and sacrifice grammar for the sake of concision.

##UI/UX Design
use @docs (colors, responsive, shadow shadow) reference for style