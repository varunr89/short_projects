# Blog Admin Layer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add admin auth, draft management, publishing, and inline commenting to the bhavanaai Astro blog.

**Architecture:** Client-side admin mode via GitHub PAT in localStorage. Drafts built into site at normal URLs but excluded from listings. Commenting system (ported from short_projects preview.html) activates in admin mode. All write operations (publish, save feedback) use GitHub Contents API from the browser.

**Tech Stack:** Astro 5, Tailwind CSS 4, vanilla JS, GitHub REST API

**Repo:** `/Users/varunr/projects/bhavanaai/` (remote: `varunr89/bhavanaai`)

**Design doc:** `/Users/varunr/projects/short_projects/docs/plans/2026-02-15-blog-admin-layer-design.md`

---

### Task 1: Admin Page and Auth

Build the `/admin` page where the user enters their GitHub PAT. Store it in localStorage. Validate it against the GitHub API.

**Files:**
- Create: `src/pages/admin.astro`

**Step 1: Create the admin page**

Create `src/pages/admin.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Admin">
  <div id="admin-logged-out">
    <h1 class="text-2xl font-bold mb-4">Admin</h1>
    <p class="text-[var(--text-muted)] mb-4">
      Enter a GitHub Fine-Grained Personal Access Token scoped to the
      <code>varunr89/bhavanaai</code> repo with <strong>Contents: Read and Write</strong> permission.
    </p>
    <p class="text-[var(--text-muted)] text-sm mb-6">
      Create one at
      <a href="https://github.com/settings/tokens?type=beta" target="_blank" rel="noopener">
        GitHub Settings &rarr; Developer Settings &rarr; Fine-grained tokens
      </a>.
    </p>
    <form id="pat-form" class="space-y-3">
      <input
        id="pat-input"
        type="password"
        placeholder="github_pat_..."
        class="w-full px-3 py-2 rounded border border-[var(--text-muted)]/30 bg-[var(--bg)] text-[var(--text)] font-mono text-sm focus:outline-none focus:border-[var(--link)]"
      />
      <button
        type="submit"
        class="px-4 py-2 rounded bg-[var(--link)] text-white text-sm font-medium hover:opacity-90"
      >
        Sign In
      </button>
      <p id="pat-error" class="text-red-500 text-sm hidden"></p>
    </form>
  </div>

  <div id="admin-logged-in" class="hidden">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Admin</h1>
      <button id="sign-out-btn" class="text-sm text-[var(--link)] hover:underline">Sign Out</button>
    </div>
    <p class="text-green-600 dark:text-green-400 text-sm mb-4" id="admin-user-info"></p>
  </div>
</BaseLayout>

<script is:inline>
(function() {
  var STORAGE_KEY = 'bhavanaai-gh-pat';
  var loggedOut = document.getElementById('admin-logged-out');
  var loggedIn = document.getElementById('admin-logged-in');
  var form = document.getElementById('pat-form');
  var input = document.getElementById('pat-input');
  var error = document.getElementById('pat-error');
  var userInfo = document.getElementById('admin-user-info');
  var signOutBtn = document.getElementById('sign-out-btn');

  function showError(msg) {
    error.textContent = msg;
    error.classList.remove('hidden');
  }

  function showLoggedIn(username) {
    loggedOut.classList.add('hidden');
    loggedIn.classList.remove('hidden');
    userInfo.textContent = 'Signed in as ' + username;
  }

  function showLoggedOut() {
    loggedIn.classList.add('hidden');
    loggedOut.classList.remove('hidden');
    error.classList.add('hidden');
    input.value = '';
  }

  async function validatePat(pat) {
    var res = await fetch('https://api.github.com/user', {
      headers: { 'Authorization': 'Bearer ' + pat }
    });
    if (!res.ok) return null;
    var data = await res.json();
    return data.login;
  }

  // Check existing PAT on load
  var existing = localStorage.getItem(STORAGE_KEY);
  if (existing) {
    validatePat(existing).then(function(username) {
      if (username) {
        showLoggedIn(username);
      } else {
        localStorage.removeItem(STORAGE_KEY);
        showLoggedOut();
      }
    });
  }

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    error.classList.add('hidden');
    var pat = input.value.trim();
    if (!pat) { showError('Please enter a token.'); return; }

    var username = await validatePat(pat);
    if (!username) { showError('Invalid token. Check permissions and try again.'); return; }

    localStorage.setItem(STORAGE_KEY, pat);
    showLoggedIn(username);
  });

  signOutBtn.addEventListener('click', function() {
    localStorage.removeItem(STORAGE_KEY);
    showLoggedOut();
  });
})();
</script>
```

