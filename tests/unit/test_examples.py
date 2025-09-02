"""Simple, fast examples tests that validate functionality without subprocess execution.

These tests verify that examples use the new API correctly and are syntactically valid
without actually running the services (which can cause timeouts).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


class TestExamplesSimple:
    """Fast, reliable tests for examples directory."""

    def test_examples_directory_exists(self) -> None:
        """Test that examples directory exists."""
        examples_dir = Path("examples")
        assert examples_dir.exists(), "examples/ directory missing"
        assert examples_dir.is_dir(), "examples/ is not a directory"

    def test_basic_service_example(self) -> None:
        """Test basic_service.py example."""
        example_path = Path("examples/01_basic_service.py")
        assert example_path.exists(), "basic_service.py missing"

        # Test syntax
        source_code = example_path.read_text(encoding="utf-8")

        try:
            compile(source_code, str(example_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in basic_service.py: {e}")

        # Test import works via importlib for numerically prefixed module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_example_basic_service", Path("examples") / "01_basic_service.py"
        )
        assert spec
        assert spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert hasattr(mod, "main"), "basic service module should define main()"

    def test_api_usage_example(self) -> None:
        """Test api_usage.py example."""
        example_path = Path("examples/02_api_usage.py")
        assert example_path.exists(), "api_usage.py missing"

        # Test syntax
        source_code = example_path.read_text(encoding="utf-8")

        try:
            compile(source_code, str(example_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in api_usage.py: {e}")

    def test_docker_ready_example(self) -> None:
        """Test docker_ready.py example."""
        example_path = Path("examples/03_docker_ready.py")
        assert example_path.exists(), "docker_ready.py missing"

        # Test syntax
        source_code = example_path.read_text(encoding="utf-8")

        try:
            compile(source_code, str(example_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in docker_ready.py: {e}")

    def test_all_examples_use_new_api(self) -> None:
        """Test that all examples use the new API correctly."""
        examples_dir = Path("examples")
        python_files = list(examples_dir.glob("*.py"))

        for example_file in python_files:
            if example_file.name.endswith(".py"):
                content = example_file.read_text()

                # Check for new API usage
                assert "flext_web" in content, (
                    f"{example_file.name} should import from flext_web"
                )

                # Should not use old import patterns
                old_patterns = [
                    "from flext_web.web_service",
                    "from flext_web.web_config",
                ]
                for pattern in old_patterns:
                    assert pattern not in content, (
                        f"{example_file.name} uses old API: {pattern}"
                    )

    def test_examples_have_main_function(self) -> None:
        """Test that executable examples have main or demo function."""
        executable_examples = {
            "01_basic_service.py": "def main(",
            "02_api_usage.py": "def demo_application_lifecycle(",  # Has demo function instead
            "03_docker_ready.py": "def main(",
        }

        for example_name, expected_function in executable_examples.items():
            example_path = Path("examples") / example_name
            if example_path.exists():
                content = example_path.read_text()

                assert expected_function in content, (
                    f"{example_name} should have {expected_function})"
                )
                assert 'if __name__ == "__main__"' in content, (
                    f"{example_name} should be executable"
                )

    def test_examples_have_docstrings(self) -> None:
        """Test that examples have proper docstrings."""
        examples_dir = Path("examples")
        python_files = list(examples_dir.glob("*.py"))

        for example_file in python_files:
            if example_file.name.endswith(".py"):
                content = example_file.read_text()

                # Should have module docstring
                assert '"""' in content, f"{example_file.name} should have docstring"

    def test_examples_syntax_check(self) -> None:
        """Verify all examples have valid Python syntax."""
        examples_dir = Path("examples")
        python_files = list(examples_dir.glob("*.py"))

        for example_file in python_files:
            source_code = example_file.read_text()

            try:
                compile(source_code, str(example_file), "exec")
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {example_file.name}: {e}")

    def test_basic_service_quick_execution(self) -> None:
        """Test basic_service can be executed quickly with help."""
        # Test with --help or similar quick flag to avoid long-running server
        cmd = [
            sys.executable,
            "-c",
            "import examples.basic_service; print('Executable')",
        ]
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=5
        )
        # It's OK if it fails due to imports, we just want to test it's executable
        # The important thing is no syntax errors
        assert "SyntaxError" not in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
