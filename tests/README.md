# 🧪 Ghost Detection System - Test Suite

Comprehensive test suite for the Ghost Detection System with both SQL and Python tests.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)

## 🎯 Overview

This test suite ensures the reliability and correctness of all Ghost Detection System components:

- **SQL Tests**: Database schema, stored procedures, views, and data integrity
- **Python Tests**: Streamlit app, MCP server, Cortex AI integration
- **Integration Tests**: End-to-end workflows and system integration

### Test Statistics

| Component | Test Files | Test Cases | Coverage |
|-----------|-----------|------------|----------|
| SQL Unit Tests | 2 | 13+ | Stored Procedures, Views |
| SQL Integration | 2 | 7+ | Schema, Constraints, AI |
| Python Unit Tests | 3 | 70+ | App, MCP, Cortex AI |
| **Total** | **7** | **90+** | **All Components** |

## 📁 Test Structure

```
tests/
├── sql/
│   ├── 00_run_all_sql_tests.sql      # Master SQL test runner
│   ├── 01_unit_tests_stored_procedures.sql
│   └── 02_integration_tests_schema.sql
├── python/
│   ├── __init__.py
│   ├── conftest.py                    # Pytest fixtures
│   ├── pytest.ini                     # Pytest configuration
│   ├── test_streamlit_app.py         # Streamlit tests
│   ├── test_mcp_server.py            # MCP server tests
│   └── test_cortex_ai.py             # Cortex AI tests
└── README.md
```

## 🚀 Running Tests

### Quick Start - All Tests

```bash
# Run all Python tests
python run_tests.py

# Or use pytest directly
cd tests/python
pytest -v
```

### Python Tests Only

```bash
# Run all Python tests
pytest tests/python/ -v

# Run specific test file
pytest tests/python/test_streamlit_app.py -v

# Run specific test class
pytest tests/python/test_cortex_ai.py::TestCortexComplete -v

# Run with markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m cortex       # Cortex AI tests only
```

### SQL Tests

SQL tests require a Snowflake connection:

```sql
-- Option 1: Using Snowflake UI
-- Open tests/sql/00_run_all_sql_tests.sql
-- Execute in Snowflake worksheet

-- Option 2: Using SnowSQL
snowsql -f tests/sql/00_run_all_sql_tests.sql

-- View results
SELECT * FROM TEST_RESULTS ORDER BY test_datetime DESC;
```

## 📊 Test Categories

### SQL Tests

#### 1. Stored Procedure Unit Tests
- ✅ `TEST_PROCESS_GHOST_EVIDENCE` - Evidence processing
- ✅ `TEST_ANALYZE_SIGHTING_WITH_AI` - AI analysis
- ✅ `TEST_GENERATE_GHOST_REPORT` - Report generation
- ✅ `TEST_CREATE_INVESTIGATION` - Investigation creation
- ✅ `TEST_UPDATE_GHOST_STATUS` - Status updates
- ✅ `TEST_CALCULATE_THREAT_SCORE` - Threat scoring

#### 2. Schema Integration Tests
- ✅ `TEST_TABLE_EXISTS` - Table existence
- ✅ `TEST_FOREIGN_KEY_INTEGRITY` - Referential integrity
- ✅ `TEST_DATA_TYPE_VALIDATION` - Data validation
- ✅ `TEST_VIEW_ACCESSIBILITY` - View accessibility
- ✅ `TEST_CORTEX_AI_AVAILABILITY` - Cortex AI functions
- ✅ `TEST_BUSINESS_VOCABULARY_INTEGRATION` - Vocabulary tables
- ✅ `TEST_AGENTIC_AI_SYSTEM` - AI agent tables

### Python Tests

#### 1. Streamlit App Tests (`test_streamlit_app.py`)
- **Initialization**: Session setup, configuration
- **CRUD Operations**: Ghost, sighting, evidence operations
- **Data Validation**: Input validation, data integrity
- **Cortex AI Integration**: AI function calls
- **Visualizations**: Chart generation, data display
- **Business Vocabulary**: Ontology, taxonomy
- **Agentic AI**: Agent configuration, policies
- **Error Handling**: Edge cases, null values

#### 2. MCP Server Tests (`test_mcp_server.py`)
- **Initialization**: Server config, validation
- **Resource Endpoints**: URI format, metadata
- **Tool Endpoints**: Schema validation, parameters
- **Query Execution**: SQL execution, parameter binding
- **Data Serialization**: JSON handling, datetime
- **Authentication**: Credentials, roles, permissions
- **Caching**: Cache keys, expiration, invalidation
- **Error Handling**: Connection, query, resource errors
- **Performance**: Pagination, limiting, timeouts
- **Cortex Integration**: AI queries through MCP