**Step 2: Test manually**

Run: `cd /Users/varunr/projects/bhavanaai && npm run dev`

- Visit `http://localhost:4321/admin`
- Verify the PAT form renders
- Enter an invalid token, verify error message
- Enter a valid GitHub PAT, verify "Signed in as varunr89" appears
- Refresh the page, verify still signed in (localStorage persists)
- Click "Sign Out", verify form reappears

**Step 3: Commit**

```bash
git add src/pages/admin.astro
git commit -m "feat: add admin page with GitHub PAT auth"
```

---

### Task 2: Admin Nav Link in BaseLayout

Add a "Drafts" link to the nav that only shows when admin mode is active.

**Files:**
- Modify: `src/layouts/BaseLayout.astro`

**Step 1: Add the Drafts link and admin detection script**

In `src/layouts/BaseLayout.astro`, add a hidden "Drafts" link to the nav and a script to toggle it.

After the RSS nav link (line 43: `<a href={`${base}rss.xml`}>RSS</a>`), add:

```html
<a href={`${base}drafts`} id="nav-drafts" class="hidden">Drafts</a>
```

After the existing theme toggle `<script is:inline>` block (after line 63), add a new script:

```html
<script is:inline>
  // Admin mode: show Drafts nav link if PAT exists
  (function() {
    var pat = localStorage.getItem('bhavanaai-gh-pat');
    if (pat) {
      var el = document.getElementById('nav-drafts');
      if (el) el.classList.remove('hidden');
    }
  })();
</script>
```

**Step 2: Test manually**

- With dev server running, visit `http://localhost:4321/`
- Verify "Drafts" link is NOT visible in the nav
- Go to `/admin`, sign in with a valid PAT
- Go back to `/` -- verify "Drafts" link IS now visible in the nav
- Sign out on `/admin`, go back to `/` -- verify "Drafts" is hidden again

**Step 3: Commit**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat: add Drafts nav link visible in admin mode"
```

---

### Task 3: Drafts Listing Page

Build the `/drafts` page that lists all draft posts with Publish buttons.

**Files:**
- Create: `src/pages/drafts.astro`

**Step 1: Create the drafts listing page**

Create `src/pages/drafts.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

const drafts = (await getCollection('blog', ({ data }) => data.draft === true))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
const base = import.meta.env.BASE_URL;
---

<BaseLayout title="Drafts">
  <div id="drafts-gate" class="hidden">
    <p class="text-[var(--text-muted)]">
      Please <a href={`${base}admin`}>sign in</a> to view drafts.
    </p>
  </div>

  <div id="drafts-content" class="hidden">
    <h1 class="text-2xl font-bold mb-6">Drafts</h1>

    {drafts.length === 0 ? (
      <p class="text-[var(--text-muted)]">No drafts.</p>
    ) : (
      <ul class="space-y-4">
        {drafts.map((post) => (
          <li class="flex items-center justify-between gap-4">
            <a href={`${base}blog/${post.slug}`} class="block group flex-1 min-w-0">
              <span class="text-[var(--text-muted)] text-sm font-mono">
                {post.data.date.toISOString().split('T')[0]}
              </span>
              <span class="ml-4 group-hover:underline">{post.data.title}</span>
            </a>
            <button
              class="publish-btn shrink-0 px-3 py-1 rounded text-xs font-medium bg-green-600 text-white hover:bg-green-700"
              data-slug={post.slug}
            >
              Publish
            </button>
          </li>
        ))}
      </ul>
    )}
  </div>
