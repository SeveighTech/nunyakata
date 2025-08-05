#!/usr/bin/env python3
"""
Comprehensive test runner for the Nunyakata project.

This script runs all tests, linting, formatting checks, and code quality tools
in the correct order, providing a single command to validate the entire codebase.

Usage:
    python run_tests.py              # Run all checks
    python run_tests.py --fast       # Skip slow checks (security, docs)
    python run_tests.py --coverage   # Run only tests with coverage
    python run_tests.py --lint       # Run only linting and formatting
    python run_tests.py --help       # Show help
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class TestRunner:
    """Main test runner class."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.failed_checks = []
        self.passed_checks = []

    def run_command(
        self, command: List[str], description: str, check_return_code: bool = True
    ) -> bool:
        """Run a command and return success status."""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{description}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Running: {' '.join(command)}{Colors.ENDC}\n")

        try:
            result = subprocess.run(
                command, cwd=self.project_root, capture_output=False, text=True
            )

            if check_return_code and result.returncode != 0:
                print(f"\n{Colors.FAIL}❌ {description} FAILED{Colors.ENDC}")
                self.failed_checks.append(description)
                return False
            else:
                print(f"\n{Colors.OKGREEN}✅ {description} PASSED{Colors.ENDC}")
                self.passed_checks.append(description)
                return True

        except FileNotFoundError as e:
            print(f"\n{Colors.FAIL}❌ Command not found: {e}{Colors.ENDC}")
            self.failed_checks.append(f"{description} (command not found)")
            return False
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ Error running {description}: {e}{Colors.ENDC}")
            self.failed_checks.append(f"{description} (error)")
            return False

    def is_tool_installed(self, tool_name: str) -> bool:
        """Check if a Python tool is installed."""
        try:
            subprocess.run(
                ["python3", "-m", tool_name, "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed."""
        print(f"{Colors.HEADER}🔍 Checking Dependencies{Colors.ENDC}")

        # Check Python 3
        try:
            subprocess.run(["python3", "--version"], capture_output=True, check=True)
            print(f"{Colors.OKGREEN}✅ Python 3 found{Colors.ENDC}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.FAIL}❌ Python 3 not found{Colors.ENDC}")
            return False

        # Check pip (try both pip and pip3)
        self.pip_command = None
        for pip_cmd in ["pip", "pip3"]:
            try:
                subprocess.run([pip_cmd, "--version"], capture_output=True, check=True)
                print(
                    f"{Colors.OKGREEN}✅ Pip package manager found ({pip_cmd}){Colors.ENDC}"
                )
                self.pip_command = pip_cmd
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        if not self.pip_command:
            print(f"{Colors.FAIL}❌ Pip package manager not found{Colors.ENDC}")
            return False

        return True

    def install_dev_dependencies(self) -> bool:
        """Install development dependencies."""
        return self.run_command(
            ["python3", "-m", self.pip_command, "install", "-r", "requirements-dev.txt"],
            "Installing Development Dependencies",
        )

    def run_formatting_check(self) -> bool:
        """Run code formatting checks."""
        success = True

        # Black formatting check
        success &= self.run_command(
            ["python3", "-m", "black", "--check", "src/", "tests/"],
            "Code Formatting Check (Black)",
        )

        # Import sorting check
        success &= self.run_command(
            ["python3", "-m", "isort", "--check-only", "src/", "tests/"],
            "Import Sorting Check (isort)",
        )

        return success

    def run_linting(self) -> bool:
        """Run linting checks."""
        success = True

        # Critical flake8 checks (syntax errors, undefined names)
        success &= self.run_command(
            [
                "python3",
                "-m",
                "flake8",
                "src",
                "--count",
                "--select=E9,F63,F7,F82",
                "--show-source",
                "--statistics",
            ],
            "Critical Linting Check (Flake8 - Syntax & Undefined Names)",
        )

        # Full flake8 check (warnings only)
        self.run_command(
            [
                "python3",
                "-m",
                "flake8",
                "src",
                "--count",
                "--exit-zero",
                "--max-complexity=10",
                "--max-line-length=127",
                "--statistics",
            ],
            "Full Linting Check (Flake8 - Style)",
            check_return_code=False,
        )

        return success

    def run_type_checking(self) -> bool:
        """Run type checking."""
        return self.run_command(
            ["python3", "-m", "mypy", "src/nunyakata"], "Type Checking (MyPy)"
        )

    def run_tests_with_coverage(self) -> bool:
        """Run tests with coverage reporting."""
        return self.run_command(
            [
                "python3",
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--cov=src/nunyakata",
                "--cov-report=term-missing",
                "--cov-report=xml",
                "--cov-fail-under=70",
            ],
            "Unit Tests with Coverage",
        )

    def run_tests_only(self) -> bool:
        """Run tests without coverage (faster)."""
        return self.run_command(
            ["python3", "-m", "pytest", "tests/", "-v"], "Unit Tests (No Coverage)"
        )

    def run_integration_tests(self) -> bool:
        """Run integration tests if they exist."""
        # Check if integration tests exist
        result = subprocess.run(
            [
                "python3",
                "-m",
                "pytest",
                "tests/",
                "-m",
                "integration",
                "--collect-only",
                "-q",
            ],
            cwd=self.project_root,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0 and result.stdout.strip():
            return self.run_command(
                ["python3", "-m", "pytest", "tests/", "-m", "integration", "-v"],
                "Integration Tests",
            )
        else:
            print(
                f"{Colors.WARNING}⚠️  No integration tests found - skipping{Colors.ENDC}"
            )
            return True

    def run_security_checks(self) -> bool:
        """Run security scans."""
        success = True

        # Check and install security tools if not present
        tools_to_install = []
        if not self.is_tool_installed("safety"):
            tools_to_install.append("safety")
        if not self.is_tool_installed("bandit"):
            tools_to_install.append("bandit[toml]")

        if tools_to_install:
            subprocess.run(
                ["python3", "-m", "pip", "install"] + tools_to_install,
                capture_output=True,
            )
        # Bandit security check
        self.run_command(
            [
                "python3",
                "-m",
                "bandit",
                "-r",
                "src",
                "-f",
                "json",
                "-o",
                "bandit-report.json",
            ],
            "Security Check (Bandit)",
            check_return_code=False,  # Don't fail on security warnings
        )

        # Safety dependency check
        self.run_command(
            ["python3", "-m", "safety", "check"],
            "Dependency Security Check (Safety)",
            check_return_code=False,  # Don't fail on security warnings
        )

        return success

    def build_package(self) -> bool:
        """Build the package."""
        # Install build tools
        success = self.run_command(
            ["python3", "-m", "pip", "install", "build", "twine"],
            "Installing Build Dependencies",
        )

        if not success:
            return False

        # Build package
        success &= self.run_command(["python3", "-m", "build"], "Building Package")

        # Check package
        if success:
            success &= self.run_command(
                ["python3", "-m", "twine", "check", "dist/*"],
                "Package Validation (Twine)",
            )

        return success

    def build_docs(self) -> bool:
        """Build documentation if possible."""
        if (self.project_root / "mkdocs.yml").exists():
            return self.run_command(
                ["mkdocs", "build"], "Building Documentation (MkDocs)"
            )
        else:
            print(
                f"{Colors.WARNING}⚠️  No mkdocs.yml found - skipping documentation build{Colors.ENDC}"
            )
            return True

    def print_summary(self):
        """Print a summary of all checks."""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")

        if self.passed_checks:
            print(
                f"\n{Colors.OKGREEN}✅ PASSED ({len(self.passed_checks)}):{Colors.ENDC}"
            )
            for check in self.passed_checks:
                print(f"   • {check}")

        if self.failed_checks:
            print(f"\n{Colors.FAIL}❌ FAILED ({len(self.failed_checks)}):{Colors.ENDC}")
            for check in self.failed_checks:
                print(f"   • {check}")

        total_checks = len(self.passed_checks) + len(self.failed_checks)
        success_rate = (
            (len(self.passed_checks) / total_checks * 100) if total_checks > 0 else 0
        )

        print(
            f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}% ({len(self.passed_checks)}/{total_checks}){Colors.ENDC}"
        )

        if self.failed_checks:
            print(
                f"\n{Colors.FAIL}❌ Some checks failed. Please review the output above.{Colors.ENDC}"
            )
            return False
        else:
            print(
                f"\n{Colors.OKGREEN}🎉 All checks passed! Your code is ready for production.{Colors.ENDC}"
            )
            return True

    def run_all_checks(self, fast: bool = False, coverage: bool = True) -> bool:
        """Run all checks based on options."""
        print(f"{Colors.HEADER}{Colors.BOLD}Nunyakata Test Runner{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Running comprehensive test suite...{Colors.ENDC}")

        # Check dependencies first
        if not self.check_dependencies():
            return False

        # Install dependencies
        if not self.install_dev_dependencies():
            return False

        # Code quality checks
        self.run_formatting_check()
        self.run_linting()
        self.run_type_checking()

        # Tests
        if coverage:
            self.run_tests_with_coverage()
        else:
            self.run_tests_only()

        self.run_integration_tests()

        # Slower checks (skip if fast mode)
        if not fast:
            self.run_security_checks()
            self.build_package()
            self.build_docs()

        return self.print_summary()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Comprehensive test runner for Nunyakata project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                 # Run all checks
    python run_tests.py --fast          # Skip slow checks
    python run_tests.py --coverage      # Run tests with coverage only
    python run_tests.py --lint          # Run linting and formatting only
    python run_tests.py --no-coverage   # Run tests without coverage (faster)
        """,
    )

    parser.add_argument(
        "--fast", action="store_true", help="Skip slow checks (security, docs, build)"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run only tests with coverage"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Run tests without coverage reporting (faster)",
    )
    parser.add_argument(
        "--lint", action="store_true", help="Run only linting and formatting checks"
    )

    args = parser.parse_args()

    runner = TestRunner()

    try:
        if args.coverage:
            # Only run tests with coverage
            success = (
                runner.check_dependencies()
                and runner.install_dev_dependencies()
                and runner.run_tests_with_coverage()
            )
        elif args.lint:
            # Only run linting and formatting
            success = (
                runner.check_dependencies()
                and runner.install_dev_dependencies()
                and runner.run_formatting_check()
                and runner.run_linting()
                and runner.run_type_checking()
            )
        else:
            # Run all checks
            success = runner.run_all_checks(
                fast=args.fast, coverage=not args.no_coverage
            )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Test run interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
