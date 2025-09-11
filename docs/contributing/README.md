# Contributing Guide - FLEXT Web Interface

**Development Standards**: Clean Architecture • DDD • FLEXT ecosystem patterns  
**Quality Requirements**: 90%+ coverage • Strict typing • Comprehensive linting  
**Process**: Feature branches • Quality gates • PR review • Documentation updates

## 🤝 Welcome Contributors

Thank you for your interest in contributing to **flext-web**, the enterprise web interface for the FLEXT distributed data integration platform. This guide will help you get started with contributing effectively while maintaining our high standards for code quality and architecture.

### Project Values

- **Quality First**: 90%+ test coverage, strict typing, comprehensive linting
- **Clean Architecture**: Clear separation of concerns, SOLID principles
- **FLEXT Integration**: Consistent patterns across the 33-project ecosystem
- **Documentation**: Keep docs current with all changes
- **Security**: Never compromise on security or data protection

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.13+** (required for latest features)
- **Poetry** (dependency management)
- **Git** (version control)
- **Make** (build automation)
- **Understanding of**: Clean Architecture, DDD, CQRS patterns

### First-Time Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/flext-web.git
cd flext-web

# 2. Add upstream remote
git remote add upstream https://github.com/flext-sh/flext-web.git

# 3. Complete project setup
make setup

# 4. Verify environment
make diagnose
make doctor

# 5. Run tests to ensure everything works
make validate
```

### Understanding the Codebase

Before making changes, please review:

- **[Architecture Guide](../architecture/README.md)** - System design and patterns
- **[Development Guide](../development/README.md)** - Development workflows
- **[API Reference](../api/README.md)** - API structure and conventions
- **[TODO.md](../TODO.md)** - Current issues and improvement opportunities

## 📋 Contribution Types

### 🐛 Bug Fixes

**Process**:

1. **Create issue** describing the bug with reproduction steps
2. **Create branch**: `git checkout -b fix/issue-123-bug-description`
3. **Write failing test** that reproduces the bug
4. **Fix implementation** with minimal changes
5. **Verify fix** ensures test passes and no regressions
6. **Update documentation** if behavior changes

**Example Bug Fix**:

```python
# tests/test_bug_fix.py
def test_app_creation_with_invalid_port():
    """Test that invalid port raises appropriate error"""
    handler = FlextWebAppHandler()

    # This should fail gracefully
    result = handler.create("test-app", port=70000)  # Invalid port

    assert not result.success
    assert "Port must be between 1 and 65535" in result.error
```

### ✨ New Features

**Process**:

1. **Discuss in issue** before implementing large features
2. **Create branch**: `git checkout -b feature/amazing-feature`
3. **Follow TDD** - write tests first, then implementation
4. **Maintain architecture** - follow Clean Architecture layers
5. **Update documentation** - API docs, README, architecture docs
6. **Add configuration** if feature requires new settings

**Feature Development Guidelines**:

- **Domain Layer**: Add entities and business rules first
- **Application Layer**: Create handlers and use cases
- **Infrastructure Layer**: Add external integrations
- **Web Layer**: Add routes and API endpoints last

### 🔧 Refactoring

**Current Priority Refactoring** (see [TODO.md](../TODO.md)):

1. **Monolithic Architecture**: Split 518-line `__init__.py` into layers
2. **Dependency Cleanup**: Remove unused Django/FastAPI dependencies
3. **Persistence Layer**: Replace in-memory storage with database
4. **Template System**: Fix Django/Flask template inconsistency

**Refactoring Process**:

1. **Ensure 90%+ test coverage** before refactoring
2. **Refactor incrementally** - small, focused changes
3. **Run tests continuously** - `make validate` after each change
4. **Update architecture docs** to reflect new structure

### 📚 Documentation

**Documentation Standards**:

- **English only** following FLEXT ecosystem standards
- **Technical accuracy** - all examples must work
- **Professional tone** - no marketing language, clear technical communication
- **Comprehensive coverage** - API changes require doc updates

**Documentation Types**:

- **API Documentation**: Update `docs/api/README.md` for endpoint changes
- **Architecture Documentation**: Update `docs/architecture/README.md` for design changes
- **Configuration**: Update `docs/configuration/README.md` for new settings
- **Development**: Update `docs/development/README.md` for workflow changes

## 🏗️ Development Workflow

### Branch Strategy

```bash
# Feature branches
git checkout -b feature/add-authentication
git checkout -b feature/implement-persistence

# Bug fix branches
git checkout -b fix/issue-123-validation-error
git checkout -b fix/memory-leak-in-handler

# Refactoring branches
git checkout -b refactor/split-monolithic-init
git checkout -b refactor/clean-dependencies
```

### Development Process

#### 1. **Before Starting Development**

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature

# Verify environment
make diagnose
make validate
```

