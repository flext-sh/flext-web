"""FLEXT Service Adapter - DI Container Pattern for Service Abstraction.

This adapter abstracts all FLEXT service interactions through DI container,
eliminating direct coupling between the web interface and FLEXT implementation.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from flext_core import FlextLoggerFactory, FlextLoggerName, FlextResult

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container

logger_factory = FlextLoggerFactory()
logger = logger_factory.create_logger(FlextLoggerName(__name__))


class FlextServiceAdapter:
    """Service adapter for FLEXT binary interactions through DI pattern."""

    def __init__(self) -> None:
        self.flext_binary = Path("/home/marlonsc/flext/cmd/flext/flext")
        self.config_file = Path("/home/marlonsc/flext/config.yaml")
        self.logger_factory = FlextLoggerFactory()
        self.logger = self.logger_factory.create_logger(FlextLoggerName(__name__))

    def execute_command(
        self,
        command: list[str],
        timeout: int = 300,
        cwd: Path | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Execute FLEXT command with standardized result handling."""
        try:
            if not self.flext_binary.exists():
                return FlextResult.fail("FLEXT service binary not found")

            full_command = [str(self.flext_binary), *command]

            if self.config_file.exists() and "-config" not in command:
                full_command.extend(["-config", str(self.config_file)])

            self.logger.info(f"Executing FLEXT command: {' '.join(command)}")

            result = subprocess.run(
                full_command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or self.flext_binary.parent.parent,
            )

            if result.returncode == 0:
                return FlextResult.ok(
                    {"status": "success", "output": result.stdout, "command": command},
                )

            error_msg = f"FLEXT command failed: {result.stderr}"
            self.logger.error(error_msg)
            return FlextResult.fail(error_msg)

        except subprocess.TimeoutExpired:
            return FlextResult.fail(f"Command timed out: {' '.join(command)}")
        except Exception as e:
            error_msg = f"FLEXT command error: {e}"
            self.logger.exception(error_msg)
            return FlextResult.fail(error_msg)


