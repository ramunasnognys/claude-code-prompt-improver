# Development Documentation Workflow

This directory contains task documentation that persists across Claude Code context resets.

## Directory Structure

```
dev/
├── active/          # Current work in progress
│   └── [task-name]/
│       ├── [task-name]-plan.md      # Comprehensive implementation plan
│       ├── [task-name]-context.md   # Key files, decisions, gotchas
│       └── [task-name]-tasks.md     # Checklist for tracking progress
└── completed/       # Finished tasks (archive)
```

## Workflow

### Starting a New Task

**Option 1: Use `/dev-docs` slash command**
```
/dev-docs implement user authentication with JWT
```
This creates the three-file structure automatically.

**Option 2: Use `strategic-plan-architect` agent**
In plan mode, use the Task tool:
```
Use strategic-plan-architect agent to plan: [your task description]
```
Agent creates more detailed plans with risk assessment and timelines.

### Working on a Task

1. **Read the plan** - `dev/active/[task-name]/[task-name]-plan.md`
2. **Check context** - Review key files and decisions in `-context.md`
3. **Follow checklist** - Mark tasks as done in `-tasks.md`
4. **Update as you go**:
   - Add new discoveries to context.md
   - Mark completed tasks in tasks.md
   - Note blockers or changes in context.md

### Before Context Reset

When approaching context limits (or before long break):

**Use `/dev-docs-update` command**
```
/dev-docs-update
```

This updates:
- Current implementation state
- Decisions made this session
- Files modified and why
- Next immediate steps
- Updates "Last Updated" timestamps

### Continuing After Reset

1. Navigate to `dev/active/[task-name]/`
2. Read all three files to get context
3. Continue from last checkpoint in tasks.md

### Completing a Task

1. Mark all tasks as ✅ in tasks.md
2. Move directory to `completed/`:
   ```bash
   mv dev/active/[task-name] dev/completed/
   ```
3. Optionally: Extract lessons learned to project docs

## File Purposes

### [task-name]-plan.md
**Purpose**: The "what" and "why"
- Executive summary
- Current vs future state
- Implementation phases
- Detailed task breakdown
- Risk assessment
- Success metrics
- Timeline estimates

**Update frequency**: Rarely (only if scope changes significantly)

### [task-name]-context.md
**Purpose**: The "how" and "where"
- Key files and their relevance
- Architectural decisions made
- Integration points
- Dependencies
- Important notes and gotchas

**Update frequency**: Frequently (whenever you make decisions or discover important info)

### [task-name]-tasks.md
**Purpose**: Progress tracking
- Checklist of all tasks
- Organized by phase
- Mark completed with ✅
- Add new tasks as discovered

**Update frequency**: Constantly (every time you complete a task)

## Best Practices

### DO
✅ Update context.md whenever you make a decision
✅ Mark tasks complete immediately
✅ Note blockers and issues as you find them
✅ Include "Last Updated" timestamps
✅ Be specific about file paths and line numbers
✅ Document edge cases and gotchas
✅ Use `/dev-docs-update` before context resets

### DON'T
❌ Let files get stale (update regularly)
❌ Forget to mark tasks complete
❌ Skip documenting decisions ("I'll remember")
❌ Leave vague next steps ("finish the API")
❌ Assume context will persist
❌ Delete files until task is truly complete

## Tips for Success

1. **Small, frequent updates** beat large, infrequent ones
2. **Specific is better than general** - "Updated auth.ts:42-67 to add rate limiting" vs "updated auth"
3. **Document why, not just what** - Future you (or Claude) needs to understand reasoning
4. **Keep tasks bite-sized** - Each task should be < 1 hour of work
5. **Update before breaks** - End of day, before lunch, before context reset

## Integration with Claude Code

### Slash Commands
- `/dev-docs [description]` - Create new task docs
- `/dev-docs-update` - Update before context reset

### Agents
- `strategic-plan-architect` - Detailed planning with risk assessment
- `plan-reviewer` - Review plans before implementation
- `documentation-architect` - Help organize and improve docs

### Skills
Skills will auto-activate based on what you're working on. Check the plan's "Required Resources" section for skill recommendations.

## Example Task Lifecycle

```bash
# 1. Start new feature
/dev-docs implement payment processing with Stripe

# 2. Work on implementation
# (Edit files, write code, test)

# 3. Update progress periodically
# Manually update context.md with decisions
# Mark completed tasks in tasks.md

# 4. Before context reset
/dev-docs-update

# 5. After context reset
# Read all three files in dev/active/payment-processing/
# Continue from where you left off

# 6. Complete task
# Mark all tasks ✅
mv dev/active/payment-processing dev/completed/
```

## Questions?

- Check `CLAUDE.md` for project-specific workflows
- Use `plan-reviewer` agent to validate plans
- Ask Claude to explain any unclear parts

---

**Remember**: These docs are your lifeline across context resets. Invest time in keeping them updated and they'll save you hours of reconstruction work.
