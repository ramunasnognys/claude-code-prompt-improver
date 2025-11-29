# OpenAI Apps SDK UI Migration Plan - RiggOps

**Last Updated**: 2025-11-26
**Status**: PLANNING - Ready for Implementation
**Effort**: Large (4-6 weeks estimated)

---

## Executive Summary

RiggOps is a mobile-first workforce management app built with Next.js 16, React 19, Tailwind CSS 4, Convex (database), and Clerk (auth). This plan migrates the entire UI from shadcn/ui components to OpenAI's Apps SDK UI while preserving all functionality.

**Target Outcome**: Unified design system with OpenAI's clean, professional aesthetic matching RiggOps's minimalist Scandinavian design philosophy.

**Key Constraints**:
- Maintain 100% feature parity during migration
- Preserve mobile-first, responsive design
- Keep current routing structure intact
- Zero breaking changes for backend/Convex integration

---

## Current State Analysis

### Tech Stack
- **Framework**: Next.js 16 (App Router)
- **UI Library**: Radix UI primitives + shadcn/ui components
- **Styling**: Tailwind CSS 4 with custom OKLch color tokens
- **Form Handling**: React Hook Form + Zod validation
- **Icons**: lucide-react
- **Notifications**: sonner (toast)
- **Auth**: Clerk (single-tenant)
- **Database**: Convex (real-time subscriptions)

### Component Inventory

**Core UI Components** (11):
- `Button` - CVA-based with variants (default, destructive, outline, secondary, ghost, link)
- `Popover` - Radix-based date/action picker
- `Calendar` - React Day Picker (date selection)
- Modal/Dialog patterns (QuickCreateJobSheet, TeamStatusModal, QuickActionsModal)

**Feature Components** (15):
- `Sidebar` - Fixed navigation (lg: breakpoint 1024px+)
- `MobileHeader` - Mobile-only header with logo
- `BottomNav` - Mobile navigation tabs
- `JobCard` - Kanban-style job display
- `StatusColumn` - Kanban column wrapper
- `DashboardStatusCard` - KPI metrics cards
- `TodayTeamsPanel` - Collapsible team status overview
- `TeamBadge` - Team member display
- `FilterPanel` - Activity filter controls
- `ActivityEventCard` - Timeline event display
- `SkeletonJobCard` / `SkeletonStatusColumn` - Loading states
- `OfflineBanner` - Offline indicator

**Pages** (9):
- Dashboard, Jobs (Kanban board), Jobs/:id, Jobs/new (form), Activity, Handover, Teams (admin), Sign-in, Sign-up

### Design Tokens (Current)
- **Colors**: OKLch-based (oklch notation with hue, lightness, chroma)
- **Status tokens**: `--status-new`, `--status-progress`, `--status-delayed`, `--status-done` (light + dark)
- **Spacing**: Tailwind defaults (0.25rem, 0.5rem, etc.)
- **Shadows**: Tailwind defaults (`shadow-xs`, `shadow-sm`, etc.)
- **Radius**: Inline variable (`--radius: 0.625rem` with scaled variants)

### Pain Points with Current Setup
1. Manual design token management (OKLch variables in CSS)
2. No unified component library across projects
3. Missing some accessible patterns (ARIA labeling, keyboard navigation)
4. Icon library mix (lucide-react only)
5. No built-in dark mode theming (manual CSS variables)

---

## Proposed Future State

### OpenAI Apps SDK UI Integration

**What's Included**:
- Pre-built, accessible components (Button, Input, Dialog, Card, Badge, etc.)
- Design tokens for colors (text-primary, text-secondary, bg-surface, etc.)
- Built-in dark mode support via CSS custom properties
- Tailwind configuration ready-made
- Icons from @openai/apps-sdk-ui
- Shadow and spacing utilities aligned with OpenAI's design system

**Component Mapping**:
| Current | Apps SDK UI |
|---------|-------------|
| Button (CVA) | `<Button>` variant props |
| Popover (Radix) | `<Popover>` component |
| Calendar (RDP) | `<DatePicker>` or custom wrapper |
| Modal (Radix) | `<Dialog>` component |
| Custom cards | `<Card>` component |
| Icons (lucide) | Apps SDK UI icons |
| Status colors | Design tokens (bg-status-new, etc.) |

