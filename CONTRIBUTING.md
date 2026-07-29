# Contributing to Family Tree

Thank you for your interest in contributing to the Family Tree project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to help build something great!

## Getting Started

### 1. Fork the Repository
Click the "Fork" button on GitHub to create your own copy

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR-USERNAME/Family_Project.git
cd Family_Project
```

### 3. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 isort
```

### 4. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Code Style

We follow PEP 8 with some preferences:

**Format code with Black**:
```bash
black .
```

**Sort imports**:
```bash
isort .
```

**Check code quality**:
```bash
flake8 .
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### Example Code Style
```python
def calculate_family_age(birth_date):
    """Calculate age from birth date.
    
    Args:
        birth_date: datetime.date object
        
    Returns:
        int: Age in years
    """
    from datetime import date
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age
```

## Types of Contributions

### Bug Reports
1. Check if bug already exists in Issues
2. Click "New Issue"
3. Provide:
   - Clear title
   - Description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment info (OS, Python version, etc.)

### Feature Requests
1. Open an Issue with label "feature-request"
2. Describe the feature
3. Explain why it would be useful
4. Provide examples if possible

### Code Contributions

#### Small Changes (Typos, Comments)
1. Make changes on feature branch
2. Commit with clear message
3. Push and create pull request

#### New Features
1. **Discuss First**: Open an issue to discuss the feature
2. **Create Branch**: `git checkout -b feature/your-feature`
3. **Develop**: Write code and tests
4. **Test**: Run tests locally
5. **Commit**: Write clear commit messages
6. **Push**: Push to your fork
7. **Pull Request**: Create detailed PR

#### Bug Fixes
1. Create branch: `git checkout -b fix/bug-description`
2. Write failing test first (TDD)
3. Fix the bug
4. Verify tests pass
5. Create pull request with issue reference

## Testing

### Run Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Write Tests
Create test files in a `tests/` directory:

```python
# tests/test_models.py
import pytest
from app import app, db
from models.user import User

def test_user_password_hashing():
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
```

## Commit Messages

Write clear, descriptive commit messages:

```
format: <type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, missing semicolons, etc
- `refactor`: Refactoring code
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Build process, dependencies, etc

### Examples
```
feat(auth): Add two-factor authentication

implement 2FA using TOTP for enhanced security
- Added TOTP token generation
- Updated login flow
- Added settings page for 2FA management

Closes #123
```

```
fix(family-tree): Fix relationship circular reference

prevent circular relationships between family members
```

## Pull Request Process

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] No hardcoded secrets or API keys
- [ ] Commit history is clean

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How to Test
Steps to test the changes:
1. 
2.
3.

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Follows code style
- [ ] Tested in different browsers

Closes #<issue-number>
```

## Documentation

### Update Documentation
- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment changes
- Add docstrings to new functions
- Update this file if adding new contribution types

### Docstring Format
```python
def example_function(param1, param2):
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is invalid
    """
    pass
```

## Project Structure

### Where to Add

**New Models**: `models/`
```python
# models/new_model.py
from models import db

class NewModel(db.Model):
    __tablename__ = 'new_models'
    # ...
```

**New Routes**: `routes/`
```python
# routes/new_routes.py
from flask import Blueprint

new_bp = Blueprint('new', __name__)

@new_bp.route('/new', methods=['GET'])
def example():
    return 'example'
```

**New Templates**: `templates/`
- Follow naming: `feature_name.html`
- Extend `base.html`

**New Styles**: `static/css/style.css`
- Use CSS variables defined in `:root`

**New Scripts**: `static/js/script.js`
- Keep global namespace clean
- Use proper namespacing

## Common Tasks

### Add New Database Model
1. Create file in `models/`
2. Define model class extending `db.Model`
3. Import in `app.py`
4. Create migration (or recreate database)
5. Add tests

### Add New Route/Feature
1. Create blueprint in `routes/`
2. Create route function with docstring
3. Create template in `templates/`
4. Register blueprint in `app.py`
5. Add navigation link in `base.html`
6. Add tests

### Update Dependencies
1. Update `requirements.txt`
2. Test thoroughly
3. Document breaking changes
4. Create PR with CHANGELOG entry

## Release Process

1. Update version in `app.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push: `git push origin v1.0.0`
5. Create GitHub Release

## Getting Help

- **Issues**: Check existing issues first
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Read README.md and other docs
- **Email**: Contact maintainers if needed

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes

## License

By contributing, you agree your contributions will be under the same license as the project (MIT).

## Questions?

Feel free to:
- Open an issue with label "question"
- Start a discussion
- Contact maintainers directly

Thank you for contributing! 🙌
