# TL Showroom Backend POC

## Project Overview
This is a proof-of-concept (POC) backend for a showroom application, built with FastAPI and PostgreSQL. The application manages profiles with different statuses (ACTIVE, INACTIVE, SUSPENDED, DELETED) and tracks their lifecycle through a history of status changes. It provides a RESTful API for creating, reading, updating, and deleting profiles.

## Technology Stack
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **PostgreSQL**: Robust, open-source relational database
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Docker & Docker Compose**: For containerization and orchestration
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the FastAPI application
- **Alembic**: Database migration tool

## Project Structure
- **main.py**: Entry point that imports the application from the app package
- **app/**: Main application package
  - **main.py**: Configures FastAPI and middleware
  - **api/**: API-related modules
    - **routes.py**: API route definitions for profile management
    - **profile_api.py**: API interface for profile operations
    - **profile_schemas.py**: Pydantic models for request/response validation
  - **config/**: Configuration modules
    - **database.py**: Database connection setup
    - **dependencies.py**: FastAPI dependency injection setup
  - **db/**: Database access layer
    - **profile_repository.py**: Repository for profile data access
  - **services/**: Business logic layer
    - **profile_service.py**: Service implementing profile business logic
  - **entities.py**: Domain entities (Profile, ProfileHistory, ProfileStatus)
- **tests/**: Test suite
  - **unit/**: Unit tests
    - **test_models.py**: Tests for domain models
    - **test_crud.py**: Tests for database operations
  - **integration/**: Integration tests
    - **test_routes.py**: Tests for API routes
- **Dockerfile**: Instructions for building the Docker image
- **docker-compose.yml**: Service definitions for the application and database
- **docker-compose.test.yml**: Service definitions for running tests
- **entrypoint.sh**: Script for starting the application with HTTPS
- **deploy.sh**: Script for deploying the application to production
- **.env.example**: Example environment variables
- **.env.test**: Environment variables for testing
- **run_tests.sh**: Script for running tests
- **test-coverage.sh**: Script for generating test coverage reports
- **test-docker.sh**: Script for running tests in Docker
- **format.sh**: Script for formatting code
- **lint.sh**: Script for linting code
- **clean.sh**: Script for cleaning up temporary files

## Architecture
This project follows a layered architecture pattern:

- **API Layer** (app/api): Handles HTTP requests and responses, input validation, and routing
  - Routes define the API endpoints and delegate to the service layer
  - Schemas define the data structures for request/response validation

- **Service Layer** (app/services): Contains the business logic
  - ProfileService implements the core business rules for profile management
  - Services are independent of the HTTP layer and database implementation

- **Data Access Layer** (app/db): Manages data persistence
  - Repositories abstract the database operations
  - Provides a clean interface for the service layer to interact with the database

- **Domain Model** (app/entities.py): Defines the core business entities
  - Profile, ProfileHistory, and ProfileStatus represent the domain concepts
  - Contains business rules specific to the entities

- **Configuration** (app/config): Manages application configuration and dependencies
  - Database connection setup
  - Dependency injection for FastAPI

This architecture provides several benefits:
- **Separation of Concerns**: Each layer has a specific responsibility
- **Testability**: Components can be tested in isolation
- **Maintainability**: Changes in one layer have minimal impact on other layers
- **Scalability**: Layers can be scaled independently as needed

## Features
- **Profile Management**: Create, read, update, and delete profiles
- **Status Tracking**: Track profile status changes (ACTIVE, INACTIVE, SUSPENDED, DELETED)
- **History Logging**: Maintain a history of status changes for each profile

## API Endpoints
- **POST /profiles/**: Create a new profile
- **GET /profiles/{profile_id}**: Get a profile by ID
- **GET /profiles/**: Get all profiles (with pagination)
- **PUT /profiles/{profile_id}**: Update a profile
- **DELETE /profiles/{profile_id}**: Delete a profile

## Database Schema
- **profiles**: Stores profile information (name, email, specialty, linkedin, status, dates)
- **profile_history**: Tracks status changes for profiles

## Deployment
The application is designed to be deployed using Docker Compose. The deployment process is automated with the deploy.sh script, which:
1. Pulls the latest code from Git
2. Builds the Docker image
3. Restarts the services
4. Connects the API container to the web server network

## Development Setup
1. Clone the repository
2. Create a .env file with the required environment variables:
   - DATABASE_URL
   - DB_USER
   - DB_PASS
   - DB_NAME
3. Run `docker-compose up` to start the application and database

## Testing Setup
The project includes a comprehensive testing setup with unit tests and integration tests.

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setting Up the Testing Environment
1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure the testing environment (optional):
   - Copy `.env.test` to create your own test configuration
   - By default, tests use SQLite for simplicity
   - You can configure PostgreSQL for testing by uncommenting and setting the appropriate variables in `.env.test`

3. Run the tests:
   ```
   pytest
   ```

   Alternatively, you can use the provided script:
   ```
   ./run_tests.sh
   ```

   To install dependencies and run tests in one command:
   ```
   ./run_tests.sh --install
   ```

### Test Structure
- **Unit Tests**: Tests for individual components (models, CRUD operations)
  - `tests/unit/test_models.py`: Tests for SQLAlchemy models
  - `tests/unit/test_crud.py`: Tests for database operations through the hexagonal architecture

- **Integration Tests**: Tests for API endpoints
  - `tests/integration/test_routes.py`: Tests for API routes

### Running Specific Tests
- Run all tests:
  ```
  pytest
  ```

- Run unit tests only:
  ```
  pytest tests/unit/
  ```

- Run integration tests only:
  ```
  pytest tests/integration/
  ```

- Run tests with coverage report:
  ```
  pytest --cov=. --cov-report=html
  ```
  This will generate an HTML coverage report in the `htmlcov` directory.

### Running Tests with Docker
You can also run tests in a containerized environment using Docker Compose:

```
docker-compose -f docker-compose.test.yml up
```

This will:
1. Build the Docker image
2. Install all dependencies
3. Run all tests with coverage reporting
4. Display the test results in the terminal

This approach ensures that tests run in an environment similar to production and is especially useful for CI/CD pipelines.

### Continuous Integration
This project uses GitHub Actions for continuous integration. The workflow automatically runs tests on push to the main branch and on pull requests.

The workflow:
1. Sets up Python
2. Installs dependencies
3. Runs tests with coverage reporting
4. Uploads coverage reports to Codecov

You can see the workflow configuration in `.github/workflows/test.yml`.

### Using the Shell Scripts
This project includes shell scripts to simplify common development tasks:

```
# Install dependencies
./install.sh

# Run tests
./run_tests.sh

# Run tests with coverage report
./test-coverage.sh

# Run linting
./lint.sh

# Format code
./format.sh

# Run tests in Docker
./test-docker.sh

# Clean up temporary files
./clean.sh
```

These shell scripts provide a convenient way to run common tasks and make it easier to integrate with CI/CD systems.

## Production Deployment
For production deployment, the application uses HTTPS with Let's Encrypt certificates. The entrypoint.sh script configures Uvicorn to use SSL certificates for secure communication.
