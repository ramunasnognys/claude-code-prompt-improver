# Getting Started - Testing Your Claude Code Setup

**Quick Start Guide**: Test the infrastructure with a simple app example

---

## Prerequisites

✅ Setup is complete (see SETUP_COMPLETE.md)
🔄 **Restart Claude Code now** to load new settings

---

## Test 1: Skills Auto-Activation

### Try These Prompts

**Test Backend Skill:**
```
I need to create a new API endpoint for user registration
```
**Expected:** You should see a skill activation message suggesting `backend-dev-guidelines`

**Test Frontend Skill:**
```
Help me create a React component for a login form
```
**Expected:** `frontend-dev-guidelines` should be suggested

**Test Skill Developer:**
```
How do I create a custom skill?
```
**Expected:** `skill-developer` skill activates

### How It Works

The `UserPromptSubmit` hook:
1. Reads your prompt
2. Checks `skill-rules.json` for keyword matches
3. Injects skill suggestions before Claude sees your message
4. Skills auto-suggest based on context

---

## Test 2: Create Your First Simple App

Let's build a "Todo App" to test the workflow.

### Step 1: Use `/dev-docs` Slash Command

Type in Claude Code:
```
/dev-docs create a simple todo app with React frontend and Express backend
```

**What happens:**
- Command expands into a detailed prompt
- Claude creates `dev/active/todo-app/` directory
- Three files generated:
  - `todo-app-plan.md` - Implementation plan
  - `todo-app-context.md` - Key files and decisions
  - `todo-app-tasks.md` - Checklist

### Step 2: Review the Plan

Read the generated files:
```bash
cat dev/active/todo-app/todo-app-plan.md
cat dev/active/todo-app/todo-app-tasks.md
```

**What to look for:**
- Executive summary
- Implementation phases
- Detailed task breakdown
- Success metrics

### Step 3: Start Implementation

Follow the checklist in `todo-app-tasks.md`:

```markdown
## Phase 1: Setup
- [ ] Create project structure
- [ ] Setup Express backend
- [ ] Setup React frontend
- [ ] Configure dev environment

## Phase 2: Backend
- [ ] Create todo API routes
- [ ] Add data validation
- [ ] Implement CRUD operations
```

As you work:
- ✅ Mark completed tasks
- 📝 Update `todo-app-context.md` with decisions
- 🔍 Skills will auto-activate as you edit files

### Step 4: Test Context Survival

Before context reset (or to test):
```
/dev-docs-update
```

**What happens:**
- Updates all 3 dev docs files
- Captures current state
- Notes next steps
- Updates timestamps

**After restart/reset:**
- Read `dev/active/todo-app/` files
- You have full context to continue

---

## Test 3: Use an Agent

### Option 1: Strategic Plan Architect (The New One!)

```
Use strategic-plan-architect agent to plan: build a todo app with user authentication
```

**What happens:**
- Agent analyzes your request
- Examines your codebase structure
- Creates comprehensive plan with:
  - Risk assessment
  - Timeline estimates
  - Detailed phases
  - Auto-generates 3 dev docs files

**Difference from `/dev-docs`:**
- Agent = Deep analysis, more detailed
- Slash command = Quick template, faster

### Option 2: Code Architecture Review

After creating some code:
```
Use code-architecture-reviewer agent to review my todo app code
```

**What happens:**
- Agent reads your implementation
- Checks against best practices
- Identifies issues
- Suggests improvements

### Option 3: Plan Review

```
Use plan-reviewer agent to review the plan in dev/active/todo-app/todo-app-plan.md
```

**What happens:**
- Agent validates plan structure
- Checks for missing pieces
- Suggests improvements
- Validates feasibility

---

## Test 4: Skills Triggering on File Edits

### Create a Backend File

Create `backend/routes/todos.ts`:
```typescript
import express from 'express';

const router = express.Router();

router.get('/todos', async (req, res) => {
  // Get all todos
});

export default router;
```

**Expected:**
- `backend-dev-guidelines` skill may suggest (based on pathPatterns)
- Content patterns detect `router.`, `export`
- Hook reminds you of best practices

### Create a Frontend File

Create `src/components/TodoList.tsx`:
```typescript
import React from 'react';

export const TodoList: React.FC = () => {
  return <div>Todo List</div>;
};
```

**Expected:**
- `frontend-dev-guidelines` may trigger
- Content patterns detect React imports
- MUI patterns checked if using Material-UI

---

## Test 5: Error Handling Reminder

Create a file with async code:

`backend/services/todoService.ts`:
```typescript
export class TodoService {
  async createTodo(data: any) {
    const result = await prisma.todo.create({ data });
    return result;
  }
}
```

**Expected on Stop:**
- `error-handling-reminder` hook runs
- Detects async operations
- Gentle reminder about try-catch and Sentry
- Non-blocking (just awareness)

---

## Complete Workflow Example

### Scenario: Build Simple Todo App

#### 1. Planning Phase

**Enter plan mode:**
```
-p I want to build a todo app
```

**Use strategic-plan-architect:**
```
Use strategic-plan-architect agent to plan: simple todo app with React + Express
```

**Review and approve plan**

#### 2. Implementation Phase

**Exit plan mode, start coding:**

The agent creates:
```
dev/active/todo-app/
├── todo-app-plan.md
├── todo-app-context.md
└── todo-app-tasks.md
```

**Follow the tasks:**

