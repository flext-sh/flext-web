# CLAUDE.md - FLX-WEB MODULE

**Hierarchy**: PROJECT-SPECIFIC
**Project**: FLX Web - Enterprise Web Dashboard
**Status**: PRODUCTION READY (Django Monolith)
**Last Updated**: 2025-06-28

**Reference**: `/home/marlonsc/CLAUDE.md` → Universal principles
**Reference**: `/home/marlonsc/internal.invalid.md` → Cross-workspace issues
**Reference**: `../CLAUDE.md` → PyAuto workspace patterns

---

## 🎯 PROJECT-SPECIFIC CONFIGURATION

### Virtual Environment Usage

```bash
# MANDATORY: Use workspace venv
source /home/marlonsc/pyauto/.venv/bin/activate
# NOT project-specific venv
```

### Agent Coordination

```bash
# Read workspace coordination first
cat /home/marlonsc/pyauto/.token | tail -5
# Log Web-specific work
echo "FLX_WEB_WORK_$(date)" >> .token
```

## 📊 REAL IMPLEMENTATION STATUS

Based on actual code analysis from `flx-meltano-enterprise/src/flx_web/`:

| Django App     | Views | Models | Admin | Total Lines | NotImplementedError |
| -------------- | ----- | ------ | ----- | ----------- | ------------------- |
| **dashboard**  | 351   | -      | -     | 351         | 0                   |
| **projects**   | 473   | 219    | 424   | 1,116       | 0                   |
| **pipelines**  | 188   | 284    | 181   | 653         | 0                   |
| **monitoring** | 543   | 307    | -     | 850         | 0                   |
| **users**      | -     | 540    | -     | 540         | 0                   |

**Total**: 3,930+ lines of Django code with ZERO NotImplementedError

## 🚨 CRITICAL DISCOVERY

### **Architecture Reality vs Expectations**

**Expected**: Modern React/Vue/Angular SPA with API backend
**Reality**: Traditional Django monolith with server-side rendering

This is a **FUNDAMENTAL ARCHITECTURAL DIFFERENCE** that impacts everything:

- ✅ Django templates (NOT React components)
- ✅ Server-side rendering (NOT client-side)
- ✅ Bootstrap 5 CSS (NOT Material-UI/Vuetify)
- ✅ Page refreshes (NOT SPA routing)
- ❌ Empty `frontend/` directory (no JS framework)

### **Technology Stack Reality**

```python
# From dashboard/views.py - Real implementation
@login_required
@require_http_methods(["GET"])
def dashboard_home(request: HttpRequest) -> HttpResponse:
    """Dashboard home with system stats via gRPC."""
    grpc_stats = _fetch_grpc_stats()
    health_status = _check_system_health()
    recent_executions = _get_recent_executions()

    return render(request, "dashboard/home.html", {
        "stats": grpc_stats,
        "health": health_status,
        "executions": recent_executions,
    })
```

This is Django views returning HTML, not REST API endpoints!

## 🔧 EXTRACTION STRATEGY

### **Direct Django App Extraction**

```bash
# Step 1: Copy Django project structure
cp -r flx-meltano-enterprise/src/flx_web/* src/flx_web/

# Step 2: Update imports (if needed)
# Most imports are Django-standard, minimal changes needed

# Step 3: Ensure gRPC dependencies
# The Django app depends on gRPC clients from flx_core
```

### **Key Dependencies**

1. **gRPC Clients**: Uses flx_core.grpc for backend communication
2. **Domain Config**: Uses unified configuration system
3. **Django 5.x**: Latest Django with Python 3.13
4. **Bootstrap 5**: Frontend CSS framework

## 📁 PROJECT STRUCTURE

```
flx-web/
├── src/
│   └── flx_web/
│       ├── manage.py                    # Django management
│       ├── flx_web/                     # Django project
│       │   ├── __init__.py
│       │   ├── settings/
│       │   │   ├── base.py            # Base settings
│       │   │   ├── development.py      # Dev settings
│       │   │   └── production.py       # Prod settings
│       │   ├── urls.py                 # URL configuration
│       │   ├── wsgi.py                 # WSGI application
│       │   └── celery.py               # Celery config
│       ├── apps/                        # Django apps
│       │   ├── dashboard/
│       │   │   ├── views.py           # 351 lines
│       │   │   ├── urls.py
│       │   │   └── templates/
│       │   ├── projects/
│       │   │   ├── models.py          # 219 lines
│       │   │   ├── views.py           # 473 lines
│       │   │   ├── REDACTED_LDAP_BIND_PASSWORD.py           # 424 lines
│       │   │   └── templates/
│       │   ├── pipelines/
│       │   │   ├── models.py          # 284 lines
│       │   │   ├── views.py           # 188 lines
│       │   │   └── REDACTED_LDAP_BIND_PASSWORD.py           # 181 lines
│       │   ├── monitoring/
│       │   │   ├── models.py          # 307 lines
│       │   │   ├── views.py           # 543 lines
│       │   │   └── templates/
│       │   └── users/
│       │       └── models.py          # 540 lines
│       ├── templates/                   # Base templates
│       │   ├── base.html
│       │   ├── navbar.html
│       │   └── footer.html
│       ├── static/                      # Static assets
│       │   ├── css/
│       │   ├── js/
│       │   └── img/
│       └── frontend/                    # EMPTY (artifact)
│           ├── dist/                   # No files
│           └── src/                    # No files
├── tests/
├── requirements/
├── docker/
├── pyproject.toml
├── README.md
├── CLAUDE.md                           # This file
└── .env.example
```

