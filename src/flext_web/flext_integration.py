"""FLEXT Service Integration - Direct integration with FLEXT Go service and FlexCore."""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Any

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_web.infrastructure.di_container import get_service_result

ServiceResult = get_service_result()

logger = logging.getLogger(__name__)


class FlextServiceIntegration:
    """Direct integration with FLEXT Go service."""

    def __init__(self) -> None:
        self.flext_binary = Path("/home/marlonsc/flext/cmd/flext/flext")
        self.config_file = Path("/home/marlonsc/flext/config.yaml")
        self.logger = logging.getLogger(__name__)

    def check_flext_service(self) -> ServiceResult[dict[str, Any]]:
        """Check if FLEXT service is available."""
        try:
            if not self.flext_binary.exists():
                return ServiceResult.fail("FLEXT service binary not found")

            # Check FLEXT service version
            result = subprocess.run(
                [str(self.flext_binary), "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return ServiceResult.ok(
                    {
                        "available": True,
                        "version": result.stdout.strip(),
                        "binary_path": str(self.flext_binary),
                    }
                )
            return ServiceResult.fail(f"FLEXT service check failed: {result.stderr}")

        except Exception as e:
            return ServiceResult.fail(f"FLEXT service integration error: {e}")

    def execute_pipeline_via_flext(
        self, pipeline_name: str, extractor: str, loader: str, config: dict[str, Any]
    ) -> ServiceResult[dict[str, Any]]:
        """Execute pipeline via FLEXT service."""
        try:
            # Verify FLEXT service is available
            check_result = self.check_flext_service()
            if not check_result.success:
                return check_result

            # Prepare pipeline execution command
            cmd = [
                str(self.flext_binary),
                "pipeline",
                "execute",
                "--name",
                pipeline_name,
                "--extractor",
                extractor,
                "--loader",
                loader,
                "--config",
                json.dumps(config),
            ]

            if self.config_file.exists():
                cmd.extend(["--config-file", str(self.config_file)])

            self.logger.info(f"Executing FLEXT pipeline: {pipeline_name}")

            # Execute via FLEXT service
            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
                cwd=self.flext_binary.parent.parent,  # /home/marlonsc/flext
            )

            if result.returncode == 0:
                return ServiceResult.ok(
                    {
                        "status": "completed",
                        "output": result.stdout,
                        "pipeline": pipeline_name,
                        "extractor": extractor,
                        "loader": loader,
                    }
                )
            error_msg = f"FLEXT pipeline execution failed: {result.stderr}"
            self.logger.error(error_msg)
            return ServiceResult.fail(error_msg)

        except subprocess.TimeoutExpired:
            return ServiceResult.fail(f"Pipeline {pipeline_name} execution timed out")
        except Exception as e:
            error_msg = f"FLEXT integration error: {e}"
            self.logger.exception(error_msg)
            return ServiceResult.fail(error_msg)


