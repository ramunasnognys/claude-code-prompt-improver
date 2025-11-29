# OpenAI Apps SDK UI Migration - Project Directory

**Status**: ✅ PLANNING COMPLETE - READY TO EXECUTE
**Date**: 2025-11-26
**Project**: RiggOps (Rigger Job Management System)
**Effort**: 4-6 weeks
**Branch**: `matt/openai-sdk-ui-migration`

---

## 📁 Contents

### 📋 Main Planning Documents

1. **openai-sdk-ui-migration-plan.md** (19.5 KB)
   - Executive summary and scope
   - Current state analysis
   - 7-phase implementation strategy
   - Risk mitigation & success metrics
   - Timeline estimates

2. **openai-sdk-ui-migration-context.md** (15.6 KB)
   - Complete file structure reference
   - Design tokens (OKLch colors)
   - Component APIs and dependencies
   - Integration points (Convex, Clerk, Sonner)
   - Design guidelines and accessibility standards

3. **openai-sdk-ui-migration-tasks.md** (29.9 KB)
   - Actionable checklist for all 7 phases
   - 100+ specific tasks with acceptance criteria
   - Phase-by-phase breakdown:
     * Phase 1: Setup (6 tasks)
     * Phase 2: Navigation (6 tasks)
     * Phase 3: Forms (7 tasks)
     * Phase 4: Cards (7 tasks)
     * Phase 5: Pages (10 tasks)
     * Phase 6: Dark Mode & A11y (8 tasks)
     * Phase 7: Testing & Docs (7 tasks)

4. **ANSWERS_TO_UNRESOLVED_QUESTIONS.md** (12.0 KB)
   - Detailed analysis of 6 technical questions
   - Codebase findings for each question
   - Specific recommendations
   - Implementation guidance

---

## 🎯 Quick Summary

### What We're Doing
Migrating RiggOps UI from shadcn/ui components to **OpenAI's Apps SDK UI** for:
- Unified, professional design system
- Native dark mode support
- Better accessibility (WCAG 2.1 AA)
- Reduced CSS maintenance
- Consistent component library

### Current State
- **Stack**: Next.js 16, React 19, Tailwind CSS 4, Convex, Clerk
- **Components**: 11 UI primitives + 15 feature components
- **Pages**: 9 pages (dashboard, jobs, activity, handover, teams, auth, etc.)
- **Design**: OKLch color tokens, mobile-first responsive, Scandinavian aesthetic

### Effort
- **Total**: 4-6 weeks (160-240 hours)
- **Largest Phase**: Phase 5 (Pages) - 7-10 days
- **Risk Level**: LOW - Most decisions already made, clear path forward

---

## 🚀 How to Use This Directory

### For Project Managers
1. Read: **openai-sdk-ui-migration-plan.md** (Executive Summary + Phases)
2. Reference: Timeline estimates (4-6 weeks)
3. Track: Use **openai-sdk-ui-migration-tasks.md** checklist

### For Developers
1. Read: **openai-sdk-ui-migration-context.md** (understand current state)
2. Read: **ANSWERS_TO_UNRESOLVED_QUESTIONS.md** (technical decisions)
3. Follow: **openai-sdk-ui-migration-tasks.md** phase by phase
4. Reference: **openai-sdk-ui-migration-plan.md** for detailed task descriptions

### For Phase-to-Phase Execution
```
Phase 1 (Setup) → Verify build ✅
Phase 2 (Navigation) → Test responsive ✅
Phase 3 (Forms) → Test validation ✅
Phase 4 (Cards) → Test styling ✅
Phase 5 (Pages) → End-to-end testing ✅
Phase 6 (A11y/Dark) → Accessibility audit ✅
Phase 7 (Testing/Docs) → Bundle analysis, PR → Merge ✅
```

---

## 🔍 Key Findings (From Codebase Analysis)

### Icons (35 unique)
✅ All standard lucide-react icons - compatible with Apps SDK
- Fallback strategy: Keep lucide-react if Apps SDK missing any

### Date Pickers (2 instances)
✅ react-day-picker + Popover pattern
- Recommendation: Keep as-is, no changes needed

### Modals (3 Radix UI Dialogs)
✅ 51 sonner toast instances integrated - NO z-index conflicts
- Current pattern: Modal.Portal + Toaster at root

### Color System (OKLch CSS variables)
✅ CSS custom properties work with any design system
- Current: 20+ color tokens defined in globals.css
- Recommendation: Keep tokens, they're compatible with Apps SDK

### Tailwind Config
✅ Tailwind v4 (PostCSS-first), no config file
- Current: Inline `@theme` in globals.css
- Recommendation: Extract to tailwind.config.ts for clarity

### Providers (5 total)
✅ Clear nesting: ClerkProvider → ConvexProviderWithClerk → Children
- AppsSDKUIProvider: Add at root level (like Toaster)

---

## 📊 Migration Complexity by Phase

| Phase | Complexity | Risk | Duration |
|-------|-----------|------|----------|
| **1: Setup** | Low | Low | 1-2 days |
| **2: Navigation** | Low | Low | 3-4 days |
| **3: Forms** | Medium | Low | 4-5 days |
| **4: Cards** | Medium | Low | 4-5 days |
| **5: Pages** | High | Medium | 7-10 days |
| **6: A11y/Dark** | Medium | Low | 3-4 days |
| **7: Testing/Docs** | Medium | Low | 3-4 days |

