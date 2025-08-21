# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-28

### Added
- Initial release of ANAL Framework
- Core application framework with ASGI support
- HTTP layer with routing, controllers, and responses
- Database layer with SQLAlchemy 2.0+ and migrations
- Authentication system with models, backends, and middleware
- Complete CLI system with project management commands
- SQLite default database configuration for easy setup
- Rich developer experience with type hints and validation
- Comprehensive middleware system
- Event system and dependency injection
- Project scaffolding and management tools

### Features
- **Framework Core**: Application class, configuration management, and registry
- **HTTP Layer**: Controllers, routing, middleware, and response handling
- **Database**: ORM with SQLAlchemy, migrations with Alembic, multi-database support
- **Authentication**: User models, authentication backends, and security middleware
- **CLI Tools**: 
  - `anal-admin startproject` - Create new projects
  - `anal-admin runserver` - Development server
  - `anal-admin makemigrations` - Create database migrations
  - `anal-admin migrate` - Apply migrations
  - `anal-admin createsuperuser` - Create admin users
  - `anal-admin shell` - Interactive Python shell
  - `anal-admin version` - Version information
- **Default Configuration**: SQLite database for instant development setup

### Technical Details
- Python 3.12+ support
- Async-first design with Starlette/ASGI
- Full type hints and Pydantic validation
- Comprehensive middleware system
- Dependency injection container
- Event-driven architecture
- Rich CLI with colored output and progress bars

### Dependencies
- uvicorn[standard] - ASGI server
- starlette - Web framework base
- pydantic - Data validation
- SQLAlchemy[asyncio] - ORM
- alembic - Database migrations
- typer - CLI framework
- rich - Terminal formatting
- And many more for full functionality

[0.1.0]: https://github.com/analframework/anal/releases/tag/v0.1.0
