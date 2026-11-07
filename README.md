# EDDAI-EliteDangerousApiInterface
A web API and web application for searching information for the game Elite Dangerous

## Project Description

This is an open-source project written in Python, Django, Django REST Framework, and Celery, while the web interface will be developed in Vue.js. Currently, the project is still in development and features an alpha version with the API available on the main branch at the URL [eddai.italiangamingsystem.it](http://eddai.italiangamingsystem.it).

## How It Works

1. **Data Collection**: EDDAI collects data from [EDDN](https://github.com/EDCD/EDDN), processes and saves the information in the database. It is also possible to send data through the available APIs.
2. **Data Access**: Users can access the data through API endpoints, which provide structured and easy-to-use information. Additionally, it will be possible to access the data through a web application.

## Container Deployment

The frontend and backend are independent images. Traefik terminates HTTPS on the
same public hostname and routes `/api/`, `/admin/`, `/users/`, `/static/`,
`/healthz/` and the currently unused `/media/` to Django. All other paths go to
the Vue static server. API paths without a trailing slash also reach Django.

- Frontend: Node builds Vue, then non-root Nginx serves the bundled HTML, CSS and
    JavaScript on port 8080. SPA navigation falls back to `index.html`; missing
    assets return 404. It does not need the backend image or a shared filesystem.
- Backend: Daphne serves Django on port 8080. WhiteNoise serves the static files
    collected during the image build, including admin, GIS, DRF and custom CSS.
    Login, Frontier callbacks, API documentation, Celery and EDDN remain backend
    responsibilities. `/healthz/` is a liveness check, not a database readiness check.
- Media uploads are currently unused. No media or static volumes are mounted.
    Existing Docker volumes are not deleted by this change. Do not remove old media
    data before checking and backing it up.

### Images and Configuration

Configure the existing backend environment variables and these deployment values
in the root `.env` or the deployment environment. Replace the commit placeholders
with the full commits published by the corresponding pipelines:

```dotenv
BACKEND_IMAGE=ghcr.io/fabietto01/eddai-elitedangerousapiinterface:sha-<backend-commit>
FRONTEND_IMAGE=ghcr.io/fabietto01/eddai-elitedangerousapiinterface-frontend:sha-<frontend-commit>
APP_HOST=eddai.italiangamingsystem.it
DJANGO_SETTINGS_MODULE=eddai_EliteDangerousApiInterface.settings.prod
```

Image digests can be used instead of tags. There is deliberately no `latest`
fallback. The two commits may differ if their API contracts remain compatible.
Traefik must already be connected to the external `proxy_net` network, with an
`https` entrypoint and the existing certificate resolver named `claudflare`.
PostGIS, RabbitMQ, Redis, SMTP and Loki remain external dependencies.

### Release and Rollback

Back up the database before applying schema changes. From the repository root:

```sh
docker compose pull
docker compose --profile release run --rm --no-deps migrate
docker compose up -d --remove-orphans
```

On the first deployment, `--remove-orphans` removes the old `nginx` service, which
must not keep its competing Traefik router. Do not add `--volumes`.
Migrations run once explicitly, not once per replica. They must remain compatible
with any old backend replicas still running during a rolling release.

Scale independently with `docker compose up -d --scale frontend=2 --scale django=2`.
Keep a single Celery Beat scheduler. Roll back by restoring the previous image
references and recreating the affected services; this does not undo migrations.

For local builds, set `BACKEND_IMAGE=eddai-backend:local` and
`FRONTEND_IMAGE=eddai-frontend:local`, run `docker compose build django frontend`,
then use `docker compose up -d --pull never` with the required external services.

### Automated Builds

The backend and frontend workflows publish separate GHCR images on relevant
`main` changes, releases or a manually selected Git tag. Each image gets a
`sha-<full-commit>` tag; releases also get a version tag. Frontend-only changes
do not rebuild the backend. Both workflows produce provenance and SBOM metadata
and upload image vulnerability reports. The frontend pipeline also checks SPA
fallback and real 404 responses in its Nginx container.

These workflows publish artifacts; they do not have credentials or automation
to deploy to the production server. The Compose commands above are the explicit
deployment procedure.

## Development Guide

### Setting Up the Development Environment (Recommended: Dev Containers)

The easiest and recommended way to set up the development environment is using Dev Containers. This approach automatically configures all necessary dependencies (RabbitMQ, Redis, PostGIS) in an isolated container environment.

#### 1. Prerequisites

Before starting, ensure you have the following installed:
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)

#### 2. Clone the Repository

```sh
git clone https://github.com/yourusername/EDDAI-EliteDangerousApiInterface.git
cd EDDAI-EliteDangerousApiInterface
```

#### 3. Setup Dev Container

##### 3.1 Install the Dev Containers Extension

1. **Open Visual Studio Code**
2. **Install the Dev Containers extension**:
    - Go to the Extensions view in Visual Studio Code (`Ctrl+Shift+X`)
    - Search for `Dev Containers` (by Microsoft)
    - Click Install

##### 3.2 Open Project in Dev Container

1. **Open the project folder** in Visual Studio Code:
    ```sh
    code .
    ```

2. **Start the Dev Container**:
    - Open the Command Palette (`Ctrl+Shift+P`)
    - Type and select `Dev Containers: Reopen in Container`
    - Wait for the container to build and initialize (this may take a few minutes on first run)

The Dev Container will automatically:
- Set up a PostgreSQL database with PostGIS extension
- Configure RabbitMQ for Celery task queue
- Set up Redis for caching and Celery backend
- Install all Python dependencies from `environment.yml`
- Configure the development environment

#### 4. Alternative Setup (Without Dev Containers - Not Recommended)

If you prefer to develop without using containers, you can set up your environment manually. This method is not recommended due to the complexity of managing dependencies and configurations.

##### 4.1 Install Backend Dependencies

Install the backend dependencies using Docker with a docker-compose file. Create a `docker-compose.yml` file in your project root:

```yaml
services:
    rabbitmq:
        image: rabbitmq:3.11.13-management
        ports:
            - "5672:5672"
            - "15672:15672"
        environment:
            TZ: UTC
            RABBITMQ_DEFAULT_USER: user
            RABBITMQ_DEFAULT_PASS: password
    redis_result_backend:
        image: redis:6.2.12
        ports:
            - "6379:6379"
        environment:
            TZ: UTC
    redis_cache:
        image: redis:6.2.12
        ports:
            - "6379:6379"
        environment:
            TZ: UTC
    db:
        image: "postgis/postgis:16-3.4"
        environment:
            TZ: UTC
            POSTGRES_DB: eddai
            POSTGRES_USER: user
            POSTGRES_PASSWORD: password
        ports:
            - "5432:5432"
```

##### 4.2 Install Python Environment

1. **Install Miniconda**:
    - Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html)

