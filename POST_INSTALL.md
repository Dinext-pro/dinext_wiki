# Wiki Post-Install Steps

Use these steps after installing the `wiki` app on a Frappe site.

## 1. Install the app on the site

```bash
bench --site <site-name> install-app wiki
bench --site <site-name> migrate
```

## 2. Build Wiki assets

Run this from the `apps/wiki` directory:

```bash
yarn install --frozen-lockfile
yarn build
```

This builds both:

- public page CSS at `wiki/public/css/tailwind.css`
- the `/wiki` Vue app at `wiki/public/frontend` and `wiki/www/wiki.html`

## 3. Publish the initial wiki content

The installer creates a default Wiki Space with route `docs` and a welcome page.
Before opening it publicly, confirm:

- the Wiki Space is published
- the root Wiki Document group is published
- the welcome Wiki Document is published

For public guest access, add a role row on the Wiki Space:

```text
Role: Guest
Permission Level: Read
```

Without this row, anonymous users will get a 404 even if the space and page are
published.

## 4. Clear caches and restart

```bash
bench --site <site-name> clear-cache
bench --site <site-name> clear-website-cache
bench restart
```

## 5. Verify

```bash
curl -I -L https://<site-name>/wiki
curl -I -L https://<site-name>/docs
curl -I https://<site-name>/assets/wiki/frontend/index.html
```

Expected results:

- `/wiki` returns `200 OK` for the Wiki admin SPA
- `/docs` redirects to the first published page and returns `200 OK`
- `/assets/wiki/frontend/index.html` returns `200 OK`