#### 3. Cortex AI Tests (`test_cortex_ai.py`)
- **Cortex Complete**: Text generation, context
- **Cortex Sentiment**: Positive, negative, neutral
- **Cortex Translate**: Multi-language support
- **Cortex Embeddings**: Vector generation, similarity
- **Classification**: Ghost types, threat levels
- **Report Generation**: Investigation reports, briefs
- **Pattern Recognition**: Temporal, location patterns
- **Quality & Performance**: Response validation, confidence

## ✍️ Writing Tests

### Python Test Template

```python
import pytest
from unittest.mock import Mock, patch

class TestYourFeature:
    """Test your feature"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_data = {...}
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        # Arrange
        input_data = self.test_data
        
        # Act
        result = your_function(input_data)
        
        # Assert
        assert result is not None
        assert result['status'] == 'success'
    
    @patch('module.dependency')
    def test_with_mock(self, mock_dep):
        """Test with mocked dependency"""
        mock_dep.return_value = 'mocked_value'
        
        result = function_using_dependency()
        
        assert result == 'expected_value'
```

### SQL Test Template

```sql
CREATE OR REPLACE PROCEDURE TEST_YOUR_FEATURE()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Your test logic here
        -- ...
        
        result_status := 'PASS';
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_YOUR_FEATURE',
        'Test Category',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': TEST_YOUR_FEATURE';
END;
$$;
```

## 🔧 Test Fixtures

Common test fixtures are available in `conftest.py`:

```python
# Use fixtures in your tests
def test_with_fixtures(
    sample_ghost_data,
    sample_sighting_data,
    mock_snowpark_session
):
    # Fixtures automatically injected
    assert sample_ghost_data['ghost_name'] is not None
```

Available fixtures:
- `mock_snowpark_session` - Mocked Snowflake session
- `sample_ghost_data` - Sample ghost record
- `sample_sighting_data` - Sample sighting record
- `sample_evidence_data` - Sample evidence record
- `sample_ghosts_dataframe` - Sample DataFrame
- `mock_cortex_complete_response` - Mocked AI response
- And many more...

## 🔍 Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_test():
    """Fast unit test"""
    pass

@pytest.mark.integration
def test_integration_test():
    """Integration test"""
    pass

@pytest.mark.slow
def test_slow_test():
    """Slow running test"""
    pass

@pytest.mark.cortex
def test_cortex_feature():
    """Requires Cortex AI"""
    pass
```

Run specific markers:
```bash
pytest -m unit          # Only unit tests
pytest -m "not slow"    # Skip slow tests
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python run_tests.py
```

## 📊 Test Results

### Python Test Output

```
==================== test session starts ====================
collected 70 items

test_streamlit_app.py::TestStreamlitAppInitialization::test_session_initialization PASSED
test_streamlit_app.py::TestGhostDataOperations::test_ghost_data_validation PASSED
...

==================== 70 passed in 5.23s ====================
```

### SQL Test Output

```
╔══════════════════════════════════════════════════════╗
║           COMPREHENSIVE TEST SUMMARY                 ║
╚══════════════════════════════════════════════════════╝

Total Tests: 13
Passed: 13
Failed: 0
Success Rate: 100.00%
Average Execution Time: 125.5 ms
```

## 🐛 Debugging Failed Tests

### Python Tests

```bash
# Show detailed output
pytest -vv tests/python/test_streamlit_app.py

# Show print statements
pytest -s tests/python/test_streamlit_app.py

# Drop into debugger on failure
pytest --pdb tests/python/test_streamlit_app.py

# Show locals on failure
pytest -l tests/python/test_streamlit_app.py
```

### SQL Tests

```sql
-- View failed tests
SELECT * 
FROM TEST_RESULTS 
WHERE status = 'FAIL'
ORDER BY test_datetime DESC;

-- View error details
SELECT 
    test_name,
    error_message,
    execution_time_ms
FROM TEST_RESULTS
WHERE status = 'FAIL';
```

## 📚 Best Practices

1. **Write tests first** (TDD approach)
2. **Keep tests isolated** - No dependencies between tests
3. **Use descriptive names** - Test name should describe what it tests
4. **One assertion per test** - When possible
5. **Mock external dependencies** - Database, APIs, AI calls
6. **Test edge cases** - Null values, empty lists, invalid input
7. **Maintain fixtures** - Keep test data up to date
8. **Document complex tests** - Add comments explaining why

## 🆘 Support

For issues or questions:
1. Check test output for error messages
2. Review test documentation above
3. Check fixtures in `conftest.py`
4. Review sample tests for patterns

## 📝 License

Part of Ghost Detection System - All tests follow the same license as the main project.

