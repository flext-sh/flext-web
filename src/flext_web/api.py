"""FLEXT Web API - REST endpoints for FlexCore management."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from flask import Flask, render_template_string, request
from flext_core import FlextLoggerFactory, FlextLoggerName

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from .simple_web import (
    create_error_response,
    create_response,
    create_success_response,
    validate_request_data,
)
from .web_interface import FlextCoreManager

logger_factory = FlextLoggerFactory()
logger = logger_factory.create_logger(FlextLoggerName(__name__))


class FlextWebAPI:
    """FLEXT Web API for FlexCore management."""

    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.flexcore_manager = FlextCoreManager()
        self.logger = logger_factory.create_logger(FlextLoggerName(__name__))
        self._register_routes()

    def _register_routes(self) -> None:
        """Register all API routes."""
        # Dashboard routes
        self.app.route("/")(self.dashboard)
        self.app.route("/api/v1/flexcore/dashboard")(self.get_dashboard_data)

        # Cluster management routes
        self.app.route("/api/v1/flexcore/clusters", methods=["GET"])(self.list_clusters)
        self.app.route("/api/v1/flexcore/clusters", methods=["POST"])(
            self.create_cluster,
        )
        self.app.route("/api/v1/flexcore/clusters/<cluster_id>", methods=["GET"])(
            self.get_cluster,
        )
        self.app.route(
            "/api/v1/flexcore/clusters/<cluster_id>/status",
            methods=["PUT"],
        )(self.update_cluster_status)

        # Plugin management routes
        self.app.route("/api/v1/flexcore/plugins", methods=["GET"])(self.list_plugins)
        self.app.route("/api/v1/flexcore/plugins", methods=["POST"])(
            self.register_plugin,
        )
        self.app.route("/api/v1/flexcore/plugins/<plugin_id>", methods=["GET"])(
            self.get_plugin,
        )

        # Job management routes
        self.app.route("/api/v1/flexcore/jobs/meltano", methods=["POST"])(
            self.create_meltano_job,
        )
        self.app.route("/api/v1/flexcore/jobs/ray", methods=["POST"])(
            self.create_ray_job,
        )
        self.app.route("/api/v1/flexcore/jobs/<job_id>", methods=["GET"])(
            self.get_job_status,
        )
        self.app.route("/api/v1/flexcore/jobs/<job_id>/execute", methods=["POST"])(
            self.execute_job,
        )

        # Local instance routes
        self.app.route("/api/v1/flexcore/local/start", methods=["POST"])(
            self.start_local_instance,
        )
        self.app.route("/api/v1/flexcore/local/stop", methods=["POST"])(
            self.stop_local_instance,
        )
        self.app.route("/api/v1/flexcore/local/list", methods=["GET"])(
            self.list_local_instances,
        )

        # Health check
        self.app.route("/health")(self.health_check)

    def dashboard(self) -> str:
        """Serve the main dashboard."""
        try:
            template_path = Path(__file__).parent / "templates" / "dashboard.html"
            with open(template_path, encoding="utf-8") as f:
                template_content = f.read()

            return render_template_string(template_content)
        except Exception as e:
            self.logger.exception("Failed to load dashboard template")
            return f"<h1>FLEXT Dashboard Error</h1><p>Failed to load dashboard: {e}</p>"

    def get_dashboard_data(self) -> dict[str, Any]:
        """Get complete dashboard data with DI service integration."""
        try:
            # Get basic dashboard data
            result = self.flexcore_manager.get_dashboard_data()

            if result.success and result.data:
                dashboard_data = result.data

                # Enrich with FLEXT service health check
                try:
                    from .infrastructure.flext_service_adapter import get_flext_services

                    services = get_flext_services()
                    health_result = services.health_check()

                    if health_result.success and health_result.data:
                        dashboard_data["flext_service"] = {
                            "status": "healthy",
                            "version": health_result.data["version"],
                            "services_available": health_result.data["services"],
                        }
                    else:
                        dashboard_data["flext_service"] = {
                            "status": "unavailable",
                            "error": health_result.error or "Health check failed",
                        }
                except Exception as service_error:
                    dashboard_data["flext_service"] = {
                        "status": "error",
                        "error": str(service_error),
                    }

                return create_response(dashboard_data)
            return create_error_response(result.error or "Unknown error", 500)

        except Exception as e:
            self.logger.exception("Failed to get dashboard data")
            return create_error_response(f"Failed to get dashboard data: {e}", 500)

    def list_clusters(self) -> dict[str, Any]:
        """List all FlexCore clusters."""
        try:
            result = self.flexcore_manager.list_clusters()

            if result.success:
                return create_response(result.data)
            return create_error_response(result.error or "Unknown error", 500)

        except Exception as e:
            self.logger.exception("Failed to list clusters")
            return create_error_response(f"Failed to list clusters: {e}", 500)

    def create_cluster(self) -> dict[str, Any]:
        """Create a new FlexCore cluster."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            # Validate required fields
            validation_result = validate_request_data(data, ["name", "endpoint"])
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            # Generate cluster ID
            cluster_id = str(uuid.uuid4())

            result = self.flexcore_manager.register_cluster(
                cluster_id=cluster_id,
                name=data["name"],
                endpoint=data["endpoint"],
            )

            if result.success and result.data:
                self.logger.info(
                    f"FlexCore cluster created: {data['name']} ({cluster_id})",
                )
                return create_response(result.data.to_dict(), 201)
            return create_error_response(result.error or "Unknown error", 400)

        except Exception as e:
            self.logger.exception("Failed to create cluster")
            return create_error_response(f"Failed to create cluster: {e}", 500)

    def get_cluster(self, cluster_id: str) -> dict[str, Any]:
        """Get cluster information."""
        try:
            result = self.flexcore_manager.get_cluster_info(cluster_id)

            if result.success:
                return create_response(result.data)
            return create_error_response(result.error or "Unknown error", 404)

        except Exception as e:
            self.logger.exception(f"Failed to get cluster {cluster_id}")
            return create_error_response(f"Failed to get cluster: {e}", 500)

    def update_cluster_status(self, cluster_id: str) -> dict[str, Any]:
        """Update cluster status."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            validation_result = validate_request_data(data, ["status"])
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            result = self.flexcore_manager.update_cluster_status(
                cluster_id,
                data["status"],
            )

            if result.success:
                return create_response({"status": "updated"})
            return create_error_response(result.error or "Unknown error", 404)

        except Exception as e:
            self.logger.exception(f"Failed to update cluster status {cluster_id}")
            return create_error_response(f"Failed to update cluster status: {e}", 500)

    def list_plugins(self) -> dict[str, Any]:
        """List all registered plugins."""
        try:
            # Get all plugins from registry
            plugins = list(self.flexcore_manager.plugin_registry.plugins.values())
            return create_response(plugins)

        except Exception as e:
            self.logger.exception("Failed to list plugins")
            return create_error_response(f"Failed to list plugins: {e}", 500)

    def register_plugin(self) -> dict[str, Any]:
        """Register a new plugin."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            validation_result = validate_request_data(
                data,
                ["name", "version", "type", "cluster_id"],
            )
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            # Generate plugin ID
            plugin_id = str(uuid.uuid4())

            result = self.flexcore_manager.register_plugin(
                plugin_id=plugin_id,
                name=data["name"],
                version=data["version"],
                plugin_type=data["type"],
                cluster_id=data["cluster_id"],
                config=data.get("config"),
            )

            if result.success:
                self.logger.info(
                    f"Plugin registered: {data['name']} v{data['version']} ({plugin_id})",
                )
                return create_response(
                    {"plugin_id": plugin_id, "status": "registered"},
                    201,
                )
            return create_error_response(result.error or "Unknown error", 400)

        except Exception as e:
            self.logger.exception("Failed to register plugin")
            return create_error_response(f"Failed to register plugin: {e}", 500)

    def get_plugin(self, plugin_id: str) -> dict[str, Any]:
        """Get plugin information."""
        try:
            if plugin_id not in self.flexcore_manager.plugin_registry.plugins:
                return create_error_response("Plugin not found", 404)

            plugin_data = self.flexcore_manager.plugin_registry.plugins[plugin_id]
            return create_response(plugin_data)

        except Exception as e:
            self.logger.exception(f"Failed to get plugin {plugin_id}")
            return create_error_response(f"Failed to get plugin: {e}", 500)

    def create_meltano_job(self) -> dict[str, Any]:
        """Create a Meltano job."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            validation_result = validate_request_data(
                data,
                ["cluster_id", "project_path", "command"],
            )
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            # Generate job ID
            job_id = str(uuid.uuid4())

            result = self.flexcore_manager.create_meltano_job(
                job_id=job_id,
                cluster_id=data["cluster_id"],
                project_path=data["project_path"],
                command=data["command"],
                environment=data.get("environment"),
            )

            if result.success:
                self.logger.info(f"Meltano job created: {job_id}")
                return create_response(result.data, 201)
            return create_error_response(result.error or "Unknown error", 400)

        except Exception as e:
            self.logger.exception("Failed to create Meltano job")
            return create_error_response(f"Failed to create Meltano job: {e}", 500)

    def create_ray_job(self) -> dict[str, Any]:
        """Create a Ray job."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            validation_result = validate_request_data(
                data,
                ["cluster_id", "script_path"],
            )
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            # Generate job ID
            job_id = str(uuid.uuid4())

            result = self.flexcore_manager.create_ray_job(
                job_id=job_id,
                cluster_id=data["cluster_id"],
                script_path=data["script_path"],
                runtime_env=data.get("runtime_env"),
                resources=data.get("resources"),
            )

            if result.success:
                self.logger.info(f"Ray job created: {job_id}")
                return create_response(result.data, 201)
            return create_error_response(
                result.error or "Unknown error", 400,
            )

        except Exception as e:
            self.logger.exception("Failed to create Ray job")
            return create_error_response(f"Failed to create Ray job: {e}", 500)

    def get_job_status(self, job_id: str) -> dict[str, Any]:
        """Get job status."""
        try:
            result = self.flexcore_manager.job_executor.get_job_status(job_id)

            if result.success:
                return create_response(result.data)
            return create_error_response(result.error or "Unknown error", 404)

        except Exception as e:
            self.logger.exception(f"Failed to get job status {job_id}")
            return create_error_response(f"Failed to get job status: {e}", 500)

    def execute_job(self, job_id: str) -> dict[str, Any]:
        """Execute a job."""
        try:
            result = self.flexcore_manager.execute_job(job_id)

            if result.success:
                self.logger.info(f"Job executed: {job_id}")
                return create_response(result.data)
            return create_error_response(result.error or "Unknown error", 400)

        except Exception as e:
            self.logger.exception(f"Failed to execute job {job_id}")
            return create_error_response(f"Failed to execute job: {e}", 500)

    def health_check(self) -> dict[str, Any]:
        """Health check endpoint."""
        return create_response(
            {
                "status": "healthy",
                "service": "FLEXT FlexCore Management API",
                "version": "1.0.0",
                "clusters": len(self.flexcore_manager.clusters),
                "plugins": len(self.flexcore_manager.plugin_registry.plugins),
                "jobs": len(self.flexcore_manager.job_executor.jobs),
            },
        )

    def start_local_instance(self) -> dict[str, Any]:
        """Start local FlexCore instance."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            validation_result = validate_request_data(data, ["instance_name"])
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            instance_name = data["instance_name"]
            port = data.get("port", 8080)
            config = data.get("config", {})

            result = self.flexcore_manager.start_local_instance(
                instance_name,
                port,
                config,
            )

            if result.success:
                return create_success_response(
                    result.data,
                    "Local instance started successfully",
                )
            return create_error_response(result.error or "Unknown error", 500)

        except Exception as e:
            logger.exception(f"Failed to start local instance: {e}")
            return create_error_response("Failed to start local instance", 500)

    def stop_local_instance(self) -> dict[str, Any]:
        """Stop local FlexCore instance."""
        try:
            data = request.get_json()
            if not data:
                return create_error_response("Request body is required", 400)

            validation_result = validate_request_data(data, ["instance_name"])
            if not validation_result.success:
                return create_error_response(validation_result.error or "Validation failed", 400)

            instance_name = data["instance_name"]
            result = self.flexcore_manager.stop_local_instance(instance_name)

            if result.success:
                return create_success_response(
                    {"stopped": True},
                    "Local instance stopped successfully",
                )
            return create_error_response(result.error or "Unknown error", 500)

        except Exception as e:
            logger.exception(f"Failed to stop local instance: {e}")
            return create_error_response("Failed to stop local instance", 500)

    def list_local_instances(self) -> dict[str, Any]:
        """List running local FlexCore instances."""
        try:
            result = self.flexcore_manager.list_local_instances()

            if result.success:
                return create_success_response(
                    result.data,
                    "Local instances retrieved successfully",
                )
            return create_error_response(result.error or "Unknown error", 500)

        except Exception as e:
            logger.exception(f"Failed to list local instances: {e}")
            return create_error_response("Failed to list local instances", 500)

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
        """Run the Flask web server."""
        self.logger.info(f"Starting FLEXT Web API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_app() -> Flask:
    """Create and configure Flask app."""
    web_api = FlextWebAPI()
    return web_api.app


# For standalone execution
if __name__ == "__main__":
    web_api = FlextWebAPI()
    web_api.run(debug=True)
