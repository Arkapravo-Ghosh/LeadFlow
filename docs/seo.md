# Public metadata and search discovery

`APP_URL` supplies the public origin for canonical URLs, Open Graph/Twitter
previews, structured data, robots and the sitemap. Set it during the Vercel build
and at runtime for authentication origin checks. Changing the domain requires
an environment update and a new frontend build, not a source edit. Compose
already passes the public build argument when using the production image.

The landing page is the only indexable route. `/sitemap.xml` lists that page and
its preview image. `/robots.txt` allows the public site and excludes the private
workspace, account pages, authentication API paths and health route. Account and
workspace pages inherit `noindex, nofollow`; missing pages return 404. Crawl rules
are discovery instructions; session authentication still controls access.

`src/lib/site-metadata.ts` owns shared titles, descriptions, preview metadata and
WebSite/WebApplication JSON-LD. The homepage supplies its own canonical and index
policy. JSON-LD describes implemented features without fabricated ratings,
reviews or pricing. Existing semantic headings, navigation, image alt text,
favicon and viewport configuration are retained.

## Preview image

`public/leadflow-social.png` is an unchanged copy of the owner-provided
`screenshot-1791920524884.png` (3584×1880), supplied on 14 October 2026. It contains only the
public, explicitly illustrative example data. Both Open Graph and Twitter's
large-image card reference this same asset.

When the landing design changes, replace the PNG with an updated dark landing
screenshot. Update its width/height in `site-metadata.ts`, inspect it, and verify
the deployed image response and metadata. Do not capture a private workspace or a populated account form.

After deployment, check `/`, `/robots.txt`, `/sitemap.xml` and
`/leadflow-social.png`. Search-engine indexing and social-platform cache refreshes
are external processes; publishing metadata does not guarantee ranking or an
immediate refresh of previously cached link previews.
