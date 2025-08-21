"""
Example ANAL Framework Application

This example demonstrates how to build a complete REST API
using the ANAL framework with authentication, database models,
and API endpoints.
"""

# main.py - Application entry point
from anal.core import ANAL
from anal.auth import AuthenticationMiddleware
from anal.http import JsonResponse
from anal.db import connect_database, disconnect_database

# Create ANAL application
app = ANAL(__name__)

# Add authentication middleware
app.add_middleware(AuthenticationMiddleware)

# Database connection events
@app.on_startup
async def startup():
    await connect_database()
    print("🚀 ANAL Framework Application Started")

@app.on_shutdown
async def shutdown():
    await disconnect_database()
    print("👋 ANAL Framework Application Stopped")


# models.py - Database models
from anal.db import Model, fields

class User(Model):
    """User model for the application."""
    id = fields.AutoField()
    username = fields.CharField(max_length=50, unique=True)
    email = fields.EmailField(unique=True)
    first_name = fields.CharField(max_length=30, blank=True)
    last_name = fields.CharField(max_length=30, blank=True)
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)
    
    class Meta:
        table_name = "app_users"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.username


class Post(Model):
    """Blog post model."""
    id = fields.AutoField()
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author = fields.ForeignKey(User, on_delete='CASCADE')
    published = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)
    
    class Meta:
        table_name = "app_posts"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title


# controllers.py - API Controllers
from anal.http import APIController, JsonResponse
from anal.auth import login_required, permission_required

class UserController(APIController):
    """User management API."""
    
    async def list_users(self, request):
        """Get all users."""
        users = await User.objects.all()
        return JsonResponse([{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': f"{user.first_name} {user.last_name}",
            'created_at': user.created_at.isoformat()
        } for user in users])
    
    async def get_user(self, request):
        """Get specific user."""
        user_id = request.path_params['id']
        try:
            user = await User.objects.get(id=user_id)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'created_at': user.created_at.isoformat()
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    @login_required
    async def create_user(self, request):
        """Create new user."""
        data = await request.json()
        
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            await user.asave()
            
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'User created successfully'
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class PostController(APIController):
    """Blog post management API."""
    
    async def list_posts(self, request):
        """Get all posts."""
        posts = await Post.objects.filter(published=True).all()
        return JsonResponse([{
            'id': post.id,
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'author_id': post.author,
            'published': post.published,
            'created_at': post.created_at.isoformat()
        } for post in posts])
    
    @login_required
    async def create_post(self, request):
        """Create new post."""
        data = await request.json()
        user = request.state.user
        
        try:
            post = Post(
                title=data['title'],
                content=data['content'],
                author=user.id,
                published=data.get('published', False)
            )
            await post.asave()
            
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'message': 'Post created successfully'
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# routes.py - URL routing
from anal.http import Router

# Create router
router = Router()

# User routes
router.add_route('GET', '/api/users', UserController().list_users)
router.add_route('GET', '/api/users/{id}', UserController().get_user)
router.add_route('POST', '/api/users', UserController().create_user)

# Post routes
router.add_route('GET', '/api/posts', PostController().list_posts)
router.add_route('POST', '/api/posts', PostController().create_post)

# Authentication routes
from anal.auth import authenticate, login

async def login_view(request):
    """User login endpoint."""
    data = await request.json()
    
    user = await authenticate(
        username=data.get('username'),
        password=data.get('password')
    )
    
    if user:
        session_info = await login(user, request)
        return JsonResponse({
            'message': 'Login successful',
            'session_key': session_info['session_key'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

router.add_route('POST', '/api/auth/login', login_view)

# Register routes with app
app.include_router(router)


# settings.py - Application configuration
from anal.core.config import Settings

class AppSettings(Settings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Debug
    DEBUG: bool = True
    
    # CORS
    ALLOWED_HOSTS: list = ["*"]
    
    class Config:
        env_file = ".env"


# migrations/20240101_120000_initial.py - Database migration
from anal.db.migrations import Migration, CreateTable

class InitialMigration(Migration):
    """Initial database migration."""
    
    dependencies = []
    
    operations = [
        CreateTable('app_users', {
            'id': {'type': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'primary_key': True},
            'username': {'type': 'VARCHAR(50)', 'null': False, 'unique': True},
            'email': {'type': 'VARCHAR(254)', 'null': False, 'unique': True},
            'first_name': {'type': 'VARCHAR(30)', 'default': ''},
            'last_name': {'type': 'VARCHAR(30)', 'default': ''},
            'created_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'},
            'updated_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'},
        }),
        
        CreateTable('app_posts', {
            'id': {'type': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'primary_key': True},
            'title': {'type': 'VARCHAR(200)', 'null': False},
            'content': {'type': 'TEXT', 'null': False},
            'author_id': {'type': 'INTEGER', 'null': False},
            'published': {'type': 'BOOLEAN', 'default': False},
            'created_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'},
            'updated_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'},
        }),
    ]


# Running the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


"""
Usage Examples:

1. Setup:
   ```bash
   pip install ANAL
   anal-admin startproject blog_api
   cd blog_api
   ```

2. Create migrations:
   ```bash
   anal-admin makemigrations auth
   anal-admin makemigrations
   anal-admin migrate
   ```

3. Create superuser:
   ```bash
   anal-admin createsuperuser
   ```

4. Run development server:
   ```bash
   anal-admin runserver
   ```

5. Test API endpoints:
   ```bash
   # Get users
   curl http://127.0.0.1:8000/api/users
   
   # Login
   curl -X POST http://127.0.0.1:8000/api/auth/login \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "password"}'
   
   # Create post (authenticated)
   curl -X POST http://127.0.0.1:8000/api/posts \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer <session_key>" \
        -d '{"title": "My Post", "content": "Post content"}'
   
   # Get posts
   curl http://127.0.0.1:8000/api/posts
   ```

This example demonstrates:
- Model definition with relationships
- API controllers with authentication
- URL routing and middleware
- Database migrations
- Configuration management
- Request/response handling
- Error handling
- Authentication flow

The ANAL framework provides a complete, Django-like experience
with modern async support and FastAPI-style performance.
"""