</BaseLayout>

<script is:inline>
(function() {
  var STORAGE_KEY = 'bhavanaai-gh-pat';
  var REPO = 'varunr89/bhavanaai';
  var pat = localStorage.getItem(STORAGE_KEY);

  if (!pat) {
    document.getElementById('drafts-gate').classList.remove('hidden');
    return;
  }

  document.getElementById('drafts-content').classList.remove('hidden');

  // Publish handler
  document.querySelectorAll('.publish-btn').forEach(function(btn) {
    btn.addEventListener('click', async function() {
      var slug = btn.dataset.slug;
      if (!confirm('Publish "' + slug + '"? This will go live after the site rebuilds.')) return;

      btn.disabled = true;
      btn.textContent = 'Publishing...';

      try {
        // Fetch the current file from GitHub
        var filePath = 'src/content/blog/' + slug + '.md';
        var res = await fetch('https://api.github.com/repos/' + REPO + '/contents/' + filePath, {
          headers: { 'Authorization': 'Bearer ' + pat }
        });
        if (!res.ok) throw new Error('Could not read file: ' + res.status);

        var fileData = await res.json();
        var content = atob(fileData.content);

        // Flip draft: true to draft: false
        var updated = content.replace(/^draft:\s*true\s*$/m, 'draft: false');
        if (updated === content) {
          alert('Could not find "draft: true" in frontmatter.');
          btn.disabled = false;
          btn.textContent = 'Publish';
          return;
        }

        // Commit the change
        var putRes = await fetch('https://api.github.com/repos/' + REPO + '/contents/' + filePath, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + pat,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: 'publish: ' + slug,
            content: btoa(updated),
            sha: fileData.sha
          })
        });
        if (!putRes.ok) throw new Error('Could not update file: ' + putRes.status);

        btn.textContent = 'Published!';
        btn.classList.remove('bg-green-600', 'hover:bg-green-700');
        btn.classList.add('bg-gray-400');
      } catch (err) {
        alert('Error: ' + err.message);
        btn.disabled = false;
        btn.textContent = 'Publish';
      }
    });
  });
})();
</script>
```

**Step 2: Test manually**

- Create a test draft blog post: add a file `src/content/blog/test-draft.md` with `draft: true` in frontmatter
- Visit `/drafts` without being logged in -- verify "Please sign in" message
- Sign in at `/admin`, visit `/drafts` -- verify the test draft appears in the list
- Click the draft title -- verify it navigates to the blog post
- (Do NOT test the Publish button yet -- that commits to the real repo)

**Step 3: Commit**

```bash
git add src/pages/drafts.astro
git commit -m "feat: add drafts listing page with publish buttons"
```

---

### Task 4: Include Drafts in Blog Build + Draft Banner

Modify the blog slug page to build draft posts and show a "DRAFT" banner.

**Files:**
- Modify: `src/pages/blog/[...slug].astro`

**Step 1: Update getStaticPaths and add draft banner**

The current `getStaticPaths` at `src/pages/blog/[...slug].astro` already returns ALL posts (no draft filter on line 6). Drafts are already built. We just need to add the draft banner.

Replace the full content of `src/pages/blog/[...slug].astro` with:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
const isDraft = post.data.draft === true;
---

<BaseLayout title={post.data.title} description={post.data.description}>
  {isDraft && (
    <div id="draft-banner" class="mb-6 px-4 py-2 rounded bg-amber-100 dark:bg-amber-900/30 border border-amber-300 dark:border-amber-700 flex items-center justify-between gap-4">
      <span class="text-amber-800 dark:text-amber-200 text-sm font-mono font-semibold tracking-wide">DRAFT</span>
      <button
        id="banner-publish-btn"
        class="hidden px-3 py-1 rounded text-xs font-medium bg-green-600 text-white hover:bg-green-700"
        data-slug={post.slug}
      >
        Publish
      </button>
    </div>
  )}

  <article>
    <header class="mb-8">
      <h1 class="text-3xl font-bold mb-2">{post.data.title}</h1>
      <time class="text-[var(--text-muted)] text-sm font-mono">
        {post.data.date.toISOString().split('T')[0]}
      </time>
    </header>
    <div class="prose prose-lg dark:prose-invert max-w-none" id="blog-prose">
      <Content />
    </div>
  </article>

  {isDraft && (
    <script is:inline>
    (function() {
      var STORAGE_KEY = 'bhavanaai-gh-pat';
      var REPO = 'varunr89/bhavanaai';
      var pat = localStorage.getItem(STORAGE_KEY);
      var btn = document.getElementById('banner-publish-btn');
      if (!pat || !btn) return;

      btn.classList.remove('hidden');

      btn.addEventListener('click', async function() {
        var slug = btn.dataset.slug;
        if (!confirm('Publish "' + slug + '"? This will go live after the site rebuilds.')) return;

        btn.disabled = true;
        btn.textContent = 'Publishing...';

        try {
          var filePath = 'src/content/blog/' + slug + '.md';
          var res = await fetch('https://api.github.com/repos/' + REPO + '/contents/' + filePath, {
            headers: { 'Authorization': 'Bearer ' + pat }
          });
          if (!res.ok) throw new Error('Could not read file: ' + res.status);

          var fileData = await res.json();
          var content = atob(fileData.content);
          var updated = content.replace(/^draft:\s*true\s*$/m, 'draft: false');
          if (updated === content) { alert('Could not find "draft: true" in frontmatter.'); btn.disabled = false; btn.textContent = 'Publish'; return; }

          var putRes = await fetch('https://api.github.com/repos/' + REPO + '/contents/' + filePath, {
            method: 'PUT',
            headers: { 'Authorization': 'Bearer ' + pat, 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: 'publish: ' + slug, content: btoa(updated), sha: fileData.sha })
          });
          if (!putRes.ok) throw new Error('Could not update file: ' + putRes.status);

          btn.textContent = 'Published!';
          btn.classList.remove('bg-green-600', 'hover:bg-green-700');
          btn.classList.add('bg-gray-400');
        } catch (err) {
          alert('Error: ' + err.message);
          btn.disabled = false;
          btn.textContent = 'Publish';
        }
      });
    })();
    </script>
  )}
</BaseLayout>

<style is:global>
  .prose img {
    max-width: 100%;
    width: 100%;
    height: auto;
    border-radius: 0.5rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .dark .prose img {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
  }

  .prose .sources {
    font-size: 0.8rem;
    line-height: 1.5;
    color: var(--text-muted);
  }

  .prose .sources h4 {
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .prose .insight {
    background: color-mix(in srgb, var(--link) 8%, transparent);
    border-left: 3px solid var(--link);
    border-radius: 0 0.375rem 0.375rem 0;
    padding: 0.75rem 1rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    line-height: 1.6;
  }

  .prose .insight p {
    margin: 0;
  }

  .prose .insight code {
    font-size: 0.85em;
  }
</style>
```

