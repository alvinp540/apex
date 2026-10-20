# ApexStratos Deployment

## Current Architecture

- Frontend: React 18 and Vite 5; install with npm and build with `npm run build` from `apex_frontend`.
- Backend: Django 5.2, Django REST Framework, Channels and Daphne; dependencies are listed in `apex_backend/requirements.txt`.
- Database: SQLite for local development unless `DB_NAME` selects MySQL. MySQL deployments use the pinned `mysqlclient` driver from `apex_backend/requirements.txt`.
- Migrations: Django migrations, applied with `python manage.py migrate` only after a production backup and migration review.
- Existing process declaration: `apex_backend/Procfile` defines Daphne and a Celery worker. It does not establish that Pinnacle/cPanel supports Procfiles, Daphne, Redis or persistent workers.
- Frontend API: `/api/v1` by default. WebSockets use same-origin `ws:`/`wss:` unless `VITE_WS_BASE_URL` is set.
- Local Vite proxy: copy `apex_frontend/.env.example` to `.env`; set `VITE_DEV_API_TARGET` and `VITE_DEV_WS_TARGET` to the local backend. These proxy values are used only by the Vite development server. Set `VITE_API_BASE_URL` and, if needed, `VITE_WS_BASE_URL` to the production API origins in the production build environment; do not ship local `.env` files.
- Recovery repository: `https://github.com/fiddle254/Apex-loading.git`. Confirm the hosting deployment integration before deploying.

## Vercel Deployment

The frontend and backend are configured as two Vercel projects from this repository:

1. Create a Vercel project with the root directory set to `apex_frontend`. It uses `apex_frontend/vercel.json` to build the Vite app and provide SPA route fallback.
2. Create a second Vercel project with the root directory set to `apex_backend`. It uses Django's ASGI entrypoint and registers the Celery app as a Vercel Queues subscriber. Python 3.13 is selected by `apex_backend/.python-version`.
3. Assign `apexstratos.co.ke` (and optionally `www.apexstratos.co.ke`) to the frontend Vercel project. Assign `api.apexstratos.co.ke` to the backend Vercel project. Add each domain to the matching Vercel project's Domains settings, then apply the exact DNS records Vercel shows at the domain's DNS provider. Do not change existing DNS records until you have confirmed which currently serve email and other services.
4. Configure a persistent PostgreSQL database and set `DATABASE_URL` in the backend project's Vercel environment. This repository supports PostgreSQL URLs, as well as the existing MySQL variables for non-Vercel hosts. Vercel's function filesystem is not persistent; do not deploy the local SQLite database or store uploads on the function filesystem.
5. Configure `REDIS_URL` with a Redis-compatible service that supports the Pub/Sub operations used by Channels. This is separate from Celery: Vercel Queues is the Celery broker on Vercel.
6. Add backend environment variables: `DJANGO_SETTINGS_MODULE=apex_backend.settings.production`, `DJANGO_SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, `ALLOWED_HOSTS=api.apexstratos.co.ke`, `CORS_ALLOWED_ORIGINS=https://apexstratos.co.ke,https://www.apexstratos.co.ke`, `CSRF_TRUSTED_ORIGINS=https://apexstratos.co.ke,https://www.apexstratos.co.ke`, and `FRONTEND_URL=https://apexstratos.co.ke`. Add provider credentials (for example Cloudinary and payment/email settings) only when those features are configured. Vercel deployment hostnames are added to `ALLOWED_HOSTS` automatically; keep the custom API hostname in the list.
7. Add `VITE_API_BASE_URL=https://api.apexstratos.co.ke/api/v1` to the frontend project's Vercel environment. Set `VITE_WS_BASE_URL=wss://api.apexstratos.co.ke` for notification WebSockets. Rebuild the frontend after changing either variable.
8. Apply reviewed Django migrations to the configured production database before directing users to the deployment. Existing SQLite or cPanel data is not copied automatically; back it up and plan a deliberate migration before switching traffic.

Vercel's Django Channels WebSocket support and Vercel Queues are currently beta features. Vercel Queues runs Celery tasks through serverless subscribers rather than a persistent worker; task delivery is at least once, so tasks should remain safe to retry. WebSocket connections can close at the configured function duration and the frontend reconnects automatically. Verify these features and their current plan limits in Vercel before production use. The PostgreSQL and Redis-compatible services are external integrations and may have separate limits or charges.

## Local Validation

