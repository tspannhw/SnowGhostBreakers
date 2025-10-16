#!/usr/bin/env python3
"""
Master Test Runner for Ghost Detection System
Runs all unit and integration tests and generates comprehensive report
"""

import sys
import os
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.start_time = None
        self.results = {
            'python_tests': {},
            'sql_tests': {},
            'overall': {}
        }
        self.project_root = Path(__file__).parent
        
    def print_banner(self):
        """Print test banner"""
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════╗
║                     GHOST DETECTION SYSTEM                               ║
║                   COMPREHENSIVE TEST SUITE                               ║
║                         Master Test Runner                               ║
╚══════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
Test Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Project Root: {self.project_root}
Python Version: {sys.version.split()[0]}
"""
        print(banner)
    
    def print_section(self, title):
        """Print section header"""
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}")
        print("━" * 80)
        print(f"{title}")
        print("━" * 80)
        print(Colors.ENDC)
    
    def run_python_tests(self):
        """Run Python unit and integration tests"""
        self.print_section("PHASE 1: PYTHON TESTS")
        
        test_dir = self.project_root / "tests" / "python"
        
        if not test_dir.exists():
            print(f"{Colors.WARNING}Warning: Python test directory not found{Colors.ENDC}")
            return False
        
        print(f"Running pytest from: {test_dir}")
        print("")
        
        # Run pytest with various options
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(test_dir),
            "-v",
            "--tb=short",
            "-ra",
            "--color=yes"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.project_root),
                capture_output=False,
                text=True
            )
            
            self.results['python_tests'] = {
                'status': 'PASS' if result.returncode == 0 else 'FAIL',
                'return_code': result.returncode
            }
            
            if result.returncode == 0:
                print(f"\n{Colors.OKGREEN}✅ Python tests PASSED{Colors.ENDC}")
                return True
            else:
                print(f"\n{Colors.FAIL}❌ Python tests FAILED{Colors.ENDC}")
                return False
                
        except FileNotFoundError:
            print(f"{Colors.FAIL}Error: pytest not found. Install with: pip install pytest{Colors.ENDC}")
            return False
        except Exception as e:
            print(f"{Colors.FAIL}Error running Python tests: {e}{Colors.ENDC}")
            return False
    
    def run_sql_tests(self):
        """Run SQL tests (requires Snowflake connection)"""
        self.print_section("PHASE 2: SQL TESTS")
        
        sql_test_file = self.project_root / "tests" / "sql" / "00_run_all_sql_tests.sql"
        
        if not sql_test_file.exists():
            print(f"{Colors.WARNING}Warning: SQL test file not found{Colors.ENDC}")
            return False
        
        print("SQL tests require Snowflake connection.")
        print(f"Test file location: {sql_test_file}")
        print("")
        print("To run SQL tests:")
        print(f"  1. Connect to Snowflake using SnowSQL or Snowflake UI")
        print(f"  2. Execute: {sql_test_file}")
        print(f"  3. Review results in TEST_RESULTS table")
        print("")
        
        # Check if snowsql is available
        try:
            result = subprocess.run(
                ["snowsql", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"{Colors.OKGREEN}SnowSQL detected: {result.stdout.strip()}{Colors.ENDC}")
                print("You can run SQL tests with:")
                print(f"  snowsql -f {sql_test_file}")
                self.results['sql_tests'] = {'status': 'AVAILABLE', 'message': 'SnowSQL detected'}
            else:
                self.results['sql_tests'] = {'status': 'MANUAL', 'message': 'Run manually in Snowflake'}
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"{Colors.WARNING}SnowSQL not found. Run SQL tests manually in Snowflake.{Colors.ENDC}")
            self.results['sql_tests'] = {'status': 'MANUAL', 'message': 'SnowSQL not available'}
        
        return True
    
    def check_test_dependencies(self):
        """Check if test dependencies are installed"""
        self.print_section("DEPENDENCY CHECK")
        
        dependencies = {
            'pytest': 'pytest',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'snowflake-snowpark-python': 'snowflake.snowpark'
        }
        
        missing = []
        installed = []
        
        for package, import_name in dependencies.items():
            try:
                __import__(import_name)
                installed.append(package)
                print(f"{Colors.OKGREEN}✓{Colors.ENDC} {package}")
            except ImportError:
                missing.append(package)
                print(f"{Colors.FAIL}✗{Colors.ENDC} {package} (missing)")
        
        print("")
        
        if missing:
            print(f"{Colors.WARNING}Missing dependencies: {', '.join(missing)}{Colors.ENDC}")
            print(f"Install with: pip install {' '.join(missing)}")
            return False
        else:
            print(f"{Colors.OKGREEN}All dependencies installed!{Colors.ENDC}")
            return True
    
    def generate_summary(self):
        """Generate test summary"""
        self.print_section("TEST SUMMARY")
        
        end_time = time.time()
        duration = end_time - self.start_time
        
        print(f"Total Execution Time: {duration:.2f} seconds")
        print("")
        
        # Python tests summary
        python_status = self.results.get('python_tests', {}).get('status', 'NOT RUN')
        python_icon = "✅" if python_status == 'PASS' else "❌" if python_status == 'FAIL' else "⏭️"
        
        print(f"Python Tests:  {python_icon} {python_status}")
        
        # SQL tests summary
        sql_status = self.results.get('sql_tests', {}).get('status', 'NOT RUN')
        sql_icon = "✅" if sql_status == 'PASS' else "⚠️" if sql_status in ['AVAILABLE', 'MANUAL'] else "⏭️"
        
        print(f"SQL Tests:     {sql_icon} {sql_status}")
        print("")
        
        # Overall status
        if python_status == 'PASS':
            print(f"{Colors.OKGREEN}{Colors.BOLD}")
            print("╔══════════════════════════════════════════════════════════════════════════╗")
            print("║                       ✅ PYTHON TESTS PASSED! ✅                        ║")
            print("║                                                                          ║")
            print("║         All Python unit and integration tests successful                ║")
            print("╚══════════════════════════════════════════════════════════════════════════╝")
            print(Colors.ENDC)
        else:
            print(f"{Colors.WARNING}{Colors.BOLD}")
            print("╔══════════════════════════════════════════════════════════════════════════╗")
            print("║                     ⚠️  REVIEW TEST RESULTS  ⚠️                        ║")
            print("║                                                                          ║")
            print("║         Please check test output above for details                      ║")
            print("╚══════════════════════════════════════════════════════════════════════════╝")
            print(Colors.ENDC)
        
        # Save results to file
        self.save_results()
    
    def save_results(self):
        """Save test results to JSON file"""
        results_file = self.project_root / "tests" / "test_results.json"
        
        self.results['overall'] = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': time.time() - self.start_time,
            'python_version': sys.version.split()[0]
        }
        
        try:
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\nResults saved to: {results_file}")
        except Exception as e:
            print(f"Warning: Could not save results: {e}")
    
    def run(self):
        """Run all tests"""
        self.start_time = time.time()
        
        self.print_banner()
        
        # Check dependencies
        deps_ok = self.check_test_dependencies()
        if not deps_ok:
            print(f"\n{Colors.FAIL}Cannot run tests: missing dependencies{Colors.ENDC}")
            return 1
        
        # Run Python tests
        python_success = self.run_python_tests()
        
        # Run SQL tests (informational)
        self.run_sql_tests()
        
        # Generate summary
        self.generate_summary()
        
        # Return exit code
        return 0 if python_success else 1


def main():
    """Main entry point"""
    runner = TestRunner()
    exit_code = runner.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

