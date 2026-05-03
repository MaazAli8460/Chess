# Postgres Setup (Neon or Supabase)

This app uses `DATABASE_URL` from the environment. Use a hosted Postgres provider in production.

## Neon (recommended)

1. Create a project at [neon.tech](https://neon.tech)
2. Copy the connection string.
3. Add it to your Vercel project env as `DATABASE_URL`.

Example:

```text
postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
```

## Supabase

1. Create a project at [supabase.com](https://supabase.com)
2. Get the connection string from Settings → Database.
3. Add it to your Vercel project env as `DATABASE_URL`.

Example:

```text
postgresql://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require
```

## Local sanity check

Run migrations using the production database URL in your local `.env`:

```bash
python manage.py migrate
```

If migrations run, the connection is working.