#### 2. **During Development**

```bash
# Run quality gates frequently
make check                    # Quick lint + type check
make test                     # Run tests with coverage
make validate                 # Complete validation

# Test your changes
make runserver               # Start development server
curl http://localhost:8080/health  # Test endpoints
```

#### 3. **Before Committing**

```bash
# Run complete validation
make validate

# Check test coverage
make coverage-html
# Open reports/coverage/index.html

# Format code
make format

# Verify pre-commit hooks
make pre-commit
```

#### 4. **Commit Guidelines**

```bash
# Use conventional commit format
git commit -m "feat: add user authentication system"
git commit -m "fix: resolve memory leak in application handler"
git commit -m "refactor: split monolithic init file into layers"
git commit -m "docs: update API documentation for new endpoints"
```

### Quality Gates

All contributions must pass these quality gates:

#### Automated Checks

```bash
make validate                 # Must pass before PR
├── make lint
├── make type-check          # MyPy strict type checking
├── make security            # Bandit + pip-audit
└── make test                # 90%+ coverage required
```

#### Manual Review Criteria

- **Architecture Compliance**: Follows Clean Architecture + DDD patterns
- **FLEXT Integration**: Uses flext-core patterns consistently
- **Code Quality**: Readable, maintainable, well-documented
- **Test Quality**: Comprehensive unit, integration, and API tests
- **Documentation**: All changes documented appropriately

## 🧪 Testing Requirements

### Test Coverage Standards

- **Minimum Coverage**: 90% overall coverage required
- **New Code**: 100% coverage for new features
- **Critical Paths**: 100% coverage for security and business logic
- **Edge Cases**: Comprehensive error condition testing

### Test Categories

```bash
# Unit Tests (fast, isolated)
pytest -m unit

# Integration Tests (with dependencies)
pytest -m integration

# API Tests (end-to-end)
pytest -m api

# Specific test files
pytest tests/test_domain_entities.py -v
```

### Writing Good Tests

```python
# Good test example
class TestFlextWebAppHandler:
    """Test application handler with proper setup"""

    def setup_method(self):
        """Setup for each test method"""
        self.handler = FlextWebAppHandler()

    def test_create_app_success(self):
        """Test successful application creation"""
        # Arrange
        name = "test-app"
        port = 3000
        host = "localhost"

        # Act
        result = self.handler.create(name, port, host)

        # Assert
        assert result.success
        assert result.data is not None
        assert result.data.name == name
        assert result.data.port == port
        assert result.data.host == host
        assert result.data.status == FlextWebAppStatus.STOPPED

    def test_create_app_invalid_name(self):
        """Test application creation with invalid name"""
        # Act
        result = self.handler.create("", 3000, "localhost")

        # Assert
        assert not result.success
        assert "App name is required" in result.error

    @pytest.mark.parametrize("port", [0, 70000, -1])
    def test_create_app_invalid_port(self, port):
        """Test application creation with invalid ports"""
        result = self.handler.create("test-app", port, "localhost")

        assert not result.success
        assert "Invalid port number" in result.error
```

## 📝 Pull Request Process

### Creating a Pull Request

1. **Push your branch**:

   ```bash
   git push origin feature/your-feature
   ```

2. **Create PR** using the GitHub interface or CLI:

   ```bash
   gh pr create --title "feat: add amazing feature" --body "Description of changes"
   ```

3. **PR Template** (use this structure):

   ```markdown
   ## Description

   Brief description of changes and motivation.

   ## Type of Change

   - [ ] Bug fix (non-breaking change that fixes an issue)
   - [ ] New feature (non-breaking change that adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update
   - [ ] Refactoring (no functional changes)

   ## Changes Made

   - Detailed list of changes
   - Include file modifications
   - Mention any configuration changes

   ## Testing

   - [ ] All existing tests pass
   - [ ] New tests added for new functionality
   - [ ] Manual testing completed
   - [ ] API endpoints tested with curl/Postman

   ## Documentation

   - [ ] Code comments updated
   - [ ] API documentation updated
   - [ ] README updated if needed
   - [ ] Architecture docs updated if needed

   ## Quality Gates

   - [ ] `make validate` passes
   - [ ] Test coverage ≥ 90%
   - [ ] Type checking passes
   - [ ] Security scanning passes

   ## Screenshots/Examples

   (If applicable, include screenshots or example API calls)
   ```

### PR Review Process

#### Author Responsibilities

- **Self-review**: Review your own changes before requesting review
- **Quality gates**: Ensure all automated checks pass
- **Documentation**: Update all relevant documentation
- **Testing**: Add comprehensive tests for changes
- **Responsive**: Address review feedback promptly

