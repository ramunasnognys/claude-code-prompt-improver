# Rigger Job Management App - Development Context

**Last Updated**: 2025-12-02 (Add Photos to Existing Jobs)

## Current Status: ADD PHOTOS TO EXISTING JOBS COMPLETE

**This Session** (2025-12-02):
- Implemented ability to add photos to existing jobs
- New `addPhotosToJob` mutation with version check + 5 photo limit
- New `AddPhotosSection` component for job detail page
- `PhotoUpload` now accepts `maxPhotos` prop for remaining slots
- Photos card always visible on job detail page

**Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`
**Git Branch**: `main`
**Latest Commit**: `2c2066d` - feat: add photos to existing jobs

---

## SESSION CHANGES

### 1. New Mutation (`convex/jobs.ts`)

```typescript
export const addPhotosToJob = mutation({
  args: {
    jobId: v.id("jobRequests"),
    photoIds: v.array(v.id("_storage")),
    expectedVersion: v.number(),
  },
  handler: async (ctx, args) => {
    // Auth check
    // Get job
    // Version check
    const existingPhotos = job.photoIds ?? [];
    const totalPhotos = existingPhotos.length + args.photoIds.length;
    if (totalPhotos > 5) {
      throw new Error(`Cannot add photos. Only ${5 - existingPhotos.length} slots remaining.`);
    }
    // Merge + update
    await ctx.db.patch(args.jobId, {
      photoIds: [...existingPhotos, ...args.photoIds],
      lastUpdatedByUserId: user._id,
      version: job.version + 1,
    });
    // Activity event
    await ctx.db.insert("activityEvents", {
      type: "photos_added",
      note: `${args.photoIds.length} photo(s) added`,
      // ...
    });
  },
});
```

### 2. New Component (`components/AddPhotosSection.tsx`)

```tsx
interface AddPhotosSectionProps {
  jobId: Id<"jobRequests">;
  existingCount: number;
  expectedVersion: number;
}

export function AddPhotosSection({ ... }) {
  const [photos, setPhotos] = useState<PhotoFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const addPhotos = useMutation(api.jobs.addPhotosToJob);
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);

  const remainingSlots = 5 - existingCount;

  // Upload photos then call mutation
  // Toast on success

  return (
    <div>
      <PhotoUpload maxPhotos={remainingSlots} ... />
      {photos.length > 0 && <Button>Add {photos.length} Photo(s)</Button>}
    </div>
  );
}
```

### 3. PhotoUpload `maxPhotos` Prop

```tsx
interface PhotoUploadProps {
  value: PhotoFile[];
  onChange: (files: PhotoFile[]) => void;
  disabled?: boolean;
  error?: string;
  maxPhotos?: number;  // NEW - defaults to 5
}

// Uses maxAllowed = maxPhotos ?? MAX_PHOTOS throughout
```

### 4. Job Detail Page Update

```tsx
{/* Photos Card - Always visible */}
<div className="border rounded-lg p-4">
  <h2>Photos ({job.photoIds?.length ?? 0}/5)</h2>

  {/* Existing photos */}
  {job.photoIds?.length > 0 && <PhotoGallery photoIds={job.photoIds} />}

  {/* Add more photos (if < 5) */}
  {(!job.photoIds || job.photoIds.length < 5) && (
    <AddPhotosSection
      jobId={job._id}
      existingCount={job.photoIds?.length ?? 0}
      expectedVersion={job.version}
    />
  )}
</div>
```

---

## Files Modified This Session

**Convex:**
- `convex/jobs.ts` - Added `addPhotosToJob` mutation

**Components:**
- `components/PhotoUpload.tsx` - Added `maxPhotos` prop
- `components/AddPhotosSection.tsx` - NEW component

**Pages:**
- `app/jobs/[id]/page.tsx` - Photos card always visible + add UI

---

## Previous Session: Photo Upload UX Improvements

- Added to QuickCreateJobSheet (mobile FAB flow)
- Fixed gallery picker (removed capture attribute)
- Added "+" add more tile in photo grid
- Smaller thumbnails (5 cols mobile, 10 cols desktop)
- Refined remove button (dark blur, iOS/Android style)

---

## Build Status

```
Route (app)
├ ○ /                    - Landing/redirect
├ ○ /activity            - Activity timeline
├ ○ /admin/teams         - Team management
├ ○ /dashboard           - Redirects to /jobs
├ ○ /handover            - Shift handover (desktop)
├ ○ /jobs                - Kanban board
├ ƒ /jobs/[id]           - Job detail page (has photos + add)
├ ○ /jobs/new            - Create job form (has upload)
├ ○ /profile             - User settings
├ ƒ /sign-in/[[...sign-in]]
└ ƒ /sign-up/[[...sign-up]]

11 routes, build passes
```

---

## Context Reset Procedure

1. Read this file for session context
2. Check git status: `cd ~/Developer/workspace/prompt-improver/rigger-jobs && git status`
3. Run Convex: `npx convex dev`
4. Start dev: `npm run dev` (http://localhost:3000)
5. Test add photos at `/jobs/[id]` detail page

---

## Architecture Summary

**Frontend**: Next.js 16 + React 19 + Tailwind
**Backend**: Convex (real-time DB + file storage)
**Auth**: Clerk (JWT + webhooks)
**UI**: Radix UI + shadcn components
**Icons**: Lucide React
**Toasts**: Sonner

**Key Patterns**:
- Presentational components (no Convex queries inside)
- React.memo for performance
- Version-based optimistic locking
- Server-side filtering/enrichment
- 44px touch targets throughout
- Controlled components for form state

---

## Photo Feature Summary

**Schema**: `photoIds: v.optional(v.array(v.id("_storage")))` in `jobRequests`

**Upload Flow**:
1. User selects photos (camera or gallery)
2. HEIC converted to JPEG client-side
3. Files uploaded to Convex storage via `generateUploadUrl`
4. Storage IDs passed to `createJob` or `addPhotosToJob`

**Display**:
- `PhotoGallery` component with lightbox (react-medium-image-zoom)
- Grid layout: 5 cols mobile, 10 cols desktop

**Limits**:
- Max 5 photos per job
- Max 5MB per file
- Accepted: JPEG, PNG, HEIC/HEIF

---

## Remaining Post-MVP Features

- [ ] Push notifications for urgent jobs
- [ ] Analytics dashboard
- [ ] Shift management
- [ ] Multi-language (Norwegian + English)
- [ ] CSV/PDF export
- [ ] AI integration (optional)