**Step 2: Test manually**

- With a test draft post in the content collection, visit its URL `/blog/test-draft`
- Verify the yellow "DRAFT" banner appears at the top
- Verify the "Publish" button is hidden when not logged in
- Sign in at `/admin`, revisit the draft page
- Verify the "Publish" button now appears in the banner
- Visit a published post -- verify NO draft banner appears

**Step 3: Commit**

```bash
git add src/pages/blog/[...slug].astro
git commit -m "feat: add draft banner and publish button to blog posts"
```

---

### Task 5: Inline Commenting System

Port the commenting system from the short_projects preview.html into the blog layout. The commenting system activates only in admin mode on blog post pages.

This is the largest task. The commenting JS from `short_projects/ai-productivity-gap/post/preview.html` (lines 734-1410) needs to be adapted to work within the Astro blog layout.

**Files:**
- Create: `src/scripts/comments.js` -- The full commenting system
- Modify: `src/pages/blog/[...slug].astro` -- Mount the commenting UI and load the script
- Modify: `src/styles/global.css` -- Add commenting CSS

**Step 1: Create the commenting script**

Create `src/scripts/comments.js`. This is the commenting engine ported from preview.html with these changes:
- Targets `.prose` inside `#blog-prose` (the Astro blog layout) instead of a standalone `.prose`
- Uses the existing Astro layout instead of its own page structure
- Includes the GitHub API sync (save/load feedback to repo)
- Only initializes when admin mode is active (PAT in localStorage)