---

## ✅ Pre-Migration Checklist

Before starting Phase 1:
- [ ] Team reviewed all 4 documents
- [ ] Approved 6 Q&A recommendations
- [ ] Read OpenAI Apps SDK documentation
- [ ] Created git branch: `matt/openai-sdk-ui-migration`
- [ ] Assigned developer(s) to project
- [ ] Scheduled Phase 1 kickoff

---

## 📝 Document Map

```
openai-sdk-ui-migration/
├── README.md (this file) ← START HERE
├── openai-sdk-ui-migration-plan.md
│   ├── Executive summary
│   ├── Current state analysis
│   ├── 7-phase breakdown
│   ├── Risk matrix
│   └── Success metrics
├── openai-sdk-ui-migration-context.md
│   ├── File structure reference
│   ├── Design tokens (OKLch)
│   ├── Component APIs
│   ├── Integration points
│   └── Design guidelines
├── openai-sdk-ui-migration-tasks.md
│   ├── Phase 1: Setup (6 tasks)
│   ├── Phase 2: Navigation (6 tasks)
│   ├── Phase 3: Forms (7 tasks)
│   ├── Phase 4: Cards (7 tasks)
│   ├── Phase 5: Pages (10 tasks)
│   ├── Phase 6: A11y/Dark Mode (8 tasks)
│   └── Phase 7: Testing/Docs (7 tasks)
└── ANSWERS_TO_UNRESOLVED_QUESTIONS.md
    ├── Question 1: Icons
    ├── Question 2: Date Pickers
    ├── Question 3: Modals & Toasts
    ├── Question 4: OKLch Colors
    ├── Question 5: Providers
    └── Question 6: Tailwind Config
```

---

## 🎓 Learning Resources

### OpenAI Apps SDK UI
- Official Docs: https://openai.github.io/apps-sdk-ui/
- Components reference
- Design tokens guide
- Dark mode setup
- Accessibility patterns

### RiggOps Codebase
- `/app/globals.css` - Design tokens
- `/components/ui/` - UI primitives
- `/components/` - Feature components
- `/app/layout.tsx` - Provider nesting

---

## 🤝 Team Collaboration

### Before Phase 1
- [ ] Assign lead developer
- [ ] Schedule planning meeting (2 hours)
- [ ] Discuss 6 Q&A recommendations
- [ ] Confirm timeline alignment

### During Migration
- [ ] Daily standup (15 min) - phase progress
- [ ] Phase review meeting - before moving to next phase
- [ ] Visual regression testing - compare old vs new
- [ ] Accessibility testing - WCAG 2.1 AA compliance

### After Migration
- [ ] Design review (colors, spacing, responsive)
- [ ] Code review (PR with detailed notes)
- [ ] Testing sign-off (all features working)
- [ ] Team training (using Apps SDK components)

---

## 🚨 Risk Management

### Low-Risk Areas
- Icon substitutions (fallback strategy ready)
- Color tokens (OKLch compatible with CSS vars)
- Provider nesting (clear guidance from Apps SDK docs)
- Dark mode (automatic via Apps SDK)

### Medium-Risk Areas
- Phase 5 (Pages) - largest phase, many dependencies
- Real device testing - need to test on multiple devices
- Bundle size - Apps SDK may add bloat

### Mitigation Strategies
- Read Apps SDK docs thoroughly before starting
- Test each phase before moving to next
- Create visual regression baseline (screenshots)
- Monitor bundle size with analyzer
- Rollback ready: keep `main` branch untouched

---

## 📞 Support Resources

### Documentation
- Migration guide (will be created in Phase 7)
- Design token mapping (created in Phase 1)
- Component examples (in codebase)

### External References
- OpenAI Apps SDK UI docs
- Tailwind CSS v4 docs
- Radix UI primitive docs (still used for Popover, Calendar)
- Convex docs (no changes needed)
- Clerk docs (no changes needed)

---

## 🎉 Success Criteria

When migration is complete:
- ✅ All 9 pages load without errors
- ✅ All features functional (CRUD, real-time, forms)
- ✅ Responsive on mobile & desktop
- ✅ Dark mode works
- ✅ Lighthouse scores ≥90 (Performance), ≥95 (Accessibility)
- ✅ Bundle size <15% increase
- ✅ Team trained on Apps SDK
- ✅ Documentation updated
- ✅ PR merged to main
- ✅ No regressions

---

## 📅 Timeline

- **Week 1**: Phase 1 (Setup) + Phase 2 (Navigation)
- **Week 2**: Phase 3 (Forms) + Phase 4 (Cards)
- **Week 3-4**: Phase 5 (Pages) - longest phase
- **Week 5**: Phase 6 (A11y/Dark Mode)
- **Week 6**: Phase 7 (Testing/Docs/PR/Merge)

---

**Last Updated**: 2025-11-26
**Status**: ✅ READY TO START
**Next Action**: Schedule Phase 1 kickoff, read Apps SDK docs
