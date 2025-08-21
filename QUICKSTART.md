# Quick Start Guide for ANAL Framework

## Installation

```bash
pip install anal-framework
```

## Create Your First Project

```bash
# Create new project
anal-admin startproject myapp
cd myapp

# Setup database (SQLite by default)
anal-admin makemigrations auth
anal-admin migrate

# Create admin user
anal-admin createsuperuser

# Run development server
anal-admin runserver
```

Your app will be available at `http://localhost:8000`

## Features

✅ **SQLite Default Database** - Ready to use out of the box  
✅ **Rich CLI Tools** - Complete project management  
✅ **Modern Async Framework** - Built on Starlette/ASGI  
✅ **Type Safety** - Full type hints with Pydantic  
✅ **Authentication System** - Built-in user management  
✅ **Database Migrations** - Powered by Alembic  
✅ **Multi-Database Support** - PostgreSQL, MySQL, MongoDB  

## Quick Example

```python
# controllers.py
from anal.http import Controller, JSONResponse
from anal.http.decorators import route

class UserController(Controller):
    
    @route("/users", methods=["GET"])
    async def list_users(self, request):
        return JSONResponse({"users": []})
```

## Documentation

- [Full Documentation](https://docs.analframework.org)
- [Tutorial](https://docs.analframework.org/tutorial/)
- [GitHub Repository](https://github.com/analframework/anal)

## Support

- GitHub Issues: https://github.com/analframework/anal/issues
- Documentation: https://docs.analframework.org