From the repository root, install frontend dependencies with `npm ci` in `apex_frontend`. Run `npm run build` there. For linting, first resolve the current ESLint 9 configuration error (the repository has no `eslint.config.*`).

Create a Python virtual environment for the backend, install `apex_backend/requirements.txt`, then from `apex_backend` run:

```powershell
python manage.py check --settings=apex_backend.settings.development
python manage.py test apps.cohorts.tests.test_assessment_integrity --settings=apex_backend.settings.development
python manage.py test apps.cohorts.tests.test_allocation --settings=apex_backend.settings.development
python manage.py test apps.cohorts.tests.test_content_import --settings=apex_backend.settings.development
```

Do not run seed, reset, flush or deletion commands against production.

## Assessment Content Import Status

The verified local SQLite import contains 1,504 complete assessment records and 15,040 questions across the three libraries. Nine source packs containing 656 assessments remain excluded because strict validation finds repeated prompts; those packs require meaningful content correction and revalidation. Three existing starter assessments in occupied schedule slots are preserved by the partial importer.

The importer is validation-only by default. Review a local preflight report with:

```powershell
python manage.py bootstrap_apexstratos_libraries --allow-partial --preserve-existing-slots --report-json .\assessment-preflight.json --settings=apex_backend.settings.development
```

The `--apply` and `--publish` options must not be used against production without an approved deployment, a database backup, and a zero-failure content report. Never publish Medical and Health or Law and Society content before its required qualified review. Reconcile database and API inventories after any import; a successful command alone does not establish that the target library is complete or published.

## Production Configuration

Set these in the hosting platform's protected environment-variable UI, not in Git:

- `DJANGO_SECRET_KEY`: newly generated production-only secret.
- `ALLOWED_HOSTS`: production backend hostnames.
- `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`: exact HTTPS frontend origins.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: production database connection.
- `REDIS_URL`: production Redis URL if the deployed Channels/Celery features require Redis.
- `FRONTEND_URL`: production frontend base URL.
- `APEX_VERSION`, `GIT_COMMIT`: release label and exact deployed commit.
- Provider/storage/email values as required: `CLOUDINARY_*`, `STRIPE_*`, `MPESA_*`, `EMAIL_*`.

`apex_backend/.env.example` and `apex_frontend/.env.example` contain names only. Never upload local `.env` files or add secret values to GitHub. Rotate any credential that has ever been committed.

Production settings now fail early unless core deployment identity, host, secret and database variables are configured. `/health` returns `200` only when Django can connect to the configured database and otherwise returns `503`. `/version` returns only the configured release label and Git commit; it does not disclose secrets.

## Pinnacle/cPanel Setup To Confirm

No hosting control-panel access or provider configuration is available in this workspace. Before selecting an exact deployment procedure, confirm with Pinnacle/cPanel support:

1. Whether the account supports cPanel Git Version Control deployment from this GitHub repository, or requires SSH/manual upload.
2. Whether it supports a Python application with the required Python version, Django, ASGI/Daphne, Channels, WebSockets, Redis and Celery worker processes.
3. The provider-assigned application root, startup command, environment-variable interface, static-file mapping and SPA history fallback configuration.
4. The production database engine/version, backup procedure, migrations policy, outbound network and persistent-media policy.
5. TLS termination/proxy headers and the exact public API/WebSocket origin and callback URLs.

Do not assume Node/Python Application Manager, Procfile support, SSH access, Redis, or deployment hooks until the account confirms them. If the account only supports static frontend hosting and PHP, the current Django/Channels backend needs a separate compatible host; it cannot be deployed as a static cPanel site.

## Release, Verification and Rollback

1. Choose a release label and record the exact commit with `git rev-parse HEAD` after committing the tested source.
2. Build the frontend from that commit. Configure the hosting deployment to build or upload that exact commit, not a working directory snapshot.
3. Back up the production database using the host's supported backup tool. Review pending migrations and compatibility before applying them.
4. Deploy application code and required static assets; restart only using the provider-documented mechanism.
5. Set `APEX_VERSION` and `GIT_COMMIT` from that release. Confirm `/health`, `/version`, the homepage, authentication, API and WebSocket behavior on the public domain.
6. Keep the previous release commit/build available. If application verification fails, restore the prior code/build and configuration. Do not roll back or replace production data; use a forward fix for schema changes unless the database owner approves a tested recovery plan.

Live deployment and `https://Apexstratos.co.ke` verification require authorized hosting access and are not performed by local builds.