**Benefits**:
- ✅ Professional, cohesive design across all projects
- ✅ Consistent accessibility patterns (WCAG 2.1 AA)
- ✅ Reduced CSS maintenance (no custom token management)
- ✅ Dark mode handled automatically
- ✅ Responsive utilities built-in
- ✅ Smaller bundle size (shared design system)

---

## Migration Strategy

### Phase Approach
1. **Setup** - Install SDK, configure Tailwind/CSS imports
2. **Layout & Navigation** - Migrate Sidebar, MobileHeader, BottomNav
3. **Buttons & Forms** - Migrate Button, form inputs, controls
4. **Cards & Content** - Migrate cards, badges, data displays
5. **Pages & Integration** - Migrate entire pages end-to-end
6. **Dark Mode & Polish** - Verify dark mode, accessibility, responsive
7. **Testing & Docs** - Comprehensive testing, migration guide

### Risk Mitigation
- **Breaking Changes**: Apps SDK may have different API. Test each component before merging.
- **Icon Differences**: Some lucide icons may not exist in Apps SDK. Create wrapper or substitute.
- **Color Token Mismatches**: Apps SDK tokens may not map 1:1 to OKLch. Create compatibility layer if needed.
- **Bundle Size**: Monitor for bloat. Tree-shake unused components.

---

## Implementation Phases

### Phase 1: Setup & Configuration (Effort: S)

**Objective**: Install Apps SDK, configure styles, verify build.

**Tasks**:
1.1 Install @openai/apps-sdk-ui package
1.2 Update main.css with SDK imports
1.3 Verify Tailwind configuration compatibility
1.4 Test dev server builds without errors
1.5 Document current color token mapping

**Acceptance Criteria**:
- ✅ Package installed with no conflicts
- ✅ CSS imports resolve correctly
- ✅ `npm run dev` runs successfully
- ✅ No TypeScript errors in components
- ✅ Build completes (`npm run build`)

**Dependencies**: None (foundational)

---

### Phase 2: Layout & Navigation Migration (Effort: M)

**Objective**: Migrate Sidebar, MobileHeader, BottomNav to Apps SDK UI.

**Tasks**:
2.1 Migrate Sidebar to Apps SDK UI (navigation links, logo, user section)
2.2 Migrate MobileHeader to Apps SDK UI
2.3 Migrate BottomNav tabs to Apps SDK UI
2.4 Test responsive layout (mobile <1024px, desktop ≥1024px)
2.5 Verify touch targets remain ≥44px
2.6 Update icon imports from Apps SDK

**Acceptance Criteria**:
- ✅ Sidebar renders correctly on desktop
- ✅ MobileHeader visible on mobile only
- ✅ BottomNav visible on mobile only
- ✅ All navigation links functional
- ✅ Active page highlighting works
- ✅ Icons display correctly
- ✅ No visual regressions vs. current

**Dependencies**: Phase 1

---

### Phase 3: Button & Form Controls (Effort: M)

**Objective**: Migrate Button, form inputs, selects, checkboxes to Apps SDK UI.

**Tasks**:
3.1 Migrate Button component (all variants: solid, outline, soft, ghost)
3.2 Create Input wrapper for Apps SDK UI
3.3 Migrate form controls in QuickCreateJobSheet
3.4 Migrate form controls in TeamStatusModal
3.5 Migrate form controls in QuickActionsModal
3.6 Verify form validation (Zod) still works
3.7 Test keyboard navigation (Tab, Enter, Escape)

**Acceptance Criteria**:
- ✅ All button variants render and function
- ✅ Form inputs accept text/numbers
- ✅ Validation errors display correctly
- ✅ Submit buttons trigger form submission
- ✅ Disabled states work
- ✅ Focus rings visible (keyboard navigation)
- ✅ No layout shifts on validation errors

**Dependencies**: Phase 1

---

### Phase 4: Cards, Badges & Data Display (Effort: M)

**Objective**: Migrate JobCard, StatusColumn, DashboardStatusCard, TeamBadge, ActivityEventCard.

**Tasks**:
4.1 Migrate DashboardStatusCard (KPI metrics) to Apps SDK UI
4.2 Migrate JobCard layout (status badge, team badge, metadata)
4.3 Migrate TeamBadge display (member names)
4.4 Migrate StatusColumn container styling
4.5 Migrate ActivityEventCard layout (event type, timestamp, metadata)
4.6 Update color tokens for status badges (new/progress/delayed/done)
4.7 Test cards on both mobile & desktop

