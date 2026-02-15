# Blog Admin Layer Design

Add an admin layer to the bhavanaai Astro blog: draft management, publishing, and inline commenting -- all from the browser, on any device.

## Constraints

- Stay on GitHub Pages (static site, no server functions)
- GitHub PAT for authentication (entered once per device, stored in localStorage)
- No new backend infrastructure
- YAGNI throughout

## Architecture

The blog remains a fully static Astro site deployed to GitHub Pages. Admin features are client-side JS that activates when a valid GitHub PAT is in localStorage. All write operations (publish, save feedback) go through the GitHub Contents API directly from the browser.

## Admin Auth

- New `/admin` page with a single text input for a GitHub Fine-Grained PAT
- PAT scoped to the bhavanaai repo with "Contents: Read and Write" permission
- Stored in localStorage, validated with `GET /user` on the GitHub API
- Admin mode detected site-wide by checking localStorage for the PAT
- No OAuth, no server-side auth, no passwords

## Draft Visibility

- Drafts are built into the site at their normal URLs (full Astro rendering pipeline)
- Drafts are excluded from: homepage listing, RSS feed, sitemap
- A "Drafts" link appears in the nav bar only when admin mode is active (client-side JS toggle)
- If a non-admin visits a draft URL directly, they see the post with a "DRAFT" banner but no admin controls
- Draft pages are not secret -- just unlisted

## Draft Management

- `/drafts` page lists all posts with `draft: true` (fetched at build time via `getCollection`)
- Each row shows: title, date, "View" link, "Publish" button
- Page is gated by admin mode (shows "Please sign in" with link to /admin if no PAT)

## Publishing

- "Publish" button appears on `/drafts` page and on individual draft post pages (admin mode only)
- Flow: click Publish > confirm dialog > GitHub Contents API reads the markdown file, flips `draft: true` to `draft: false` in frontmatter, commits back > success message ("site will rebuild in ~1 min")
- No "unpublish" button (rare action, do via git)
- No build status tracking (YAGNI)

## Inline Commenting

Ported from the preview.html commenting system already built for short_projects.

### Features
- Text selection commenting: select text, click "Comment," type feedback, margin annotation
- Image/chart commenting: click an image, click "Comment," type feedback
- Right-margin cards on wide screens, inline cards on mobile
- "Save Feedback" and "Clear All Comments" buttons in a banner
- Only visible in admin mode

### Persistence and Sync
- Comments save to localStorage immediately (fast, no network delay)
- "Save Feedback" commits `feedback/{slug}.json` to the repo via GitHub Contents API
- On page load (in admin mode), fetch `feedback/{slug}.json` from the repo and restore comments
- Merge strategy: GitHub version is source of truth, localStorage is the working copy
- Feedback files stored at `public/feedback/{slug}.json` (accessible at `https://me.bhavanaai.com/feedback/{slug}.json`)

### Feedback Workflow with Claude
1. View draft on any device, add inline comments
2. Click "Save Feedback" (commits to repo)
3. Tell Claude: "apply feedback on ai-productivity-gap"
4. Claude reads `feedback/{slug}.json`, applies changes, commits updated draft
5. Site rebuilds, view updated draft, repeat

## File Changes

### New files
- `src/pages/admin.astro` -- PAT entry and validation page
- `src/pages/drafts.astro` -- Draft listing with publish buttons
- `src/scripts/admin.js` -- Admin mode detection, GitHub API helpers, inline commenting system

### Modified files
- `src/layouts/BaseLayout.astro` -- Add "Drafts" nav link (hidden by default, toggled by admin JS). Include admin.js script.
- `src/pages/blog/[...slug].astro` -- Include drafts in `getStaticPaths`. Add draft banner. Mount commenting UI container.

### Unchanged
- `src/content/config.ts` -- Draft field already exists in schema
- `src/pages/index.astro` -- Already filters out drafts
- `src/pages/rss.xml.js` -- Already filters out drafts

## Dependencies

No new npm dependencies. The commenting system is vanilla JS (ported from preview.html). GitHub API calls use `fetch`.