class FlextPipelineService:
    """Pipeline execution service through FLEXT adapter."""

    def __init__(self, adapter: FlextServiceAdapter) -> None:
        self.adapter = adapter
        self.logger_factory = FlextLoggerFactory()
        self.logger = self.logger_factory.create_logger(FlextLoggerName(__name__))

    def execute_pipeline(
        self,
        name: str,
        extractor: str,
        loader: str,
        config: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Execute data pipeline through FLEXT service."""
        command = [
            "pipeline",
            "execute",
            "--name",
            name,
            "--extractor",
            extractor,
            "--loader",
            loader,
            "--config",
            json.dumps(config),
        ]

        return self.adapter.execute_command(command)

    def list_pipelines(self) -> FlextResult[list[dict[str, Any]]]:
        """List available pipelines."""
        command = ["pipeline", "list", "--json"]
        result = self.adapter.execute_command(command)

        if result.success and result.data:
            try:
                output_data = result.data.get("output", "")
                pipelines = (
                    json.loads(output_data)
                    if output_data.strip()
                    else []
                )
                return FlextResult.ok(pipelines)
            except json.JSONDecodeError:
                return FlextResult.fail("Invalid pipeline list response")
        return FlextResult.fail(result.error or "Pipeline listing failed")


class FlextPluginService:
    """Plugin management service through FLEXT adapter."""

    def __init__(self, adapter: FlextServiceAdapter) -> None:
        self.adapter = adapter
        self.logger_factory = FlextLoggerFactory()
        self.logger = self.logger_factory.create_logger(FlextLoggerName(__name__))

    def register_plugin(
        self,
        name: str,
        version: str,
        plugin_type: str,
        config: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Register plugin with FLEXT service."""
        command = [
            "plugin",
            "register",
            "--name",
            name,
            "--version",
            version,
            "--type",
            plugin_type,
            "--config",
            json.dumps(config),
        ]

        return self.adapter.execute_command(command)

    def list_plugins(self) -> FlextResult[list[dict[str, Any]]]:
        """List registered plugins."""
        command = ["plugin", "list", "--json"]
        result = self.adapter.execute_command(command)

        if result.success and result.data:
            try:
                output_data = result.data.get("output", "")
                plugins = (
                    json.loads(output_data)
                    if output_data.strip()
                    else []
                )
                return FlextResult.ok(plugins)
            except json.JSONDecodeError:
                return FlextResult.fail("Invalid plugin list response")
        return FlextResult.fail(result.error or "Plugin listing failed")


class FlextClusterService:
    """Cluster management service through FLEXT adapter."""

    def __init__(self, adapter: FlextServiceAdapter) -> None:
        self.adapter = adapter
        self.logger_factory = FlextLoggerFactory()
        self.logger = self.logger_factory.create_logger(FlextLoggerName(__name__))

    def start_cluster(
        self,
        name: str,
        nodes: int = 1,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Start FlexCore cluster."""
        command = ["cluster", "start", "--name", name, "--nodes", str(nodes)]

        if config:
            command.extend(["--config", json.dumps(config)])

        return self.adapter.execute_command(command)

    def start_local_instance(
        self,
        name: str,
        port: int = 8080,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Start local FlexCore instance."""
        command = ["instance", "start", "--name", name, "--port", str(port), "--local"]

        if config:
            command.extend(["--config", json.dumps(config)])

        # Start in background for local instances
        result = self.adapter.execute_command(command, timeout=60)

        if result.success and result.data:
            # Add local instance metadata
            instance_data = result.data.copy()
            instance_data.update(
                {
                    "instance_name": name,
                    "port": port,
                    "type": "local",
                    "endpoint": f"http://localhost:{port}",
                },
            )
            return FlextResult.ok(instance_data)
        return result

    def stop_instance(self, name: str) -> FlextResult[bool]:
        """Stop FlexCore instance."""
        command = ["instance", "stop", "--name", name]
        result = self.adapter.execute_command(command, timeout=30)

        return FlextResult.ok(True) if result.success else FlextResult.fail(result.error or "Failed to stop instance")

    def list_instances(self) -> FlextResult[list[dict[str, Any]]]:
        """List running instances."""
        command = ["instance", "list", "--json"]
        result = self.adapter.execute_command(command, timeout=10)

        if result.success and result.data:
            try:
                output_data = result.data.get("output", "")
                instances = (
                    json.loads(output_data)
                    if output_data.strip()
                    else []
                )
                return FlextResult.ok(instances)
            except json.JSONDecodeError:
                return FlextResult.fail("Invalid instance list response")
        return FlextResult.fail(result.error or "Failed to list instances")


class FlextServiceContainer:
    """DI Container for FLEXT services - Single point of service access."""

    def __init__(self) -> None:
        self._adapter = FlextServiceAdapter()
        self._pipeline_service = FlextPipelineService(self._adapter)
        self._plugin_service = FlextPluginService(self._adapter)
        self._cluster_service = FlextClusterService(self._adapter)
        self.logger_factory = FlextLoggerFactory()
        self.logger = self.logger_factory.create_logger(FlextLoggerName(__name__))

    @property
    def pipelines(self) -> FlextPipelineService:
        """Get pipeline service."""
        return self._pipeline_service

    @property
    def plugins(self) -> FlextPluginService:
        """Get plugin service."""
        return self._plugin_service

    @property
    def clusters(self) -> FlextClusterService:
        """Get cluster service."""
        return self._cluster_service

    def health_check(self) -> FlextResult[dict[str, Any]]:
        """Check FLEXT service health."""
        command = ["-version"]
        result = self._adapter.execute_command(command, timeout=10)

        if result.success:
            version_output = (
                result.data.get("output", "unknown") if result.data else "unknown"
            )
            return FlextResult.ok(
                {
                    "status": "healthy",
                    "version": version_output.strip(),
                    "services": ["pipelines", "plugins", "clusters"],
                },
            )
        return FlextResult.fail("FLEXT service not available")


# Global DI container instance
_flext_container = FlextServiceContainer()


def get_flext_services() -> FlextServiceContainer:
    """Get FLEXT services container - DI pattern entry point."""
    return _flext_container
