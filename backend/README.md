# Chess Learning Platform MVP

A complete working Django product for a chess learning business with:

- Custom auth and role-based users (student/instructor/admin)
- Course catalog, lessons, enrollment, and progress tracking
- Student dashboard with progress summaries
- Chess FEN analysis API and UI (Stockfish optional, fallback evaluator included)
- Subscription plans, mock checkout, Stripe-ready checkout and webhook endpoint
- Django admin for content and operations
- Demo seed command for instant data

## Tech Stack

- Django + Django REST Framework
- SQLite (default), PostgreSQL-ready via `DATABASE_URL`
- Celery + Redis wiring
- Stripe integration hooks

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment file:

   ```bash
   copy .env.example .env
   ```

4. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Seed demo content and users:

   ```bash
   python manage.py seed_demo
   ```

6. Start server:

   ```bash
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000`.

## Demo Credentials

- `admin / admin12345`
- `instructor / instructor123`
- `student / student123`

## API Endpoints

- `GET /courses/api/courses/`
- `GET /courses/api/courses/<slug>/`
- `POST /chess/api/analyze/` (authenticated)

## Stripe Notes

- If Stripe keys are not set, the app falls back to mock subscription flow.
- Add `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` to use live webhook verification.

## Background Workers

Celery is wired in `config/celery.py`.

Run worker (optional):

```bash
celery -A config worker -l info
```

## Testing

```bash
python manage.py test
```

## Postgres Setup

See [backend/docs/postgres.md](backend/docs/postgres.md) for Neon/Supabase steps
and example `DATABASE_URL` values. The app uses `psycopg` for Postgres in prod.

## Deploying to Vercel

Vercel uses the serverless Python runtime. For production, use a hosted Postgres
database (SQLite is not persistent on Vercel).

1. Ensure the repo root contains:
   - `vercel.json`
   - `requirements.txt` (which includes `-r backend/requirements.txt`)
2. Add environment variables in Vercel:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DATABASE_URL` (Postgres)
   - `ALLOWED_HOSTS` (e.g. `your-project.vercel.app`)
   - `VERCEL_URL` (e.g. `your-project.vercel.app`)
   - `CSRF_TRUSTED_ORIGINS` (e.g. `https://your-project.vercel.app`)
3. Set the build command in Vercel to:

   ```bash
   python backend/manage.py collectstatic --noinput
   ```

4. Run migrations against your production database locally:

   ```bash
   python backend/manage.py migrate
   ```

Notes:

- Media uploads are not persistent on Vercel. Use S3/Cloudinary for uploads.
- Stockfish requires a server binary; the app falls back to the lightweight evaluator if not set.