**Acceptance Criteria**:
- ✅ All cards display content correctly
- ✅ Badges show correct status colors
- ✅ Text hierarchy maintained (headers, body, meta)
- ✅ Spacing matches Scandinavian aesthetic
- ✅ Status colors readable in light & dark modes
- ✅ Cards responsive on mobile (full-width, stacked)
- ✅ Cards responsive on desktop (grid layout)

**Dependencies**: Phase 1, Phase 3

---

### Phase 5: Page-by-Page Migration (Effort: L)

**Objective**: Migrate all 9 pages end-to-end, testing functionality.

**Tasks**:
5.1 Migrate Dashboard page (layout, status cards, teams panel, active jobs)
5.2 Migrate Jobs page (Kanban board, status columns, job cards)
5.3 Migrate Jobs/[id] page (job detail view, actions)
5.4 Migrate Jobs/new page (job creation form, all inputs)
5.5 Migrate Activity page (event list, filters, timeline)
5.6 Migrate Handover page (daily summary, area grouping)
5.7 Migrate Teams page (team list, create/edit team modal)
5.8 Migrate Sign-in page (Clerk form)
5.9 Migrate Sign-up page (Clerk form)
5.10 End-to-end testing: Create job → Assign team → Change status → View activity

**Acceptance Criteria**:
- ✅ All pages load without errors
- ✅ Data displays correctly (Convex queries work)
- ✅ CRUD operations work (create, read, update, delete jobs/teams)
- ✅ Real-time updates from Convex display correctly
- ✅ Toast notifications (sonner) display correctly
- ✅ Modal dialogs open/close properly
- ✅ Forms submit and update Convex
- ✅ Activity timeline shows events in correct order
- ✅ Handover summary calculates correctly

**Dependencies**: Phase 1, Phase 2, Phase 3, Phase 4

---

### Phase 6: Dark Mode & Accessibility Polish (Effort: M)

**Objective**: Verify dark mode works, improve accessibility.

**Tasks**:
6.1 Test all pages in dark mode (system preference + toggle)
6.2 Verify contrast ratios meet WCAG AA (4.5:1 for text)
6.3 Test keyboard navigation (Tab, Shift+Tab, Enter, Escape)
6.4 Test screen reader labels (ARIA roles, labels)
6.5 Test focus indicators visible on all interactive elements
6.6 Test color tokens render correctly in dark mode
6.7 Test status colors readable in dark mode
6.8 Verify no console errors (accessibility warnings)

**Acceptance Criteria**:
- ✅ Dark mode toggle works
- ✅ All text readable in light & dark (contrast ≥4.5:1)
- ✅ Keyboard navigation works on all pages
- ✅ Tab order logical
- ✅ No keyboard traps
- ✅ Focus indicators visible
- ✅ Screen reader announces buttons, links, form labels
- ✅ No axe accessibility warnings

**Dependencies**: Phase 5

---

### Phase 7: Testing, Optimization & Documentation (Effort: M)

**Objective**: Comprehensive testing, bundle analysis, migration guide.

**Tasks**:
7.1 Run Lighthouse audit (performance, accessibility, SEO)
7.2 Test on real devices (iPhone, iPad, Android, desktop)
7.3 Test connectivity (offline mode with Convex)
7.4 Check bundle size (Apps SDK + Tailwind overhead)
7.5 Create migration guide documenting:
   - Before/after component examples
   - Design token mapping
   - Breaking changes (if any)
   - Icon substitutions
   - New Apps SDK features available for future use
7.6 Update README with Apps SDK UI setup instructions
7.7 Create PR with comprehensive diff and testing notes

**Acceptance Criteria**:
- ✅ Lighthouse score ≥90 (performance)
- ✅ No visual regressions
- ✅ Bundle size < 15% larger than current
- ✅ Load time on 4G ≤3s
- ✅ All features functional on real devices
- ✅ Migration guide complete and clear
- ✅ Team trained on new component library

**Dependencies**: Phase 1-6

---

## Detailed Task Breakdown

### Setup Phase (1-2 days)

