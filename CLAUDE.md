# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 4.2 production-ready Chess Learning Platform. Full-stack: server-rendered HTML templates plus a small DRF REST API. Deployed to Vercel (serverless Python runtime) with PostgreSQL in production, SQLite in local dev.

## Development Commands

All commands run from `backend/`:

```bash
# First-time setup
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo     # loads demo users, courses, and chess data

# Dev server
python manage.py runserver     # http://127.0.0.1:8000

# Tests
python manage.py test
python manage.py test courses                          # single app
python manage.py test courses.tests.CourseFlowTests   # single test class

# Migrations
python manage.py makemigrations
python manage.py migrate

# Optional background worker (Celery + Redis)
celery -A config worker -l info

# Production static files
python manage.py collectstatic --noinput
```

Demo credentials (seeded by `seed_demo`):
- Admin: `admin` / `admin12345`
- Instructor: `instructor` / `instructor123`
- Student: `student` / `student123`

## Architecture

```
Chess/
├── backend/
│   ├── config/          # settings.py, urls.py, celery.py, wsgi.py, sitemaps.py
│   ├── users/           # custom AUTH_USER_MODEL, roles, email verification
│   ├── courses/         # courses, lessons, enrollments, progress tracking
│   ├── chesslab/        # FEN/PGN analysis, Stockfish, game import, check-move API
│   ├── payments/        # Stripe subscriptions, webhooks, mock fallback
│   ├── dashboard/       # home, student progress, testimonials, admin analytics
│   ├── blog/            # Article + ArticleCategory models, SEO blog
│   ├── templates/       # all HTML templates
│   └── static/          # CSS, JS, images
├── api/
│   └── index.py         # Vercel serverless WSGI entrypoint (adds backend/ to sys.path)
└── vercel.json
```

Note: `backend/api/index.py` also exists but the root `api/index.py` is the one Vercel uses. The `.env` file belongs at `backend/.env` (that is where `settings.py` reads it from via `django-environ`).

### Key design decisions

- **`chesslab/services.py`** — chess engine abstraction: uses Stockfish when `STOCKFISH_PATH` is set, otherwise falls back to a built-in material-score evaluator. Both paths expose the same `analyze_position(fen)` interface returning `{best_move, evaluation, source}`.
- **Stripe mock** — `payments/views.py` checks for `STRIPE_SECRET_KEY` and `plan.stripe_price_id` at runtime; if absent it uses a mock checkout flow. No feature flag needed.
- **Celery is optional** — the task queue is wired but not required for local dev.
- **Custom User model** (`users.User`) — extends `AbstractUser`, adds `role` field (`student`/`instructor`/`admin`), `chess_com_username`, and `is_email_verified`. Always use `AUTH_USER_MODEL` / `get_user_model()`. The `can_author_courses` property returns `True` for instructors, admins, and staff.
- **Premium access** — `Course.is_premium` is automatically set to `True` whenever `price > 0` in `Course.save()`. Access to premium course lessons requires either a direct `Enrollment` or an active `UserSubscription`.
- **Email verification** — `users/tokens.py` has `EmailVerificationTokenGenerator`. Token invalidates after use (hash includes `is_email_verified`). Without `SENDGRID_API_KEY`, emails print to console.
- **Static files** — `CompressedManifestStaticFilesStorage` (whitenoise) in production only (`DEBUG=False`). Dev uses plain `StaticFilesStorage` so tests don't require `collectstatic`.
- **Blog** — `blog/` app: `Article` + `ArticleCategory` models. Admin publishes articles; `published_at` is set via bulk action. SEO meta comes from `Article.meta_description`.

### URL structure

| Prefix | App |
|--------|-----|
| `/` | `dashboard` (home, student dashboard, testimonials) |
| `/users/` | `users` (signup, login, profile, email verify) |
| `/accounts/` | Django built-in auth views (login, logout, password reset) |
| `/courses/` | `courses` (listing, detail, enroll, create) |
| `/chess/` | `chesslab` (analyzer, game player, PGN import, REST API) |
| `/payments/` | `payments` (plans, checkout, Stripe webhook) |
| `/blog/` | `blog` (article list, article detail) |
| `/admin/` | Django admin |
| `/admin/analytics/` | Staff-only analytics dashboard |
| `/sitemap.xml` | XML sitemap (courses + blog + static) |
| `/robots.txt` | robots.txt |

REST endpoints:
- `GET /courses/api/courses/` — paginated course list
- `GET /courses/api/courses/<slug>/` — course detail with lessons
- `POST /chess/api/analyze/` — FEN analysis (authenticated)
- `POST /chess/api/check-move/` — validate a move against the engine (authenticated); returns `{correct, best_move, evaluation, feedback}`

## Environment Variables

Place at `backend/.env` (copy from `backend/.env.example`):

```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=
VERCEL_URL=          # auto-appended to ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS when set
DATABASE_URL=        # defaults to SQLite; set postgres:// for production
STOCKFISH_PATH=      # optional; omit to use fallback evaluator
STRIPE_PUBLIC_KEY=   # optional; omit to use mock checkout
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
CELERY_BROKER_URL=   # optional; e.g. redis://localhost:6379/0
CELERY_RESULT_BACKEND=
SENDGRID_API_KEY=    # optional; omit to print emails to console
DEFAULT_FROM_EMAIL=noreply@chesslearn.com
```

## Vercel Deployment

1. Push to GitHub; import project in Vercel.
2. Set env vars: `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL` (Neon/Supabase Postgres), `ALLOWED_HOSTS`, `VERCEL_URL`, `CSRF_TRUSTED_ORIGINS`, `SENDGRID_API_KEY`, `DEFAULT_FROM_EMAIL`.
3. Install and build commands are in `vercel.json` (`pip install -r requirements.txt` / `python backend/manage.py collectstatic --noinput`).
4. Run migrations against production DB locally: `python backend/manage.py migrate`.

SQLite is not persistent on Vercel — PostgreSQL is required in production.
Media uploads are not persistent on Vercel — use S3/Cloudinary if media uploads are needed.
