# LeadFlow working flow — dark mode

Fresh captures from 14 October 2026, using the existing theme without edits.
These show the local production frontend with real FastAPI/PostgreSQL services,
synthetic seed data and a disposable account. Production records were not changed.
The landing preview is the app’s explicitly labeled static illustration; workspace
and dialog screenshots show actual saved data and working controls.

Images are numbered in viewing order using `01-description.png` through
`15-description.png`. Desktop: 1440×1000 CSS pixels; laptop: 1366×768; tablet:
768×1024; mobile: 390×844. PNGs use 2× resolution for readable text. There is no
browser chrome, development badge, exposed credential or loading placeholder.

| Order | Screen | Image |
| --- | --- | --- |
| 1 | Landing page, desktop | [01-landing-page-desktop.png](01-landing-page-desktop.png) |
| 2 | Seeded lead workspace: today pinned, overdue red, all six statuses | [02-lead-workspace-desktop.png](02-lead-workspace-desktop.png) |
| 3 | Lead workspace at a laptop viewport, first screen | [03-lead-workspace-laptop.png](03-lead-workspace-laptop.png) |
| 4 | Add a lead with name, optional company and phone | [04-add-new-lead.png](04-add-new-lead.png) |
| 5 | Discussion draft with follow-up date/time and Qualified status, desktop | [05-discussion-and-follow-up-desktop.png](05-discussion-and-follow-up-desktop.png) |
| 6 | Follow-up dialog at a laptop viewport, complete form and Save Note visible | [06-discussion-and-follow-up-laptop.png](06-discussion-and-follow-up-laptop.png) |
| 7 | Themed follow-up calendar | [07-follow-up-date-picker.png](07-follow-up-date-picker.png) |
| 8 | Themed time picker minute menu | [08-follow-up-time-picker.png](08-follow-up-time-picker.png) |
| 9 | Saved discussion and follow-up, newest note first | [09-saved-discussion-timeline.png](09-saved-discussion-timeline.png) |
| 10 | Combined name search and status filter, with immediate updated summary | [10-search-and-status-filter.png](10-search-and-status-filter.png) |
| 11 | Lead workspace, tablet | [11-lead-workspace-tablet.png](11-lead-workspace-tablet.png) |
| 12 | Lead workspace, mobile | [12-lead-workspace-mobile.png](12-lead-workspace-mobile.png) |
| 13 | Mobile timeline at the top, with saved history and status | [13-discussion-timeline-mobile.png](13-discussion-timeline-mobile.png) |
| 14 | Mobile dialog scrolled to the populated follow-up form and Save Note | [14-follow-up-form-mobile.png](14-follow-up-form-mobile.png) |
| 15 | Landing page, mobile | [15-landing-page-mobile.png](15-landing-page-mobile.png) |

Full-page landing/workspace images include the entire page, except image 03,
which shows the laptop's actual first viewport. Dialog captures also show the
actual viewport. Images 13 and 14 show the same mobile dialog at different scroll
positions so both the history and complete form can be reviewed. At laptop height,
the history scrolls within the dialog while the follow-up form remains visible.

All 15 images were visually reviewed for theme, readable text, wrapping, clipping,
open picker placement and meaningful populated states. Chrome/Playwright also
verified the route/title, nonblank screens, no framework error overlay, no
horizontal overflow and no unexpected console/runtime errors. Lead creation,
status changes, note saves, follow-up save and search/filter interactions used the
real API and database. Browser plugin not available; installed Chrome/Playwright
was used. These are viewport emulations, not physical-device or Safari checks.