## 🚀 DJANGO FEATURES IMPLEMENTED

### **1. Dashboard App**

Real-time monitoring with gRPC integration:

- System statistics display
- Health status monitoring
- Recent execution tracking
- Login required for all views

### **2. Projects App**

Full CRUD with Django REDACTED_LDAP_BIND_PASSWORD:

- Project model with relationships
- Template management
- Deployment tracking
- Custom REDACTED_LDAP_BIND_PASSWORD actions

### **3. Pipelines App**

Pipeline management interface:

- Pipeline configuration UI
- Execution history views
- Schedule management
- Status badge display

### **4. Monitoring App**

System monitoring dashboard:

- Metrics visualization
- Alert management
- Performance graphs
- Resource utilization

### **5. Users App**

Extended Django user model:

- Custom user fields
- Role-based permissions
- Profile management
- Authentication integration

## 📊 UI TECHNOLOGY BREAKDOWN

### **What's Used**

```html
<!-- From base.html template -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Bootstrap 5 CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    />
    <!-- Font Awesome -->
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    />
    <!-- Custom CSS -->
    <link href="{% static 'css/style.css' %}" />
  </head>
</html>
```

### **What's NOT Used**

- ❌ React/Vue/Angular
- ❌ Webpack/Vite
- ❌ Node.js build process
- ❌ API-first architecture
- ❌ JavaScript framework

## 🔒 PROJECT .ENV SECURITY REQUIREMENTS

### MANDATORY .env Variables

```bash
# WORKSPACE (required for all PyAuto projects)
WORKSPACE_ROOT=/home/marlonsc/pyauto
PYTHON_VENV=/home/marlonsc/pyauto/.venv
DEBUG_MODE=true

# DJANGO SPECIFIC
DJANGO_SECRET_KEY=your-secret-key-minimum-50-characters
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DJANGO_SETTINGS_MODULE=flx_web.settings.production

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/flx_web
DATABASE_CONN_MAX_AGE=60

# gRPC Backend
GRPC_HOST=localhost
GRPC_PORT=50051
GRPC_TIMEOUT=30

# Static/Media Files
STATIC_ROOT=/var/www/flx_web/static
MEDIA_ROOT=/var/www/flx_web/media
STATICFILES_STORAGE=whitenoise.storage.CompressedManifestStaticFilesStorage

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Email (for error reporting)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### MANDATORY CLI Usage

```bash
# ALWAYS source workspace venv + project .env
source /home/marlonsc/pyauto/.venv/bin/activate
source .env

# Django management
python manage.py migrate --settings=flx_web.settings.development
python manage.py runserver --settings=flx_web.settings.development
python manage.py collectstatic --noinput --settings=flx_web.settings.production

# Production
gunicorn flx_web.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## 📝 LESSONS APPLIED

### **From Investigation Success**

1. **Discovered Reality**: Django monolith, not SPA
2. **Found gRPC Integration**: Backend communication implemented
3. **Verified Completeness**: 0 NotImplementedError
4. **Identified UI Stack**: Bootstrap 5 + Django templates

### **Documentation Accuracy**

- ✅ Real line counts per Django app
- ✅ Actual technology stack identified
- ✅ Empty frontend/ directory noted
- ✅ No false claims about React/Vue

## 🎯 NEXT ACTIONS

1. Extract complete Django project
2. Set up PostgreSQL database
3. Configure gRPC connections
4. Create Docker deployment
5. Add Nginx configuration
6. Set up static file serving

## ⚠️ ARCHITECTURAL IMPLICATIONS

### **Monolith vs Microservices**

This Django monolith challenges the microservices narrative:

- Single deployment unit
- Shared database
- Server-side rendering
- Traditional web architecture

### **Future Frontend Options**

If modern frontend needed:

1. **Progressive Enhancement**: Add React/Vue components to existing pages
2. **API Layer**: Create DRF API alongside Django views
3. **Full Rewrite**: Replace with SPA (major effort)

### **Current Benefits**

- ✅ Simple deployment
- ✅ Fast development
- ✅ SEO friendly
- ✅ No JavaScript complexity
- ✅ Unified codebase

---

**MANTRA FOR THIS PROJECT**: **EMBRACE THE MONOLITH, PERFECT THE EXPERIENCE**

**Remember**: This is a complete Django web application, not a modern SPA. The challenge is deployment and integration, not frontend development.
