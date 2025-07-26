#!/usr/bin/env python3
"""
Test runner script for nunyakata package.
This script provides comprehensive testing capabilities.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description, exit_on_failure=True):
    """Run a command and handle the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print("=" * 60)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        if e.stdout:
            print(f"Output:\n{e.stdout}")
        if e.stderr:
            print(f"Error:\n{e.stderr}")

        if exit_on_failure:
            sys.exit(1)
        return False


def install_dependencies():
    """Install development dependencies."""
    return run_command(
        ["pip", "install", "-e", ".[dev,test,webhook]"],
        "Installing development dependencies",
    )


def run_linting():
    """Run code linting checks."""
    success = True

    # Black formatting check
    success &= run_command(
        ["black", "--check", "src", "tests"],
        "Checking code formatting with black",
        exit_on_failure=False,
    )

    # isort import sorting check
    success &= run_command(
        ["isort", "--check-only", "src", "tests"],
        "Checking import sorting with isort",
        exit_on_failure=False,
    )

    # Flake8 linting
    success &= run_command(
        ["flake8", "src", "tests"], "Running flake8 linting", exit_on_failure=False
    )

    return success


def run_type_checking():
    """Run type checking with mypy."""
    return run_command(
        ["mypy", "src/nunyakata"],
        "Running type checking with mypy",
        exit_on_failure=False,
    )


def run_unit_tests():
    """Run unit tests."""
    return run_command(
        [
            "pytest",
            "tests/",
            "-v",
            "-m",
            "unit",
            "--cov=src/nunyakata",
            "--cov-report=term-missing",
            "--cov-report=html",
        ],
        "Running unit tests",
    )


def run_integration_tests():
    """Run integration tests."""
    return run_command(
        [
            "pytest",
            "tests/",
            "-v",
            "-m",
            "integration",
            "--cov=src/nunyakata",
            "--cov-report=term-missing",
        ],
        "Running integration tests",
        exit_on_failure=False,
    )


def run_all_tests():
    """Run all tests."""
    return run_command(
        [
            "pytest",
            "tests/",
            "-v",
            "--cov=src/nunyakata",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=xml",
        ],
        "Running all tests",
    )


def run_security_checks():
    """Run security checks."""
    success = True

    # Install security tools if not available
    try:
        subprocess.run(["bandit", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing bandit...")
        subprocess.run(["pip", "install", "bandit[toml]"], check=True)

    try:
        subprocess.run(["safety", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing safety...")
        subprocess.run(["pip", "install", "safety"], check=True)

    # Run bandit security checks
    success &= run_command(
        ["bandit", "-r", "src", "-f", "json"],
        "Running security checks with bandit",
        exit_on_failure=False,
    )

    # Check for known security vulnerabilities
    success &= run_command(
        ["safety", "check"],
        "Checking for known security vulnerabilities",
        exit_on_failure=False,
    )

    return success


def format_code():
    """Format code with black and isort."""
    success = True

    success &= run_command(["black", "src", "tests"], "Formatting code with black")

    success &= run_command(["isort", "src", "tests"], "Sorting imports with isort")

    return success


def build_package():
    """Build the package."""
    # Install build tools
    run_command(["pip", "install", "build", "twine"], "Installing build tools")

    # Clean previous builds
    import shutil

    for path in ["dist", "build", "src/nunyakata.egg-info"]:
        if Path(path).exists():
            shutil.rmtree(path)
            print(f"Cleaned {path}")

    # Build package
    success = run_command(["python", "-m", "build"], "Building package")

    if success:
        # Check package
        run_command(
            ["python", "-m", "twine", "check", "dist/*"], "Checking package integrity"
        )

    return success


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Nunyakata test runner")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--type-check", action="store_true", help="Run type checking")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests"
    )
    parser.add_argument("--all-tests", action="store_true", help="Run all tests")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    parser.add_argument("--format", action="store_true", help="Format code")
    parser.add_argument("--build", action="store_true", help="Build package")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full test suite (equivalent to --lint --type-check --all-tests --security)",
    )

    args = parser.parse_args()

    # If no specific arguments, run basic tests
    if not any(vars(args).values()):
        args.all_tests = True

    success = True

    print("🚀 Nunyakata Test Runner")
    print("=" * 60)

    if args.install:
        success &= install_dependencies()

    if args.format:
        success &= format_code()

    if args.lint or args.full:
        success &= run_linting()

    if args.type_check or args.full:
        success &= run_type_checking()

    if args.unit:
        success &= run_unit_tests()

    if args.integration:
        success &= run_integration_tests()

    if args.all_tests or args.full:
        success &= run_all_tests()

    if args.security or args.full:
        success &= run_security_checks()

    if args.build:
        success &= build_package()

    print(f"\n{'='*60}")
    if success:
        print("🎉 All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