```markdown
## Phase 1: Project Setup
- [x] Create directory structure
- [x] Initialize npm projects
- [x] Setup TypeScript configs
- [ ] Install dependencies
```

**As you work:**
- Edit files → Skills auto-activate
- Make decisions → Document in context.md
- Complete tasks → Mark ✅ in tasks.md

#### 3. Mid-Implementation Review

**Use code reviewer:**
```
Use code-architecture-reviewer to review backend/routes/todos.ts
```

**Update dev docs:**
```
/dev-docs-update
```

#### 4. Context Reset

**After compaction/restart:**

Read all 3 files:
```bash
cat dev/active/todo-app/todo-app-plan.md
cat dev/active/todo-app/todo-app-context.md
cat dev/active/todo-app/todo-app-tasks.md
```

**Continue from last checkpoint:**
- You know what was done
- You know what's next
- You have all context

#### 5. Completion

**Finish remaining tasks:**
```markdown
## All Phases
- [x] All tasks completed ✅
```

**Archive:**
```bash
mv dev/active/todo-app dev/completed/
```

---

## Quick Command Reference

### Slash Commands
```bash
/dev-docs [task description]      # Create dev docs
/dev-docs-update                  # Update before reset
/route-research-for-testing       # Find affected routes
```

### Using Agents
```bash
Use [agent-name] agent to [task]

# Examples:
Use strategic-plan-architect agent to plan: [description]
Use code-architecture-reviewer to review [file/feature]
Use plan-reviewer agent to review [plan-file]
Use web-research-specialist to research [topic]
```

### Available Agents
- `strategic-plan-architect` - Elite planning (NEW!)
- `code-architecture-reviewer` - Review code
- `plan-reviewer` - Review plans
- `code-refactor-master` - Plan refactors
- `documentation-architect` - Create docs
- `frontend-error-fixer` - Fix frontend issues
- `auto-error-resolver` - Fix TypeScript errors
- `web-research-specialist` - Research online
- `auth-route-tester` - Test JWT routes
- `auth-route-debugger` - Debug auth issues
- `refactor-planner` - Plan refactoring

---

## Understanding Skill Activation

### Keywords that Trigger Skills

**backend-dev-guidelines:**
- backend, API, endpoint, route, controller, service
- Express, Prisma, middleware, validation

**frontend-dev-guidelines:**
- component, React, UI, page, modal, dialog
- MUI, Material-UI, styling, layout

**skill-developer:**
- skill system, create skill, skill triggers
- hook system, skill-rules.json

**route-tester:**
- test route, test endpoint, test API
- authenticated route, JWT testing

**error-tracking:**
- error handling, exception, Sentry
- monitoring, captureException

### File Patterns that Trigger Skills

**Backend files:**
- `src/**/*.ts`
- `backend/**/*.ts`
- `api/**/*.ts`
- Content: `router.`, `export.*Controller`, `prisma.`

**Frontend files:**
- `src/**/*.tsx`
- `frontend/**/*.tsx`
- `SaaS/src/**/*.tsx`
- Content: `from '@mui/material'`, `import.*React`

---

## Debugging Tips

### Skills Not Triggering?

**Check hook is running:**
```bash
ls -l .claude/hooks/skill-activation-prompt.sh
# Should show: -rwxr-xr-x (executable)
```

**Test manually:**
```bash
cd .claude/hooks
echo '{"prompt":"I need to create a backend API"}' | npx tsx skill-activation-prompt.ts
```

**Expected output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 RECOMMENDED SKILLS:
  → backend-dev-guidelines

ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Agents Not Found?

**Check agent exists:**
```bash
ls .claude/agents/strategic-plan-architect.md
```

**Use exact name (without .md):**
```
Use strategic-plan-architect agent to plan: my task
```

### Dev Docs Not Created?

**Check command syntax:**
```
/dev-docs description of task
```

**Verify directory exists:**
```bash
ls -la dev/active/
```

---

## Next Steps

1. ✅ **Test skills** - Try keyword prompts
2. ✅ **Create todo app** - Use `/dev-docs` command
3. ✅ **Use an agent** - Try strategic-plan-architect
4. ✅ **Implement feature** - Follow the tasks
5. ✅ **Update docs** - Use `/dev-docs-update`
6. ✅ **Review code** - Use code-architecture-reviewer
7. ✅ **Archive task** - Move to completed/

## Tips for Success

**DO:**
- ✅ Use `/dev-docs` for every significant feature
- ✅ Update context.md as you make decisions
- ✅ Mark tasks complete immediately
- ✅ Use agents for complex analysis
- ✅ Run `/dev-docs-update` before context reset
- ✅ Let skills auto-activate (don't fight it)

**DON'T:**
- ❌ Skip creating dev docs for "quick" features
- ❌ Let context.md get stale
- ❌ Forget to mark tasks complete
- ❌ Ignore skill suggestions
- ❌ Delete dev docs until truly done

---

## Success Criteria

You'll know it's working when:

1. **Skills auto-suggest** when you mention keywords
2. **Dev docs persist** across context resets
3. **Agents provide value** with detailed analysis
4. **You never lose context** because docs are up-to-date
5. **Code quality improves** with hook reminders

---

## Get Help

- **Setup issues:** See `SETUP_COMPLETE.md`
- **Workflow questions:** See `dev/README.md`
- **Skill creation:** Use `skill-developer` skill
- **Agent list:** Check `.claude/agents/README.md`

---

**You're ready to build!** 🚀

Start with: `/dev-docs create a simple todo app`