The script is a self-contained IIFE. Port the full commenting system from `/Users/varunr/projects/short_projects/ai-productivity-gap/post/preview.html` (lines 734-1410) with the following modifications:

1. **Initialization guard**: Wrap everything in an admin mode check:
   ```js
   var pat = localStorage.getItem('bhavanaai-gh-pat');
   if (!pat) return; // Not in admin mode, do nothing
   ```

2. **DOM targeting**: Change `document.querySelector('.prose')` to `document.getElementById('blog-prose')`.

3. **Comments column**: Create and append the comments column dynamically instead of expecting it in the HTML. Create a `div.comments-column` and insert it as a sibling to the main content container.

4. **Feedback banner**: Create and prepend the "Save Feedback" and "Clear All" buttons dynamically at the top of the article.

5. **GitHub API sync**: Replace the File System Access API `showSaveFilePicker` in `saveFeedback()` with a GitHub Contents API commit:
   ```js
   var REPO = 'varunr89/bhavanaai';
   var slug = window.location.pathname.replace(/^\/blog\//, '').replace(/\/$/, '');
   var feedbackPath = 'public/feedback/' + slug + '.json';
   ```
   On save: PUT to `https://api.github.com/repos/{REPO}/contents/{feedbackPath}`
   On load: GET from `https://api.github.com/repos/{REPO}/contents/{feedbackPath}` (or fetch from deployed URL `https://me.bhavanaai.com/feedback/{slug}.json`)

6. **Load from GitHub on init**: After checking localStorage, also fetch `feedback/{slug}.json` from the deployed site. If it exists, merge with localStorage comments (GitHub version wins for matching IDs, localStorage adds new ones).

7. **Include image commenting support**: Port the image commenting additions (click-to-comment on images, `type: 'image'` comments, `data-comment-ids` attribute, image outline highlighting).

The full script should be approximately 500-700 lines. Port all functions from the preview.html:
- `slugify`, `generateId`, `truncate`, `removeAllChildren`, `getNearestHeading`, `getContainingParagraph`, `getCharOffsetInParagraph`
- `wrapRangeWithMark`, `findAndHighlightText`, `removeHighlight`
- `getImageForComment`, `addImageHighlight`, `removeImageHighlight`, `getAnchorForComment`
- `renderAllCards`, `createMarginCard`, `createInlineCard`, `positionMarginCards`
- `setActiveComment`, `scrollToCard`, `scrollToHighlight`
- `showAddCommentButton`, `removeAddCommentButton`, `showCommentInput`, `removeCommentInput`, `submitComment`
- `deleteComment`
- `saveToLocalStorage`, `loadFromLocalStorage`, `restoreComments`
- `saveFeedback` (MODIFIED: GitHub API instead of file picker)
- `loadFeedbackFromGitHub` (NEW: fetch from deployed URL on init)
- `clearAllComments`
- `handleMouseUp`, `onImageClick`, `handleClick`, `handleResizeOrScroll`

**Step 2: Add commenting CSS to global.css**