class FlexCoreIntegration:
    """Integration with FlexCore runtime container."""

    def __init__(self) -> None:
        self.flexcore_binary = Path("/home/marlonsc/flext/flexcore/flexcore")
        self.config_file = Path("/home/marlonsc/flext/flexcore/config.yaml")
        self.logger = logging.getLogger(__name__)

    def check_flexcore_runtime(self) -> ServiceResult[dict[str, Any]]:
        """Check FlexCore runtime container status."""
        try:
            if not self.flexcore_binary.exists():
                return ServiceResult.fail("FlexCore runtime binary not found")

            # Check FlexCore version
            result = subprocess.run(
                [str(self.flexcore_binary), "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return ServiceResult.ok(
                    {
                        "available": True,
                        "version": result.stdout.strip(),
                        "binary_path": str(self.flexcore_binary),
                        "type": "distributed_event_driven_runtime",
                    }
                )
            return ServiceResult.fail(f"FlexCore check failed: {result.stderr}")

        except Exception as e:
            return ServiceResult.fail(f"FlexCore integration error: {e}")

    def start_flexcore_cluster(
        self, cluster_name: str, node_count: int = 1
    ) -> ServiceResult[dict[str, Any]]:
        """Start FlexCore cluster for distributed execution."""
        try:
            check_result = self.check_flexcore_runtime()
            if not check_result.success:
                return check_result

            cmd = [
                str(self.flexcore_binary),
                "cluster",
                "start",
                "--name",
                cluster_name,
                "--nodes",
                str(node_count),
            ]

            if self.config_file.exists():
                cmd.extend(["--config", str(self.config_file)])

            self.logger.info(
                f"Starting FlexCore cluster: {cluster_name} with {node_count} nodes"
            )

            result = subprocess.run(
                cmd, check=False, capture_output=True, text=True, timeout=60
            )

            if result.returncode == 0:
                return ServiceResult.ok(
                    {
                        "status": "started",
                        "cluster_name": cluster_name,
                        "node_count": node_count,
                        "output": result.stdout,
                    }
                )
            return ServiceResult.fail(f"FlexCore cluster start failed: {result.stderr}")

        except Exception as e:
            return ServiceResult.fail(f"FlexCore cluster error: {e}")

    def start_local_flexcore_instance(
        self, instance_name: str, port: int = 8080, config: dict[str, Any] | None = None
    ) -> ServiceResult[dict[str, Any]]:
        """Start local FlexCore instance for single-node execution."""
        try:
            check_result = self.check_flexcore_runtime()
            if not check_result.success:
                return check_result

            cmd = [
                str(self.flexcore_binary),
                "instance",
                "start",
                "--name",
                instance_name,
                "--port",
                str(port),
                "--local",
            ]

            if config:
                cmd.extend(["--config-json", json.dumps(config)])
            elif self.config_file.exists():
                cmd.extend(["--config", str(self.config_file)])

            self.logger.info(
                f"Starting local FlexCore instance: {instance_name} on port {port}"
            )

            # Start in background
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Give it time to start
            import time

            time.sleep(2)

            if process.poll() is None:  # Still running
                return ServiceResult.ok(
                    {
                        "status": "started",
                        "instance_name": instance_name,
                        "port": port,
                        "pid": process.pid,
                        "endpoint": f"http://localhost:{port}",
                        "type": "local",
                    }
                )

            stdout, stderr = process.communicate()
            return ServiceResult.fail(f"Local FlexCore start failed: {stderr}")

        except Exception as e:
            return ServiceResult.fail(f"Local FlexCore error: {e}")

    def stop_local_flexcore_instance(self, instance_name: str) -> ServiceResult[bool]:
        """Stop local FlexCore instance."""
        try:
            cmd = [
                str(self.flexcore_binary),
                "instance",
                "stop",
                "--name",
                instance_name,
            ]

            result = subprocess.run(
                cmd, check=False, capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                self.logger.info(f"Local FlexCore instance stopped: {instance_name}")
                return ServiceResult.ok(True)
            return ServiceResult.fail(f"Stop failed: {result.stderr}")

        except Exception as e:
            return ServiceResult.fail(f"Stop error: {e}")

    def list_local_instances(self) -> ServiceResult[list[dict[str, Any]]]:
        """List running local FlexCore instances."""
        try:
            cmd = [str(self.flexcore_binary), "instance", "list", "--json"]

            result = subprocess.run(
                cmd, check=False, capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                import json

                instances = json.loads(result.stdout) if result.stdout.strip() else []
                return ServiceResult.ok(instances)
            return ServiceResult.fail(f"List failed: {result.stderr}")

        except Exception as e:
            return ServiceResult.fail(f"List error: {e}")


class FlextFlexCoreIntegration:
    """Unified integration managing FLEXT service within FlexCore runtime."""

    def __init__(self) -> None:
        self.flext_integration = FlextServiceIntegration()
        self.flexcore_integration = FlexCoreIntegration()
        self.logger = logging.getLogger(__name__)

    def get_integration_status(self) -> ServiceResult[dict[str, Any]]:
        """Get comprehensive status of FLEXT + FlexCore integration."""
        try:
            # Check FLEXT service
            flext_status = self.flext_integration.check_flext_service()

            # Check FlexCore runtime
            flexcore_status = self.flexcore_integration.check_flexcore_runtime()

            integration_status = {
                "flext_service": {
                    "available": flext_status.success,
                    "details": (
                        flext_status.data
                        if flext_status.success
                        else flext_status.error_message
                    ),
                },
                "flexcore_runtime": {
                    "available": flexcore_status.success,
                    "details": (
                        flexcore_status.data
                        if flexcore_status.success
                        else flexcore_status.error_message
                    ),
                },
                "integration_ready": flext_status.success and flexcore_status.success,
                "architecture": "FlexCore(runtime) → FLEXT(service) → Python(libraries)",
            }

            return ServiceResult.ok(integration_status)

        except Exception as e:
            return ServiceResult.fail(f"Integration status check failed: {e}")

    def execute_distributed_pipeline(
        self,
        pipeline_name: str,
        extractor: str,
        loader: str,
        config: dict[str, Any],
        cluster_name: str = "web-cluster",
    ) -> ServiceResult[dict[str, Any]]:
        """Execute pipeline in distributed FlexCore environment via FLEXT service."""
        try:
            # Verify integration is ready
            status_result = self.get_integration_status()
            if not status_result.success:
                return status_result

            if not status_result.data["integration_ready"]:
                return ServiceResult.fail("FLEXT + FlexCore integration not ready")

            # Start FlexCore cluster if needed
            cluster_result = self.flexcore_integration.start_flexcore_cluster(
                cluster_name
            )
            if not cluster_result.success:
                self.logger.warning(
                    f"FlexCore cluster start failed: {cluster_result.error_message}"
                )
                # Continue with FLEXT service only

            # Execute pipeline via FLEXT service (which may run within FlexCore)
            pipeline_result = self.flext_integration.execute_pipeline_via_flext(
                pipeline_name, extractor, loader, config
            )

            if pipeline_result.success:
                execution_data = pipeline_result.data.copy()
                execution_data["execution_mode"] = (
                    "distributed" if cluster_result.success else "standalone"
                )
                execution_data["cluster"] = (
                    cluster_name if cluster_result.success else None
                )
                return ServiceResult.ok(execution_data)
            return pipeline_result

        except Exception as e:
            return ServiceResult.fail(f"Distributed pipeline execution failed: {e}")

    def start_local_instance(
        self, instance_name: str, port: int = 8080, config: dict[str, Any] | None = None
    ) -> ServiceResult[dict[str, Any]]:
        """Start local FlexCore instance with FLEXT integration."""
        try:
            # Verify integration components
            status_result = self.get_integration_status()
            if not status_result.success:
                return status_result

            # Start local FlexCore instance
            instance_result = self.flexcore_integration.start_local_flexcore_instance(
                instance_name, port, config
            )

            if instance_result.success:
                instance_data = instance_result.data.copy()
                instance_data["flext_integration"] = True
                instance_data["architecture"] = "Local FlexCore + FLEXT service"
                return ServiceResult.ok(instance_data)
            return instance_result

        except Exception as e:
            return ServiceResult.fail(f"Local instance start failed: {e}")

    def stop_local_instance(self, instance_name: str) -> ServiceResult[bool]:
        """Stop local FlexCore instance."""
        return self.flexcore_integration.stop_local_flexcore_instance(instance_name)

    def list_local_instances(self) -> ServiceResult[list[dict[str, Any]]]:
        """List local FlexCore instances."""
        return self.flexcore_integration.list_local_instances()