2. **Create and Configure the Conda Environment**:
    ```sh
    conda env create -f eddai_EliteDangerousApiInterface/environment.yml
    conda activate eddai
    ```

#### 5. Configure Environment Variables

Before running the application, you need to set up the environment variables. This can be done by copying the `.env.template` file and creating a new `.env` file where you will set your environment-specific variables.

1. **Copy the `.env.template` file**:
    ```sh
    cp .env.template .env
    ```

2. **Edit the `.env` file**:
    Open the `.env` file in your preferred text editor and set the necessary environment variables according to your development setup.

#### 6. Database Initialization

After setting up the environment, you need to initialize the database. This involves cleaning the database, applying migrations, and importing initial data from fixtures. You can do this using Django's management commands.

1. **Clean the Database**:
    ```sh
    python manage.py flush --no-input
    ```

2. **Apply Migrations**:
    ```sh
    python manage.py migrate
    ```

3. **Import Initial Data**:
    ```sh
    python manage.py loaddata user economy system body bgs exploration material mining station
    ```

4. **Creating a Django superuser**:
    ```sh
    python manage.py createsuperuser --username admin
    ```

These commands will ensure that your database is properly set up and ready for development.

#### 7. Start the Server

You can start the server using Visual Studio Code's debugging feature or through the terminal. Visual Studio Code is already configured for this project, so it is the recommended choice.

##### 7.1 Using Visual Studio Code Debugging (Recommended)

1. **Open the Debug View**:
    - Click on the Debug icon in the Activity Bar on the side of Visual Studio Code.
    - Alternatively, you can use the shortcut `Ctrl+Shift+D`.

2. **Start Debugging**:
    - Click the green play button at the top of the Debug panel.
    - Select the debug configuration named `Django/Celery Workers`.
    - This will start the Django development server along with the three Celery workers and the Celery beat scheduler with the debugger attached.

##### 7.2 Using the Terminal

If you prefer to start the server through the terminal, you can do so with the following command:

```sh
python manage.py runserver
```

To start the three Celery workers and the Celery beat scheduler, use the following commands in separate terminal windows:

1. Start the first Celery worker:
    ```sh
    python celery -A eddai_EliteDangerousApiInterface worker -l Debug -P gevent --autoscale 50,5 -Q default -n WorkerTasck@%h
    ```

2. Start the second Celery worker:
    ```sh
    python celery -A eddai_EliteDangerousApiInterface worker -l Debug -P gevent --autoscale 50,5 -Q admin -n WorkerAdmin@%h
    ```

3. Start the third Celery worker:
    ```sh
    python celery -A eddai_EliteDangerousApiInterface worker -l Debug -P gevent --autoscale 50,5 -Q eddn -n WorkerEddn@%h
    ```

4. Start the Celery beat scheduler:
    ```sh
    python celery -A eddai_EliteDangerousApiInterface beat -l Debug --scheduler django_celery_beat.schedulers:DatabaseSchedule
    ```

This starts the Django backend at `http://127.0.0.1:8000/`; it no longer renders
the Vue application. Start Vite separately as described in the
[frontend guide](eddai_EliteDangerousApiInterface/ed_frontend/README.md).

Using Visual Studio Code's debugging feature is recommended as it provides a more integrated development experience.

## Disclaimer

EDDAI is not managed or affiliated with the game developer - Frontier Developments.