Append to `src/styles/global.css` all the commenting styles from the preview.html (lines 169-534 of the original file). These include:
- `.comments-column` layout
- `.comment-highlight` mark styles
- `.comment-highlight-img` image styles
- `.comment-card` margin cards
- `.add-comment-btn` floating button
- `.comment-input-container` textarea popup
- `.comment-card-inline` for narrow screens
- Media queries for wide/narrow screen switching
- `.comment-feedback-banner` for Save/Clear buttons
- Dark mode variants for all of the above

Prefix all selectors with `.admin-mode` so they only apply when admin mode is active. The script adds `admin-mode` class to the body.

**Step 3: Modify blog slug page to load the script**

In `src/pages/blog/[...slug].astro`, add at the bottom (before closing `</BaseLayout>`):

```html
<script src="../scripts/comments.js"></script>
```

Note: Astro will bundle this. If it causes issues with the `is:inline` scripts, use `<script is:inline src="/scripts/comments.js"></script>` and place the file in `public/scripts/` instead.

**Step 4: Create the page layout adjustments**

The commenting system needs a wider page layout to fit the margin comments column. The script should dynamically adjust the layout when admin mode is active:
- Add `admin-mode` class to `<body>`
- The CSS for `.admin-mode` widens the max-width to accommodate the comments column
- On narrow screens (mobile), fall back to inline cards below each comment

**Step 5: Test manually**

- Visit a blog post while logged out -- verify NO commenting UI appears
- Sign in at `/admin`, visit a blog post
- Verify the "Save Feedback" and "Clear All" buttons appear
- Select text -- verify the "Comment" button appears
- Add a comment -- verify margin card appears
- Click an image -- verify the "Comment" button appears
- Add an image comment -- verify it appears with "Chart:" prefix
- Click "Save Feedback" -- verify it commits to the GitHub repo (check repo for `public/feedback/{slug}.json`)
- Open the same page on another device/browser, sign in -- verify comments load from GitHub
- Delete a comment, save again -- verify updated in repo

**Step 6: Commit**

```bash
git add src/scripts/comments.js src/styles/global.css src/pages/blog/[...slug].astro
git commit -m "feat: add inline commenting system for admin mode"
```

---

### Task 6: Feedback Directory Setup

Ensure the `public/feedback/` directory exists and is in the build.

**Files:**
- Create: `public/feedback/.gitkeep`

**Step 1: Create the directory**

```bash
mkdir -p /Users/varunr/projects/bhavanaai/public/feedback
touch /Users/varunr/projects/bhavanaai/public/feedback/.gitkeep
```

**Step 2: Commit**

```bash
git add public/feedback/.gitkeep
git commit -m "feat: add feedback directory for comment storage"
```

---

### Task 7: End-to-End Smoke Test

Verify the full flow works together.

**Files:** None (testing only)

**Step 1: Full flow test**

Run: `cd /Users/varunr/projects/bhavanaai && npm run dev`

Test this sequence:
1. Visit `/` -- verify no "Drafts" in nav
2. Visit `/admin` -- enter PAT, verify sign-in succeeds
3. Visit `/` -- verify "Drafts" appears in nav
4. Click "Drafts" -- verify draft listing page shows draft posts
5. Click a draft title -- verify post renders with "DRAFT" banner and "Publish" button
6. Select text, add a comment -- verify comment card appears in margin
7. Click an image, add a comment -- verify image comment works
8. Click "Save Feedback" -- verify commit appears in the GitHub repo
9. Open an incognito window, sign in at `/admin`, visit same draft -- verify comments load from GitHub
10. Visit a published post -- verify no draft banner, but commenting still works in admin mode

**Step 2: Build test**

Run: `npm run build`

Verify:
- Build succeeds with no errors
- Draft posts are included in the build output (`dist/blog/{draft-slug}/index.html` exists)
- Draft posts are NOT in the homepage listing
- Draft posts are NOT in the RSS feed
- The `/admin` and `/drafts` pages are in the build output

**Step 3: Final commit with any fixes**

If any issues found during testing, fix and commit.