#### Reviewer Guidelines

- **Architecture**: Verify Clean Architecture compliance
- **Patterns**: Check FLEXT ecosystem pattern usage
- **Security**: Review for security vulnerabilities
- **Performance**: Consider performance implications
- **Maintainability**: Ensure code is readable and maintainable

#### Review Checklist

- [ ] **Code Quality**: Follows project standards
- [ ] **Architecture**: Maintains Clean Architecture layers
- [ ] **Testing**: Comprehensive test coverage
- [ ] **Documentation**: All changes documented
- [ ] **Security**: No security vulnerabilities introduced
- [ ] **Performance**: No performance regressions
- [ ] **Integration**: Uses flext-core patterns correctly

### Merge Requirements

**Before merge, ensure**:

- [ ] All quality gates pass (automated checks)
- [ ] At least one code review approval
- [ ] All review feedback addressed
- [ ] Documentation updated
- [ ] No merge conflicts with main branch

## 🎯 Priority Contribution Areas

### High Priority (see [TODO.md](../TODO.md))

1. **Dependency Cleanup** - Remove unused Django/FastAPI/Celery dependencies
2. **Architecture Refactoring** - Split monolithic `__init__.py` into proper layers
3. **Persistence Layer** - Replace in-memory storage with database
4. **Authentication Integration** - Add flext-auth integration

### Medium Priority

1. **Template System** - Fix Django/Flask template inconsistency
2. **Real Application Management** - Connect to actual processes/containers
3. **Observability Integration** - Enhanced flext-observability integration
4. **API Documentation** - OpenAPI/Swagger specification

### Low Priority

1. **Performance Optimization** - Caching, async operations
2. **Advanced Features** - WebSocket support, batch operations
3. **UI Enhancement** - Modern frontend framework integration
4. **Multi-tenancy** - Support for multiple organizations

## 🚨 Common Issues & Solutions

### Development Issues

**Issue**: Tests failing after changes

```bash
# Solution: Run specific failing tests with verbose output
pytest tests/test_specific.py -v -s

# Check coverage for missing tests
make coverage-html
```

**Issue**: Type checking errors

```bash
# Solution: Run mypy with error codes
poetry run mypy src --show-error-codes

# Fix common issues
# - Add type hints to function parameters
# - Use Union types for optional parameters
# - Import types from typing module
```

**Issue**: Linting errors

```bash
# Solution: Auto-fix most issues
make format
make fix

# Manual fixes for remaining issues
poetry run ruff check src --fix
```

### Contribution Issues

**Issue**: PR checks failing

- **Solution**: Run `make validate` locally before pushing
- **Check**: All quality gates must pass locally first

**Issue**: Merge conflicts

```bash
# Solution: Rebase on latest main
git fetch upstream
git rebase upstream/main
# Resolve conflicts, then force push
git push origin feature/your-feature --force-with-lease
```

**Issue**: Review feedback not addressed

- **Solution**: Address all feedback or explain why not
- **Communication**: Reply to each review comment
- **Re-request**: Request re-review after changes

## 🏆 Recognition

### Contributors

We recognize contributors in several ways:

- **README**: Contributors listed in project README
- **Release Notes**: Major contributions mentioned in releases
- **GitHub**: Contributor recognition in repository insights

### Becoming a Maintainer

Regular contributors who demonstrate:

- **Technical Excellence**: High-quality contributions
- **Architecture Understanding**: Deep understanding of Clean Architecture and DDD
- **Community Engagement**: Helpful in discussions and reviews
- **Reliability**: Consistent contributions over time

May be invited to become project maintainers with commit access and review responsibilities.

## 📞 Getting Help

### Resources

- **[Development Guide](../development/README.md)** - Development setup and workflows
- **[Architecture Guide](../architecture/README.md)** - System design and patterns
- **[FLEXT Documentation](https://github.com/flext-sh/flext)** - Ecosystem overview

### Communication

- **GitHub Issues**: Bug reports, feature requests, questions
- **GitHub Discussions**: General questions, architecture discussions
- **PR Comments**: Code-specific discussions during review

### Code of Conduct

We follow the **FLEXT Code of Conduct**:

- **Respectful**: Treat all contributors with respect
- **Professional**: Maintain professional communication
- **Inclusive**: Welcome contributors from all backgrounds
- **Constructive**: Provide constructive feedback and criticism
- **Collaborative**: Work together toward common goals

---

**Thank you for contributing to FLEXT Web Interface!**

Your contributions help build the enterprise-grade distributed data integration platform that powers modern data operations. Together, we're creating something remarkable. 🚀

---

**Contributing Standards**: Clean Architecture • Quality First • Documentation Complete  
**Next Review**: After major architecture refactoring completion