```
1.1 Install package
   npm install @openai/apps-sdk-ui
   → Update package.json, pnpm-lock.yaml

1.2 Update app/globals.css
   @import "@openai/apps-sdk-ui/css" (before/after @import "tailwindcss"?)
   → Verify CSS load order (Apps SDK first, then Tailwind)

1.3 Check Tailwind v4 compatibility
   → Verify tailwind.config.ts exists
   → Ensure no conflicts with current theme config
   → Test with `npm run dev`

1.4 Update app/layout.tsx if needed
   → Add AppsSDKUIProvider (if required by SDK)
   → Keep ClerkProvider, ConvexProvider, Toaster

1.5 Create design token mapping doc
   → Map current OKLch tokens to Apps SDK tokens
   → Document fallbacks for any missing tokens
```

### Navigation Phase (3-4 days)

```
2.1 Refactor components/Sidebar.tsx
   → Replace custom nav styling with Apps SDK UI
   → Test navigation links, active states
   → Keep logo, user section logic

2.2 Refactor components/MobileHeader.tsx
   → Use Apps SDK UI header component
   → Keep responsive (hidden on desktop)

2.3 Refactor components/BottomNav.tsx
   → Use Apps SDK UI tabs or nav
   → Test mobile-only visibility

2.4 Visual regression testing
   → Compare current vs. new on multiple breakpoints
   → Screenshot comparisons for Figma/stakeholders
```

### Forms Phase (4-5 days)

```
3.1 Create UI wrapper components
   → Input, Select, Checkbox, Radio using Apps SDK UI
   → Ensure React Hook Form integration works

3.2 Refactor QuickCreateJobSheet
   → Replace all form fields with Apps SDK UI
   → Test form submission
   → Verify Zod validation triggers

3.3 Refactor TeamStatusModal, QuickActionsModal
   → Same pattern as QuickCreateJobSheet

3.4 Test keyboard navigation
   → Use browser devtools (F12 → Console) to check focus
```

### Cards & Data Phase (4-5 days)

```
4.1 Migrate DashboardStatusCard
   → Use Apps SDK UI Card component
   → Preserve layout (large number, label, icon)

4.2 Migrate JobCard
   → Status badge → Apps SDK Badge
   → Keep drag-handle styling (if Kanban has it)

4.3 Migrate status colors
   → Update globals.css or create status-tokens.css
   → Test in light & dark modes

4.4 Test responsive layouts
   → Mobile: cards full-width, stacked
   → Desktop: cards in grid/columns
```

### Page Integration Phase (7-10 days)

```
5.1 Dashboard page
   → Update layout container
   → Test status cards, teams panel, active jobs
   → Verify Convex queries display data

5.2 Jobs page (Kanban board)
   → This is complex - may need to test extensively
   → Drag-and-drop should still work
   → Test status column styling

5.3 Jobs/:id page
   → Detail view layout
   → Action buttons (assign team, change status, update delay)
   → Modal triggers

5.4 Jobs/new page
   → Job creation form
   → All field types (text, date, select, textarea)
   → Validation display

5.5 Activity page
   → Event list layout
   → Filter controls
   → Timeline styling

5.6-5.9 Remaining pages
   → Handover, Teams, Auth pages
   → Similar testing pattern

5.10 Integration testing
   → End-to-end user workflows
   → Check Convex real-time updates
   → Verify toast notifications work
```

### Dark Mode & A11y Phase (3-4 days)

```
6.1 Dark mode testing
   → System preference (prefers-color-scheme)
   → Manual toggle (if App has one)
   → Screenshot comparison light vs. dark

6.2 Accessibility audit
   → Use axe DevTools extension
   → Check contrast ratios (Lighthouse)
   → Test keyboard nav (Tab through all pages)
   → Test with screen reader (VoiceOver on Mac/iOS)

6.3 Fix issues found
   → Add missing ARIA labels
   → Improve focus indicators if needed
   → Adjust colors for contrast
```

### Testing & Docs Phase (3-4 days)

