# EDDAI-EliteDangerousApiInterface
A web API and web application for searching information for the game Elite Dangerous

## Project Description

This is an open-source project written in Python, Django, Django REST Framework, and Celery, while the web interface will be developed in Vue.js. Currently, the project is still in development and features an alpha version with the API available on the main branch at the URL [eddai.italiangamingsystem.it](http://eddai.italiangamingsystem.it).

## How It Works

1. **Data Collection**: EDDAI collects data from [EDDN](https://github.com/EDCD/EDDN), processes and saves the information in the database. It is also possible to send data through the available APIs.
2. **Data Access**: Users can access the data through API endpoints, which provide structured and easy-to-use information. Additionally, it will be possible to access the data through a web application.

## Development Guide

### Setting Up the Development Environment

To set up the development environment, follow these steps:

#### 1. Install Dependencies

For development, some dependencies are required: RabbitMQ, Redis, and PostGIS. Specifically, RabbitMQ is used as a broker for Celery, Redis as the backend for Celery and Django cache, and finally, PostGIS is a spatial database based on PostgreSQL.

It is recommended to host everything on Docker for development, for better management.

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

#### 2. Clone the Repository

```sh
git clone https://github.com/yourusername/EDDAI-EliteDangerousApiInterface.git
cd EDDAI-EliteDangerousApiInterface
```

#### 3. Initialize the Environment

##### 3.1 Development with Visual Studio Code Dev Containers (Recommended)

To streamline the development process, you can use Visual Studio Code Dev Containers. This allows you to develop inside a containerized environment with all dependencies pre-configured.

1. **Install the Remote - Containers extension**:
    - Go to the Extensions view in Visual Studio Code (`Ctrl+Shift+X`).
    - Search for `Remote - Containers` and install it.

2. **Open the project in a Dev Container**:
    - Open the Command Palette (`Ctrl+Shift+P`).
    - Select `Remote-Containers: Open Folder in Container...`.
    - Choose the project folder.

##### 3.2 Development Without Containers (Not Recommended)

If you prefer to develop without using containers, you can set up your environment manually. This method is not recommended due to the complexity of managing dependencies and configurations.

1. **Install Miniconda**:
    - Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html) for your operating system.
    - Follow the installation instructions provided on the website.

2. **Create and Configure the Conda Environment**:
    ```sh
    conda env create -f eddai_EliteDangerousApiInterface/environment.yml
    conda activate eddai
    ```

#### 4. Configure Environment Variables

Before running the application, you need to set up the environment variables. This can be done by copying the `.env.template` file and creating a new `.env` file where you will set your environment-specific variables.

1. **Copy the `.env.template` file**:
    ```sh
    cp .env.template .env
    ```

2. **Edit the `.env` file**:
    Open the `.env` file in your preferred text editor and set the necessary environment variables according to your development setup.

#### 5. Database Initialization

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

These commands will ensure that your database is properly set up and ready for development.

#### 6. Start the Server

You can start the server using Visual Studio Code's debugging feature or through the terminal. Visual Studio Code is already configured for this project, so it is the recommended choice.

##### 6.1 Using Visual Studio Code Debugging (Recommended)

1. **Open the Debug View**:
    - Click on the Debug icon in the Activity Bar on the side of Visual Studio Code.
    - Alternatively, you can use the shortcut `Ctrl+Shift+D`.

2. **Start Debugging**:
    - Click the green play button at the top of the Debug panel.
    - Select the debug configuration named `Django/Celery Workers`.
    - This will start the Django development server along with the three Celery workers and the Celery beat scheduler with the debugger attached.

##### 6.2 Using the Terminal

If you prefer to start the server through the terminal, you can do so with the following command:

```sh
python manage.py runserver
```

To start the three Celery workers and the Celery beat scheduler, use the following commands in separate terminal windows:

1. Start the first Celery worker:
    ```sh
    celery -A eddai worker --loglevel=info -n worker1@%h
    ```

2. Start the second Celery worker:
    ```sh
    celery -A eddai worker --loglevel=info -n worker2@%h
    ```

3. Start the third Celery worker:
    ```sh
    celery -A eddai worker --loglevel=info -n worker3@%h
    ```

4. Start the Celery beat scheduler:
    ```sh
    celery -A eddai beat --loglevel=info
    ```

This will start the Django development server, and you can access the application at `http://127.0.0.1:8000/`.

Using Visual Studio Code's debugging feature is recommended as it provides a more integrated development experience.

## Disclaimer

EDDAI is not managed or affiliated with the game developer - Frontier Developments.