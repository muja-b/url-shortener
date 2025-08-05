# URL Shortener - Domain-Driven Design (DDD) Architecture

This project has been refactored to follow Domain-Driven Design principles, providing a clean separation of concerns and maintainable codebase.

## Architecture Overview

```
URLshortener/
├── domains/                          # Domain Layer (Business Logic)
│   └── url_shortening/
│       ├── entities/                 # Business Entities
│       │   └── shortened_url.py     # ShortenedUrl entity
│       ├── value_objects/           # Value Objects
│       │   ├── original_url.py      # URL validation
│       │   └── short_code.py        # Short code validation
│       ├── services/                # Domain Services
│       │   ├── hash_service.py      # Hash generation logic
│       │   └── url_shortening_service.py  # Core business logic
│       └── repositories/            # Repository Interfaces
│           └── url_repository.py    # Data access interface
├── application/                      # Application Layer (Use Cases)
│   └── use_cases/
│       ├── shorten_url_use_case.py  # URL shortening use case
│       ├── get_url_use_case.py      # URL retrieval use case
│       └── delete_url_use_case.py   # URL deletion use case
├── infrastructure/                   # Infrastructure Layer (External Concerns)
│   ├── database/
│   │   └── postgres_repository.py   # PostgreSQL implementation
│   ├── web/
│   │   ├── flask_app.py            # Flask configuration
│   │   └── routes.py               # HTTP routes
│   └── utils/
│       └── container.py            # Dependency injection
├── app_ddd.py                       # New DDD-based application entry point
└── app.py                          # Original application (for comparison)
```

## Key Benefits

### 1. **Separation of Concerns**
- **Domain Layer**: Contains all business logic and rules
- **Application Layer**: Orchestrates use cases
- **Infrastructure Layer**: Handles external concerns (database, web)

### 2. **Testability**
- Each layer can be tested independently
- Domain logic is isolated from infrastructure
- Easy to mock dependencies

### 3. **Maintainability**
- Clear boundaries between layers
- Business rules are centralized
- Easy to extend and modify

### 4. **Scalability**
- Easy to add new features
- Can swap infrastructure (e.g., different database)
- Clear dependency flow

## Running the Application

### Using DDD Architecture (Recommended)
```bash
python app_ddd.py
```

### Using Original Architecture
```bash
python app.py
```

## Key Components

### Domain Layer
- **Entities**: `ShortenedUrl` - Core business entity
- **Value Objects**: `OriginalUrl`, `ShortCode` - Immutable values with validation
- **Services**: Business logic for URL shortening and hash generation
- **Repositories**: Data access interfaces

### Application Layer
- **Use Cases**: Application-specific operations
- **Orchestration**: Coordinates domain services

### Infrastructure Layer
- **Database**: PostgreSQL implementation of repository
- **Web**: Flask routes and configuration
- **Utils**: Dependency injection container

## Migration Guide

The original `app.py` has been preserved for comparison. The new DDD structure:

1. **Extracts business logic** into domain services
2. **Separates concerns** into different layers
3. **Improves testability** with clear boundaries
4. **Enhances maintainability** with organized code

## Next Steps

1. **Add Tests**: Unit tests for each layer
2. **Add Validation**: More comprehensive input validation
3. **Add Logging**: Structured logging throughout
4. **Add Configuration**: Environment-based configuration
5. **Add Documentation**: API documentation

## Dependencies

The DDD structure requires the same dependencies as the original:
- Flask
- psycopg2
- validators

No additional dependencies are needed for the DDD architecture. 