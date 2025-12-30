#!/usr/bin/env python3
"""
Release script for Pikapika - similar to release-it for Python projects
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def update_version(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{new_version}"', content)
    pyproject_path.write_text(content)
    print(f"✅ Updated version to {new_version}")


def run_command(cmd: list, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"🔧 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result


def check_git_status() -> None:
    """Check if working directory is clean."""
    result = run_command(["git", "status", "--porcelain"])
    if result.stdout.strip():
        print("❌ Working directory is not clean. Please commit changes first.")
        sys.exit(1)
    print("✅ Working directory is clean")


def check_tests_pass() -> None:
    """Run tests to ensure they pass."""
    print("🧪 Running tests...")
    try:
        run_command(["uv", "run", "python", "-m", "pytest"])
        print("✅ All tests passed")
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        sys.exit(1)


def check_linting() -> None:
    """Run linting checks."""
    print("🔍 Running linting...")
    try:
        run_command(["uv", "run", "ruff", "check"])
        print("✅ Linting passed")
    except subprocess.CalledProcessError:
        print("❌ Linting failed")
        sys.exit(1)


def build_package() -> None:
    """Build the package."""
    print("📦 Building package...")
    try:
        run_command(["uv", "build"])
        print("✅ Package built successfully")
    except subprocess.CalledProcessError:
        print("❌ Build failed")
        sys.exit(1)


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse semantic version string."""
    match = re.match(r"v?(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    return tuple(map(int, match.groups()))


def bump_version(current: str, bump_type: str) -> str:
    """Bump version based on type."""
    major, minor, patch = parse_version(current)

    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return f"{major}.{minor}.{patch}"


def create_and_push_tag(version: str, dry_run: bool = False) -> None:
    """Create and push git tag."""
    tag = f"v{version}"

    if not dry_run:
        # Commit version change
        run_command(["git", "add", "pyproject.toml"])
        run_command(["git", "commit", "-m", f"chore: bump version to {version}"])

        # Create and push tag
        run_command(["git", "tag", "-a", tag, "-m", f"Release {version}"])
        run_command(["git", "push", "origin", "main"])
        run_command(["git", "push", "origin", tag])
        print(f"✅ Created and pushed tag {tag}")
    else:
        print(f"🔍 DRY RUN: Would create and push tag {tag}")


def main():
    parser = argparse.ArgumentParser(description="Release script for Pikapika")
    parser.add_argument(
        "bump_type", choices=["patch", "minor", "major"], help="Type of version bump"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing",
    )
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-lint", action="store_true", help="Skip linting checks")

    args = parser.parse_args()

    print("🚀 Starting release process...")

    # Get current version
    current_version = get_current_version()
    print(f"📋 Current version: {current_version}")

    # Calculate new version
    new_version = bump_version(current_version, args.bump_type)
    print(f"📈 New version: {new_version}")

    if not args.dry_run:
        # Pre-release checks
        check_git_status()

        if not args.skip_tests:
            check_tests_pass()

        if not args.skip_lint:
            check_linting()

        # Update version
        update_version(new_version)

        # Build package
        build_package()

        # Create and push tag (this will trigger GitHub Actions)
        create_and_push_tag(new_version, args.dry_run)

        print(f"🎉 Release {new_version} initiated!")
        print("📦 GitHub Actions will now:")
        print("   1. Run tests")
        print("   2. Build package")
        print("   3. Publish to TestPyPI")
        print("   4. Verify TestPyPI installation")
        print("   5. Publish to PyPI")
        print("   6. Create GitHub Release")
    else:
        print("🔍 DRY RUN MODE - No changes made")
        print(f"   Would bump version: {current_version} → {new_version}")
        print(f"   Would create tag: v{new_version}")
        print("   Would trigger GitHub Actions release workflow")


if __name__ == "__main__":
    main()
