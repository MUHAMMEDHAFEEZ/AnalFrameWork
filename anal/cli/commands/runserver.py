"""
Command to run the development server.
"""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    import uvicorn
except ImportError:
    uvicorn = None

from anal.core.config import Settings


def run_development_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = False,
    workers: int = 1,
    settings: Optional[Settings] = None
) -> None:
    """
    Run the development server.
    
    Args:
        host: Host address to bind to
        port: Port number
        reload: Enable auto-reload
        workers: Number of worker processes
        settings: Application settings
    """
    if uvicorn is None:
        print("Error: uvicorn is required to run the server.")
        print("Install it with: pip install uvicorn[standard]")
        sys.exit(1)
    
    # Find the ASGI application
    app_module = find_asgi_application()
    if not app_module:
        print("Error: Could not find ASGI application.")
        print("Make sure you have a main.py or asgi.py file with an 'app' or 'application' variable.")
        sys.exit(1)
    
    print(f"Starting development server at http://{host}:{port}")
    print("Quit the server with CONTROL-C.")
    
    if reload:
        print("Auto-reload is enabled. The server will restart when code changes.")
    
    # Configure uvicorn
    config = {
        "app": app_module,
        "host": host,
        "port": port,
        "reload": reload,
        "workers": workers if not reload else 1,  # Workers > 1 incompatible with reload
        "log_level": "debug" if settings and settings.DEBUG else "info",
        "access_log": True,
    }
    
    # Add SSL if configured
    if settings:
        if hasattr(settings, 'SSL_KEYFILE') and hasattr(settings, 'SSL_CERTFILE'):
            if settings.SSL_KEYFILE and settings.SSL_CERTFILE:
                config.update({
                    "ssl_keyfile": settings.SSL_KEYFILE,
                    "ssl_certfile": settings.SSL_CERTFILE,
                })
    
    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\\nServer stopped.")


def find_asgi_application() -> Optional[str]:
    """
    Find the ASGI application in the current project.
    
    Returns:
        Module path to the ASGI app or None if not found
    """
    # Common locations to look for ASGI app
    candidates = [
        # Direct files
        "main:app",
        "asgi:application", 
        "app:app",
        "application:app",
        
        # In project subdirectories
        "*/main:app",
        "*/asgi:application",
        "*/app:app",
    ]
    
    # Get project name from current directory
    project_name = Path.cwd().name
    
    # Add project-specific candidates
    candidates.extend([
        f"{project_name}.main:app",
        f"{project_name}.asgi:application",
        f"{project_name}/main:app",
        f"{project_name}/asgi:application",
    ])
    
    for candidate in candidates:
        if check_asgi_module(candidate):
            return candidate
    
    return None


def check_asgi_module(module_path: str) -> bool:
    """
    Check if a module path contains a valid ASGI application.
    
    Args:
        module_path: Module path in format "module:attribute"
        
    Returns:
        True if valid ASGI app found
    """
    try:
        if ":" not in module_path:
            return False
        
        module_name, app_name = module_path.split(":", 1)
        
        # Handle wildcard patterns
        if "*" in module_name:
            import glob
            pattern = module_name.replace("*", "*/")
            paths = glob.glob(pattern)
            for path in paths:
                # Convert path to module name
                mod_name = path.replace("/", ".").replace("\\\\", ".").rstrip(".py")
                test_path = f"{mod_name}:{app_name}"
                if check_asgi_module_direct(test_path):
                    return True
            return False
        else:
            return check_asgi_module_direct(module_path)
    
    except Exception:
        return False


def check_asgi_module_direct(module_path: str) -> bool:
    """Check if a specific module path has a valid ASGI app."""
    try:
        module_name, app_name = module_path.split(":", 1)
        
        # Try to import the module
        import importlib
        module = importlib.import_module(module_name)
        
        # Check if the attribute exists
        if not hasattr(module, app_name):
            return False
        
        app = getattr(module, app_name)
        
        # Basic check if it's callable (ASGI apps are callable)
        return callable(app)
    
    except Exception:
        return False


def get_reload_dirs() -> list:
    """Get directories to watch for auto-reload."""
    reload_dirs = [str(Path.cwd())]
    
    # Add common Python package directories
    for item in Path.cwd().iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name == '__pycache__':
            # Check if it's a Python package
            if (item / '__init__.py').exists():
                reload_dirs.append(str(item))
    
    return reload_dirs
