# V2 Screenshot Index

Quick reference for all v2 authenticated app screenshots.

All files: `/Users/varunr/projects/short_projects/ai-tools-evolution/charts/`

---

## Main Application

| Screenshot | Description | URL |
|------------|-------------|-----|
| `v2_auth_home.png` | Home landing page with "Browse Channels" CTA | `https://podcast.bhavanaai.com/` |
| `v2_channels_list.png` | Complete channels list (30+ channels) | `https://podcast.bhavanaai.com/channels` |
| `v2_subscriptions.png` | User's subscribed podcasts (15 subscriptions) | `https://podcast.bhavanaai.com/subscriptions` |
| `v2_account.png` | Account settings, profile, channel request form | `https://podcast.bhavanaai.com/account` |
| `v2_channel_page.png` | Individual channel detail (loading state) | `https://podcast.bhavanaai.com/channels/[id]` |

---

## Admin Dashboard

| Screenshot | Description | URL |
|------------|-------------|-----|
| `v2_admin_dashboard.png` | Dashboard with queue metrics (Pending: 2, Sent: 5, Failed: 50) | `https://podcast.bhavanaai.com/admin` |
| `v2_admin_users.png` | User management (2 users shown) | `https://podcast.bhavanaai.com/admin/users` |
| `v2_admin_channels.png` | Channel management with transcription/summarization metrics | `https://podcast.bhavanaai.com/admin/channels` |
| `v2_admin_requests.png` | Channel requests (empty state) | `https://podcast.bhavanaai.com/admin/requests` |
| `v2_admin_deliveries.png` | Delivery queue monitoring (Active: 0, Failed: 0) | `https://podcast.bhavanaai.com/admin/deliveries` |
| `v2_admin_episodes.png` | Episodes management (loading state) | `https://podcast.bhavanaai.com/admin/episodes` |
| `v2_admin_youtube.png` | YouTube audio download monitoring | `https://podcast.bhavanaai.com/admin/youtube-audio` |

---

## Key Channels Shown

**In Channels List:**
- All-In with Chamath, Jason, Sacks & Friedberg
- Dwarkesh Podcast (both Podcast and YouTube versions)
- Odd Lots
- Lex Fridman Podcast
- Deep Questions with Cal Newport
- Science Friday
- The Exonomist: the climbing podcast
- Raising Good Humans
- the Sharp End Podcast
- ParentData with Emily Oster
- Bloomberg Technology
- Data Skeptic
- Possible
- Science Vs
- Lenny's Podcast
- The Diary Of A CEO with Steven Bartlett
- Huberman Lab
- Making Sense with Sam Harris
- The Pragmatic Engineer Podcast
- The Art of Manliness podcast
- StarTalk Radio

**User's Subscriptions (15 total):**
1. Odd Lots (1066 episodes)
2. Raising Good Humans (1525 episodes)
3. the Sharp End Podcast (133 episodes)
4. ParentData with Emily Oster (138 episodes)
5. Science Friday (267 episodes)
6. Bloomberg Technology (890 episodes)
7. Data Skeptic (676 episodes)
8. Lex Fridman Podcast (492 episodes)
9. All-In with Chamath, Jason, Sacks & Friedberg (322 episodes)
10. Science Vs (318 episodes)
11. Possible (232 episodes)
12. Deep Questions with Cal Newport (402 episodes)
13. StarTalk Radio (1085 episodes)
14. The Pragmatic Engineer Podcast (YouTube, 109 episodes)
15. Dwarkesh Podcast (YouTube, 113 episodes)

---

## Design System at a Glance

**Colors:**
- Primary: Black
- Background: White
- Text: Black + Gray variants
- Success: Green
- Error: Red

**Typography:**
- System font stack
- Clear hierarchy (bold headings, regular body)

**Components:**
- Black rounded buttons
- Clean tables with sortable columns
- Card-based layouts
- Icon buttons (trash, gear)
- Search boxes
- Toggle buttons (YouTube | Podcast)
- Status badges
- Loading skeletons

**Layout:**
- Top navigation bar (main app)
- Left sidebar (admin dashboard)
- Max-width constrained content
- Generous whitespace
- Mobile-responsive patterns

---

## Tech Stack Observations

- **Framework:** Next.js or React
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui (or similar)
- **Icons:** Lucide or similar
- **Auth:** Magic link (passwordless)
- **Backend:** Queue-based processing (evident from admin dashboard)

---

## Feature Highlights

### User Features
- Browse 30+ podcasts/YouTube channels
- Subscribe/unsubscribe
- Request new channels (self-service)
- AI-generated summaries via email
- Account management

### Admin Features
- System health monitoring
- User management
- Channel management with detailed metrics
- Request review and approval
- Delivery monitoring
- Episode tracking
- YouTube download status
- Search across all admin sections

---

## Processing Pipeline (Inferred)

1. Channel ingestion (RSS/YouTube)
2. Episode detection
3. Audio download (YouTube)
4. Transcription
5. AI summarization
6. Delivery queue
7. Email sending
8. Failure tracking and retry

---

## View Full Documentation

See `V2_SCREENSHOT_TOUR_SUMMARY.md` for detailed analysis of every screen, design patterns, technical observations, and feature richness assessment.