```
7.1 Lighthouse audit
   → Open each page in DevTools → Lighthouse
   → Target: Performance ≥90, Accessibility ≥95

7.2 Device testing
   → iPhone 12/14/16, iPad Pro, Android (Samsung)
   → Desktop (Chrome, Safari, Firefox)
   → Test touch interactions, orientation changes

7.3 Bundle size analysis
   → Compare main.js, css files before/after
   → Use Bundle Analyzer if needed

7.4 Migration documentation
   → Code examples (before/after)
   → Component API reference
   → Troubleshooting guide
   → Future feature ideas with Apps SDK

7.5 Team handoff
   → Update project README
   → Create onboarding doc for new devs
```

---

## Success Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| **Design Consistency** | 70% (custom tokens) | 95% (Apps SDK) | 🎯 |
| **Accessibility Score** | 85 (Lighthouse) | 95+ | 🎯 |
| **Component Reusability** | 60% (some overlap) | 90% (Apps SDK enforced) | 🎯 |
| **Dark Mode Support** | Manual CSS vars | Native via SDK | 🎯 |
| **Bundle Size** | ~150KB (gzipped) | <165KB | 🎯 |
| **Build Time** | ~8-10s | <12s | 🎯 |
| **Feature Parity** | 100% | 100% | 🎯 |

---

## Dependencies & Prerequisites

### External
- OpenAI Apps SDK UI documentation (openai.github.io/apps-sdk-ui/)
- Tailwind CSS v4 (already installed)
- Clerk (auth) - no changes needed
- Convex (database) - no changes needed

### Internal
- Current component implementations (for reference during migration)
- Design token definitions (globals.css)
- Page layouts and routing structure

### Team Skills Needed
- React 19 patterns (hooks, suspense)
- Tailwind CSS 4 utilities
- TypeScript (types for Apps SDK components)
- Accessibility (WCAG 2.1 AA)
- Testing (visual regression, a11y)

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| **API mismatch** (Apps SDK props differ) | High | Medium | Read SDK docs thoroughly, create component wrappers |
| **Icon library gaps** (lucide → Apps SDK) | Medium | Medium | Create fallback to lucide for missing icons |
| **Color token mismatch** | Medium | Low | Test token mapping early, create compat layer |
| **Performance regression** | Medium | Low | Bundle size analysis, code splitting review |
| **Dark mode bugs** | Low | Low | Comprehensive testing on real devices |
| **Breaking changes in SDK** | High | Low | Lock package version, monitor releases |

---

## Timeline Estimate

**Total Effort**: 4-6 weeks (160-240 hours)

| Phase | Days | Effort |
|-------|------|--------|
| Phase 1: Setup | 1-2 | S (Small) |
| Phase 2: Navigation | 3-4 | M (Medium) |
| Phase 3: Forms | 4-5 | M |
| Phase 4: Cards | 4-5 | M |
| Phase 5: Pages | 7-10 | L (Large) |
| Phase 6: Dark Mode & A11y | 3-4 | M |
| Phase 7: Testing & Docs | 3-4 | M |
| **Total** | **25-34** | **4-6 weeks** |

---

## Rollback Strategy

If critical issues arise during migration:
1. Create feature branch: `matt/openai-sdk-ui-migration`
2. Keep current code on `main` unchanged
3. If migration fails: Reset to `main`, document blockers
4. Partial rollback: Migrate components incrementally, keep working pages on old UI until safe

---

## Future Opportunities

Once migration complete:
- Dark mode toggle UI control (if not already present)
- More Apps SDK components (Dropdown, Select, Combobox)
- Animation library integration (framer-motion + Apps SDK)
- Theming system for multi-tenant future
- Component storybook with Storybook + Apps SDK

---

## Questions & Clarifications Needed

1. **Icon library**: Does OpenAI Apps SDK have all icons RiggOps needs? (Home, LayoutDashboard, Activity, FileText, Settings, Plus, LogOut, User, etc.)
2. **Date picker**: Does Apps SDK have DatePicker component? If not, can we keep react-day-picker?
3. **Modal styling**: Are Apps SDK modals compatible with sonner toasts (z-index, overlap)?
4. **Custom status colors**: Can OKLch tokens be used with Apps SDK, or must we switch to RGB/Hex?
5. **Provider nesting**: Does AppsSDKUIProvider need to wrap ClerkProvider/ConvexProvider, or can it be at same level?
6. **Tailwind config**: Should we replace entire tailwind.config.ts with Apps SDK version, or merge?

---

**Next Steps**: Review plan, clarify questions, begin Phase 1 setup.
