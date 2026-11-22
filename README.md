# MuniDesk

> Client municipalities data management made easy.

REST API that centralizes and manages strategic information about the municipalities served by
service providers — legal consulting, accounting, public management and related fields —
including their public bodies and the public officials relevant to each provider's operation.

## Project status

Stable. See the [releases page](https://github.com/raulin0/munidesk/releases)
for the changelog.

## Tech stack

- Python 3.15+ (installed and managed by [uv](https://docs.astral.sh/uv/))
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [pytest](https://docs.pytest.org/) with [pytest-django](https://pytest-django.readthedocs.io/)
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

6. Create an administrator account:

   ```bash
   uv run python manage.py createsuperuser
   ```

7. Start the development server:

   ```bash
   uv run python manage.py runserver
   ```

The API is available at <http://127.0.0.1:8000/api/> and the Django Admin at
<http://127.0.0.1:8000/admin/>.

## Environment variables

| Variable        | Description                                                  | Default               |
| --------------- | ------------------------------------------------------------ | --------------------- |
| `SECRET_KEY`    | Django secret key. Required.                                 | —                     |
| `DEBUG`         | Enables debug mode. Never enable it outside local use.       | `False`               |
| `ALLOWED_HOSTS` | Comma-separated list of hosts allowed to serve the project.  | `localhost,127.0.0.1` |

The `.env` file is ignored by Git. Only `.env.example` is versioned.

## Data model

| Model            | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `Municipality`   | Client municipality: name, state (UF) and 7-digit IBGE code.                |
| `PublicBody`     | Body of a municipality (city hall, secretariat, etc.) with optional acronym. |
| `Position`       | Catalog of positions held by public officials.                              |
| `PublicOfficial` | Official linked to a public body and a position, with contact details.      |

Business rules:

- The IBGE code is unique and must have exactly 7 digits.
- A municipality name is unique within its state.
- A public body acronym is optional. When provided, it must follow the usual Brazilian municipal
  pattern (2 to 15 uppercase letters, e.g. `SEMED`) and be unique within the municipality.
- A public body name is unique within the municipality, and position names are unique.
- Phones use the `(99) 99999-9999` or `(99) 9999-9999` format.
- Records referenced by other records cannot be deleted.

User-facing labels, help texts and validation messages are in Brazilian Portuguese.

## API

All endpoints require an authenticated user (session or HTTP Basic authentication). List
responses are paginated with 20 items per page (`?page=2`).

| Resource         | Endpoint                  | Public body `kind` values (for reference)  |
| ---------------- | ------------------------- | ------------------------------------------ |
| Municipalities   | `/api/municipalities/`    |                                            |
| Public bodies    | `/api/public-bodies/`     | `city_hall`, `secretariat`, `city_council`, `autarchy`, `foundation`, `other` |
| Positions        | `/api/positions/`         |                                            |
| Public officials | `/api/public-officials/`  |                                            |

Each resource supports:

| Method   | Path          | Action               |
| -------- | ------------- | -------------------- |
| `GET`    | `/<resource>/`      | List records   |
| `POST`   | `/<resource>/`      | Create a record |
| `GET`    | `/<resource>/<id>/` | Retrieve a record |
| `PUT`    | `/<resource>/<id>/` | Replace a record |
| `PATCH`  | `/<resource>/<id>/` | Partially update a record |
| `DELETE` | `/<resource>/<id>/` | Delete a record (`409 Conflict` if other records depend on it) |

Example:

```bash
curl -u admin:your-password \
  -H "Content-Type: application/json" \
  -d '{"name": "Campinas", "state": "SP", "ibge_code": "3509502"}' \
  http://127.0.0.1:8000/api/municipalities/
```

The browsable API is available in the browser after logging in at
<http://127.0.0.1:8000/api-auth/login/>.

## Running tests

```bash
uv run pytest
```

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

## Versioning

The project follows [Semantic Versioning](https://semver.org/). The current version is defined in
`pyproject.toml` (`uv version` prints it). Each release is published on GitHub Releases with a
tag in the plain `MAJOR.MINOR.PATCH` format (for example, `1.0.0`) and changelog notes.
