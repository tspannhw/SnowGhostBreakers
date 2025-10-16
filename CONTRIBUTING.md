# Contributing to SnowGhost Breakers

Thank you for your interest in contributing to the Ghost Detection System! 👻✨

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating an issue
3. **Include:**
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (Snowflake version, Python version, etc.)
   - Screenshots if applicable

### Suggesting Enhancements

1. **Check existing feature requests**
2. **Use the feature request template**
3. **Describe:**
   - The problem you're trying to solve
   - Your proposed solution
   - Why this would be useful to other users

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Follow coding standards** (see below)
5. **Add/update tests** if applicable
6. **Update documentation**
7. **Commit with clear messages**
   ```bash
   git commit -m "feat: Add ghost classification algorithm"
   ```
8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Create a Pull Request**

## 📋 Development Setup

### Prerequisites

- Python 3.8+
- Snowflake account with Cortex AI enabled
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SnowGhostBreakers.git
   cd SnowGhostBreakers
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your Snowflake credentials
   ```

5. **Run tests**
   ```bash
   pytest tests/
   ```

## 🎨 Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

**Example:**
```python
def classify_ghost(description: str, confidence_threshold: float = 0.8) -> Dict[str, Any]:
    """
    Classify ghost type from description using Cortex AI.
    
    Args:
        description: Text description of the ghost encounter
        confidence_threshold: Minimum confidence score (0.0 to 1.0)
        
    Returns:
        Dictionary containing ghost_type, confidence_score, and reasoning
        
    Raises:
        ValueError: If description is empty or threshold is invalid
    """
    # Implementation
```

### SQL

- Use uppercase for SQL keywords
- Use snake_case for table/column names
- Include comments for complex queries
- Use proper indentation

**Example:**
```sql
-- Get ghost activity summary by location
SELECT 
    location_name,
    COUNT(DISTINCT ghost_id) AS unique_ghosts,
    COUNT(*) AS total_sightings,
    AVG(danger_level) AS avg_danger,
    MAX(sighting_datetime) AS last_sighting
FROM GHOST_SIGHTINGS
WHERE sighting_datetime >= DATEADD(day, -30, CURRENT_DATE())
GROUP BY location_name
HAVING COUNT(*) > 5
ORDER BY total_sightings DESC;
```

### Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, no logic change)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add Neo4j graph analytics integration
fix: Resolve INTO clause error in stored procedures
docs: Update installation guide for Windows users
test: Add unit tests for ghost classification
```

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/python/test_cortex_ai.py

# With coverage
pytest --cov=. --cov-report=html

# SQL tests (in Snowflake)
# Run: sql/00_run_all_sql_tests.sql
```

### Writing Tests

```python
import pytest
from your_module import classify_ghost

def test_classify_ghost_valid_input():
    """Test ghost classification with valid input"""
    result = classify_ghost("Cold spots and EMF spikes")
    assert result['ghost_type'] is not None
    assert 0.0 <= result['confidence_score'] <= 1.0

def test_classify_ghost_empty_input():
    """Test ghost classification with empty input"""
    with pytest.raises(ValueError):
        classify_ghost("")
```

## 🔒 Security

- **Never commit credentials** (see SECURITY.md)
- Use environment variables for sensitive data
- Follow principle of least privilege
- Report security issues privately

## 📝 Documentation

- Update README.md for new features
- Add docstrings to Python code
- Add comments to SQL for complex logic
- Update relevant guides (QUICKSTART.md, etc.)

## 🏗️ Project Structure

```
SnowGhostBreakers/
├── sql/                    # SQL scripts
│   ├── 01_setup_database.sql
│   ├── 02_create_tables.sql
│   └── ...
├── streamlit_app/          # Streamlit application
├── notebooks/              # Jupyter notebooks
├── scripts/                # Python scripts
├── tests/                  # Test files
│   ├── sql/               # SQL tests
│   └── python/            # Python tests
├── mcp/                    # MCP server configuration
└── docs/                   # Documentation (future)
```

## 🎯 Areas for Contribution

We especially welcome contributions in:

- 🧪 **Testing:** More comprehensive test coverage
- 📊 **Visualizations:** New chart types and dashboards
- 🤖 **AI Features:** Enhanced Cortex AI integrations
- 📚 **Documentation:** Tutorials, examples, guides
- 🐛 **Bug Fixes:** Fixing reported issues
- ⚡ **Performance:** Optimization and efficiency improvements
- 🌐 **Integrations:** New data sources or export formats

## ❓ Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/SnowGhostBreakers/discussions)
- Check existing [Issues](https://github.com/yourusername/SnowGhostBreakers/issues)
- Review the [README](README.md) and guides

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for helping make ghost detection better for everyone!** 👻🚫✨

