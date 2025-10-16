#!/usr/bin/env python3
"""
Test Validation Script
Validates that all test files are properly structured without running them
"""

import os
import sys
from pathlib import Path
import ast


class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def validate_python_syntax(file_path):
    """Validate Python file syntax"""
    try:
        with open(file_path, 'r') as f:
            ast.parse(f.read())
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def count_test_functions(file_path):
    """Count test functions in a file"""
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        
        test_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('test_'):
                    test_count += 1
        
        return test_count
    except:
        return 0


def count_test_classes(file_path):
    """Count test classes in a file"""
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        
        class_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if node.name.startswith('Test'):
                    class_count += 1
        
        return class_count
    except:
        return 0


def validate_sql_file(file_path):
    """Basic SQL file validation"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for basic SQL keywords
        has_sql = any(keyword in content.upper() for keyword in [
            'CREATE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'PROCEDURE'
        ])
        
        return has_sql, "Contains SQL statements"
    except Exception as e:
        return False, f"Error: {e}"


def main():
    """Main validation function"""
    project_root = Path(__file__).parent
    
    print(f"{Colors.BOLD}")
    print("="*80)
    print("GHOST DETECTION SYSTEM - TEST VALIDATION")
    print("="*80)
    print(f"{Colors.ENDC}\n")
    
    # Validate Python tests
    print(f"{Colors.BOLD}Python Tests:{Colors.ENDC}")
    print("-" * 80)
    
    python_test_dir = project_root / "tests" / "python"
    python_test_files = list(python_test_dir.glob("test_*.py"))
    
    total_test_functions = 0
    total_test_classes = 0
    python_valid = 0
    python_invalid = 0
    
    for test_file in sorted(python_test_files):
        is_valid, message = validate_python_syntax(test_file)
        test_funcs = count_test_functions(test_file)
        test_classes = count_test_classes(test_file)
        
        total_test_functions += test_funcs
        total_test_classes += test_classes
        
        if is_valid:
            python_valid += 1
            status = f"{Colors.OKGREEN}✓{Colors.ENDC}"
        else:
            python_invalid += 1
            status = f"{Colors.FAIL}✗{Colors.ENDC}"
        
        print(f"{status} {test_file.name:30} Classes: {test_classes:2} Functions: {test_funcs:3}")
    
    print(f"\n{Colors.BOLD}Python Test Summary:{Colors.ENDC}")
    print(f"  Test Files:     {len(python_test_files)}")
    print(f"  Valid Files:    {python_valid}")
    print(f"  Invalid Files:  {python_invalid}")
    print(f"  Test Classes:   {total_test_classes}")
    print(f"  Test Functions: {total_test_functions}")
    
    # Validate SQL tests
    print(f"\n{Colors.BOLD}SQL Tests:{Colors.ENDC}")
    print("-" * 80)
    
    sql_test_dir = project_root / "tests" / "sql"
    sql_test_files = list(sql_test_dir.glob("*.sql"))
    
    sql_valid = 0
    sql_invalid = 0
    
    for test_file in sorted(sql_test_files):
        is_valid, message = validate_sql_file(test_file)
        
        if is_valid:
            sql_valid += 1
            status = f"{Colors.OKGREEN}✓{Colors.ENDC}"
        else:
            sql_invalid += 1
            status = f"{Colors.FAIL}✗{Colors.ENDC}"
        
        print(f"{status} {test_file.name:40} {message}")
    
    print(f"\n{Colors.BOLD}SQL Test Summary:{Colors.ENDC}")
    print(f"  Test Files:    {len(sql_test_files)}")
    print(f"  Valid Files:   {sql_valid}")
    print(f"  Invalid Files: {sql_invalid}")
    
    # Check for required test infrastructure
    print(f"\n{Colors.BOLD}Test Infrastructure:{Colors.ENDC}")
    print("-" * 80)
    
    files_to_check = [
        ("conftest.py", python_test_dir / "conftest.py"),
        ("pytest.ini", python_test_dir / "pytest.ini"),
        ("__init__.py", python_test_dir / "__init__.py"),
        ("Master SQL Runner", sql_test_dir / "00_run_all_sql_tests.sql"),
        ("Test README", project_root / "tests" / "README.md"),
        ("Main Test Runner", project_root / "run_tests.py")
    ]
    
    infrastructure_ok = 0
    for name, path in files_to_check:
        if path.exists():
            status = f"{Colors.OKGREEN}✓{Colors.ENDC}"
            infrastructure_ok += 1
        else:
            status = f"{Colors.FAIL}✗{Colors.ENDC}"
        print(f"{status} {name:25} {path.name}")
    
    # Overall summary
    print(f"\n{Colors.BOLD}")
    print("="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"{Colors.ENDC}")
    
    total_files = len(python_test_files) + len(sql_test_files)
    total_valid = python_valid + sql_valid
    
    print(f"Total Test Files:    {total_files}")
    print(f"Valid Files:         {total_valid}")
    print(f"Test Functions:      {total_test_functions}")
    print(f"Test Classes:        {total_test_classes}")
    print(f"Infrastructure:      {infrastructure_ok}/{len(files_to_check)}")
    
    if python_invalid > 0 or sql_invalid > 0:
        print(f"\n{Colors.WARNING}⚠️  Some test files have issues{Colors.ENDC}")
        return 1
    elif total_valid == total_files and infrastructure_ok == len(files_to_check):
        print(f"\n{Colors.OKGREEN}✅ All tests are properly structured!{Colors.ENDC}")
        print(f"\n{Colors.BOLD}To run the tests:{Colors.ENDC}")
        print(f"  Python: pytest tests/python/ -v")
        print(f"  SQL:    snowsql -f tests/sql/00_run_all_sql_tests.sql")
        print(f"  All:    python run_tests.py")
        return 0
    else:
        print(f"\n{Colors.WARNING}⚠️  Test infrastructure incomplete{Colors.ENDC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

