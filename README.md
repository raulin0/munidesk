# MuniDesk

> Client municipalities data management made easy.

REST API that centralizes and manages strategic information about the municipalities served by
service providers — legal consulting, accounting, public management and related fields —
including their public bodies and the public officials relevant to each provider's operation.

## Project status

Under development.

## Tech stack

- Python 3.15+ (installed and managed by [uv](https://docs.astral.sh/uv/))
- [Django](https://www.djangoproject.com/)
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting

## Requirements

- [Git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

No global Python installation is needed: uv downloads and uses the version pinned in
`.python-version`.

## Getting started

1. Clone the repository and enter the project folder:

   ```bash
   git clone https://github.com/raulin0/munidesk.git
   cd munidesk
   ```

2. Install the dependencies (this creates the `.venv` virtual environment):

   ```bash
   uv sync
   ```

3. Create your local environment file from the template:

   ```bash
   cp .env.example .env
   ```

4. Generate a secret key and paste it as the `SECRET_KEY` value in `.env`:

   ```bash
   uv run python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

5. Apply the database migrations:

   ```bash
   uv run python manage.py migrate
   ```

6. Start the development server:

   ```bash
   uv run python manage.py runserver
   ```

## Environment variables

| Variable        | Description                                                  | Default               |
| --------------- | ------------------------------------------------------------ | --------------------- |
| `SECRET_KEY`    | Django secret key. Required.                                 | —                     |
| `DEBUG`         | Enables debug mode. Never enable it outside local use.       | `False`               |
| `ALLOWED_HOSTS` | Comma-separated list of hosts allowed to serve the project.  | `localhost,127.0.0.1` |

The `.env` file is ignored by Git. Only `.env.example` is versioned.

## Code quality

```bash
uv run ruff check .
uv run ruff format .
```

## Development workflow

- `main`: stable, released code.
- `develop`: integration branch.
- `feature/*`: short-lived branches created from `develop` and merged back through pull requests.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/).