"""FLEXT Web Interface - FlexCore Runtime Container Management."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from flext_core import FlextLoggerFactory, FlextLoggerName, FlextResult

logger_factory = FlextLoggerFactory()
logger = logger_factory.create_logger(FlextLoggerName(__name__))


class FlextCoreCluster:
    """FlexCore cluster representation."""

    def __init__(
        self,
        cluster_id: str,
        name: str,
        endpoint: str,
        status: str = "unknown",
        nodes: list[dict[str, Any]] | None = None,
        plugins: list[dict[str, Any]] | None = None,
    ) -> None:
        self.cluster_id = cluster_id
        self.name = name
        self.endpoint = endpoint
        self.status = status
        self.nodes = nodes or []
        self.plugins = plugins or []
        self.created_at = datetime.now()
        self.last_heartbeat: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "endpoint": self.endpoint,
            "status": self.status,
            "nodes": self.nodes,
            "plugins": self.plugins,
            "created_at": self.created_at.isoformat(),
            "last_heartbeat": (
                self.last_heartbeat.isoformat() if self.last_heartbeat else None
            ),
            "node_count": len(self.nodes),
            "plugin_count": len(self.plugins),
        }


class FlextPluginRegistry:
    """Plugin registry for FlexCore clusters."""

    def __init__(self) -> None:
        self.plugins: dict[str, dict[str, Any]] = {}
        logger_factory = FlextLoggerFactory()
        self.logger = logger_factory.create_logger(FlextLoggerName(__name__))

    def register_plugin(
        self,
        plugin_id: str,
        name: str,
        version: str,
        plugin_type: str,
        cluster_id: str,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[bool]:
        """Register a plugin with a FlexCore cluster."""
        try:
            plugin_info = {
                "plugin_id": plugin_id,
                "name": name,
                "version": version,
                "type": plugin_type,
                "cluster_id": cluster_id,
                "config": config or {},
                "status": "registered",
                "registered_at": datetime.now().isoformat(),
                "last_used": None,
                "execution_count": 0,
            }

            self.plugins[plugin_id] = plugin_info
            self.logger.info(
                f"Plugin registered: {name} v{version} on cluster {cluster_id}",
            )

            return FlextResult.ok(True)

        except Exception as e:
            error_msg = f"Failed to register plugin {plugin_id}: {e}"
            self.logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def get_plugins_by_cluster(
        self,
        cluster_id: str,
    ) -> FlextResult[list[dict[str, Any]]]:
        """Get all plugins for a specific cluster."""
        try:
            cluster_plugins = [
                plugin
                for plugin in self.plugins.values()
                if plugin["cluster_id"] == cluster_id
            ]
            return FlextResult.ok(cluster_plugins)
        except Exception as e:
            return FlextResult.fail(
                f"Failed to get plugins for cluster {cluster_id}: {e}",
            )

    def get_plugins_by_type(
        self,
        plugin_type: str,
    ) -> FlextResult[list[dict[str, Any]]]:
        """Get all plugins of specific type."""
        try:
            typed_plugins = [
                plugin
                for plugin in self.plugins.values()
                if plugin["type"] == plugin_type
            ]
            return FlextResult.ok(typed_plugins)
        except Exception as e:
            return FlextResult.fail(
                f"Failed to get plugins of type {plugin_type}: {e}",
            )


class FlextJobExecutor:
    """Job execution engine for FlexCore clusters."""

    def __init__(self) -> None:
        self.jobs: dict[str, dict[str, Any]] = {}
        logger_factory = FlextLoggerFactory()
        self.logger = logger_factory.create_logger(FlextLoggerName(__name__))

    def create_meltano_job(
        self,
        job_id: str,
        cluster_id: str,
        project_path: str,
        command: str,
        environment: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create a Meltano job."""
        try:
            job: dict[str, Any] = {
                "job_id": job_id,
                "type": "meltano",
                "cluster_id": cluster_id,
                "config": {
                    "project_path": project_path,
                    "command": command,
                    "environment": environment or {},
                },
                "status": "created",
                "created_at": datetime.now().isoformat(),
                "started_at": None,
                "completed_at": None,
                "output": [],
                "error_log": [],
            }

            self.jobs[job_id] = job
            self.logger.info(f"Meltano job created: {job_id} on cluster {cluster_id}")

            return FlextResult.ok(job)

        except Exception as e:
            error_msg = f"Failed to create Meltano job {job_id}: {e}"
            self.logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def create_ray_job(
        self,
        job_id: str,
        cluster_id: str,
        script_path: str,
        runtime_env: dict[str, Any] | None = None,
        resources: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create a Ray job."""
        try:
            job: dict[str, Any] = {
                "job_id": job_id,
                "type": "ray",
                "cluster_id": cluster_id,
                "config": {
                    "script_path": script_path,
                    "runtime_env": runtime_env or {},
                    "resources": resources or {"num_cpus": 1, "num_gpus": 0},
                },
                "status": "created",
                "created_at": datetime.now().isoformat(),
                "started_at": None,
                "completed_at": None,
                "output": [],
                "error_log": [],
            }

            self.jobs[job_id] = job
            self.logger.info(f"Ray job created: {job_id} on cluster {cluster_id}")

            return FlextResult.ok(job)

        except Exception as e:
            error_msg = f"Failed to create Ray job {job_id}: {e}"
            self.logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def execute_job(self, job_id: str) -> FlextResult[dict[str, Any]]:
        """Execute a job via FLEXT service integration."""
        try:
            if job_id not in self.jobs:
                return FlextResult.fail(f"Job {job_id} not found")

            job = self.jobs[job_id]
            job["status"] = "running"
            job["started_at"] = datetime.now().isoformat()

            self.logger.info(
                f"Dispatching {job['type']} job {job_id} to FLEXT service via HTTP",
            )

            # Real implementation: HTTP call to FLEXT service
            flext_endpoint = "http://localhost:8080/api/v1"

            if job["type"] == "meltano":
                result = self._execute_meltano_via_flext(job, flext_endpoint)
            elif job["type"] == "ray":
                result = self._execute_ray_via_flext(job, flext_endpoint)
            else:
                return FlextResult.fail(f"Unknown job type: {job['type']}")

            if result.success:
                job["status"] = "completed"
                job["completed_at"] = datetime.now().isoformat()
                if result.data and "output" in result.data:
                    job["output"].append(result.data["output"])
                return FlextResult.ok(job)
            job["status"] = "failed"
            job["completed_at"] = datetime.now().isoformat()
            job["error_log"].append(result.error or "Unknown error")
            return FlextResult.fail(result.error or "Job execution failed")

        except Exception as e:
            error_msg = f"Failed to execute job {job_id}: {e}"
            self.logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def _execute_meltano_via_flext(
        self,
        job: dict[str, Any],
        endpoint: str,
    ) -> FlextResult[dict[str, Any]]:
        """Execute Meltano job via FLEXT service using real integration."""
        try:
            # Use DI container for FLEXT pipeline service
            from .infrastructure.flext_service_adapter import get_flext_services

            services = get_flext_services()

            # Execute pipeline via FLEXT service
            result = services.pipelines.execute_pipeline(
                name=f"meltano-{job['job_id']}",
                extractor="tap-meltano",
                loader="target-output",
                config=job["config"],
            )

            if result.success:
                return FlextResult.ok(
                    {
                        "output": (result.data or {}).get(
                            "output", "Meltano job completed",
                        ),
                        "execution_time": "completed via FLEXT service + FlexCore runtime",
                        "execution_mode": (result.data or {}).get(
                            "execution_mode",
                            "distributed",
                        ),
                    },
                )
            return result

        except Exception as e:
            return FlextResult.fail(f"FLEXT-FlexCore integration error: {e}")

    def _execute_ray_via_flext(
        self,
        job: dict[str, Any],
        endpoint: str,
    ) -> FlextResult[dict[str, Any]]:
        """Execute Ray job via FLEXT service using real integration."""
        try:
            # Use DI container for FLEXT pipeline service
            from .infrastructure.flext_service_adapter import get_flext_services

            services = get_flext_services()

            # Ray jobs executed via pipeline with Ray runtime environment
            ray_config = {
                "runtime_env": job["config"].get("runtime_env", {}),
                "resources": job["config"].get("resources", {"num_cpus": 1}),
                "script_path": job["config"].get("script_path", ""),
            }

            result = services.pipelines.execute_pipeline(
                name=f"ray-{job['job_id']}",
                extractor="tap-ray",
                loader="target-output",
                config=ray_config,
            )

            if result.success:
                return FlextResult.ok(
                    {
                        "output": (result.data or {}).get(
                            "output", "Ray job completed",
                        ),
                        "execution_time": "completed via FLEXT service + FlexCore runtime",
                        "execution_mode": (result.data or {}).get(
                            "execution_mode",
                            "distributed",
                        ),
                    },
                )
            return result

        except Exception as e:
            return FlextResult.fail(f"Ray execution error: {e}")

    def get_job_status(self, job_id: str) -> FlextResult[dict[str, Any]]:
        """Get job status and details."""
        try:
            if job_id not in self.jobs:
                return FlextResult.fail(f"Job {job_id} not found")

            return FlextResult.ok(self.jobs[job_id])

        except Exception as e:
            return FlextResult.fail(f"Failed to get job status: {e}")


class FlextCoreManager:
    """FlexCore runtime container management integrating with FLEXT service."""

    def __init__(self) -> None:
        self.clusters: dict[str, FlextCoreCluster] = {}
        self.plugin_registry = FlextPluginRegistry()
        self.job_executor = FlextJobExecutor()
        logger_factory = FlextLoggerFactory()
        self.logger = logger_factory.create_logger(FlextLoggerName(__name__))

        # 🚨 ARCHITECTURAL COMPLIANCE: Use DI container for FLEXT services
        from .infrastructure.flext_service_adapter import get_flext_services

        self.flext_services = get_flext_services()

    def register_cluster(
        self,
        cluster_id: str,
        name: str,
        endpoint: str,
    ) -> FlextResult[FlextCoreCluster]:
        """Register a new FlexCore cluster."""
        try:
            cluster = FlextCoreCluster(cluster_id, name, endpoint)
            self.clusters[cluster_id] = cluster

            self.logger.info(f"FlexCore cluster registered: {name} ({cluster_id})")
            return FlextResult.ok(cluster)

        except Exception as e:
            error_msg = f"Failed to register cluster {cluster_id}: {e}"
            self.logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def get_cluster_info(self, cluster_id: str) -> FlextResult[dict[str, Any]]:
        """Get cluster information."""
        try:
            if cluster_id not in self.clusters:
                return FlextResult.fail(f"Cluster {cluster_id} not found")

            cluster = self.clusters[cluster_id]
            return FlextResult.ok(cluster.to_dict())

        except Exception as e:
            return FlextResult.fail(f"Failed to get cluster info: {e}")

    def list_clusters(self) -> FlextResult[list[dict[str, Any]]]:
        """List all registered clusters."""
        try:
            clusters_data = [cluster.to_dict() for cluster in self.clusters.values()]
            return FlextResult.ok(clusters_data)
        except Exception as e:
            return FlextResult.fail(f"Failed to list clusters: {e}")

    def update_cluster_status(
        self,
        cluster_id: str,
        status: str,
    ) -> FlextResult[bool]:
        """Update cluster status."""
        try:
            if cluster_id not in self.clusters:
                return FlextResult.fail(f"Cluster {cluster_id} not found")

            cluster = self.clusters[cluster_id]
            cluster.status = status
            cluster.last_heartbeat = datetime.now()

            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Failed to update cluster status: {e}")

    def register_plugin(
        self,
        plugin_id: str,
        name: str,
        version: str,
        plugin_type: str,
        cluster_id: str,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[bool]:
        """Register a plugin with cluster."""
        return self.plugin_registry.register_plugin(
            plugin_id,
            name,
            version,
            plugin_type,
            cluster_id,
            config,
        )

    def create_meltano_job(
        self,
        job_id: str,
        cluster_id: str,
        project_path: str,
        command: str,
        environment: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create Meltano job."""
        return self.job_executor.create_meltano_job(
            job_id,
            cluster_id,
            project_path,
            command,
            environment,
        )

    def create_ray_job(
        self,
        job_id: str,
        cluster_id: str,
        script_path: str,
        runtime_env: dict[str, Any] | None = None,
        resources: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create Ray job."""
        return self.job_executor.create_ray_job(
            job_id,
            cluster_id,
            script_path,
            runtime_env,
            resources,
        )

    def execute_job(self, job_id: str) -> FlextResult[dict[str, Any]]:
        """Execute job."""
        return self.job_executor.execute_job(job_id)

    def get_dashboard_data(self) -> FlextResult[dict[str, Any]]:
        """Get complete dashboard data."""
        try:
            clusters_result = self.list_clusters()
            if not clusters_result.success:
                return FlextResult.fail("Failed to get clusters")

            # Get plugin statistics
            plugin_stats: dict[str, Any] = {
                "total_plugins": len(self.plugin_registry.plugins),
                "plugins_by_type": {},
                "plugins_by_cluster": {},
            }

            for plugin in self.plugin_registry.plugins.values():
                plugin_type = plugin["type"]
                cluster_id = plugin["cluster_id"]

                plugin_stats["plugins_by_type"][plugin_type] = (
                    plugin_stats["plugins_by_type"].get(plugin_type, 0) + 1
                )
                plugin_stats["plugins_by_cluster"][cluster_id] = (
                    plugin_stats["plugins_by_cluster"].get(cluster_id, 0) + 1
                )

            # Get job statistics
            job_stats: dict[str, Any] = {
                "total_jobs": len(self.job_executor.jobs),
                "jobs_by_status": {},
                "jobs_by_type": {},
            }

            for job in self.job_executor.jobs.values():
                job_status = job["status"]
                job_type = job["type"]

                job_stats["jobs_by_status"][job_status] = (
                    job_stats["jobs_by_status"].get(job_status, 0) + 1
                )
                job_stats["jobs_by_type"][job_type] = (
                    job_stats["jobs_by_type"].get(job_type, 0) + 1
                )

            dashboard_data = {
                "clusters": clusters_result.data,
                "cluster_count": len(clusters_result.data or []),
                "plugin_stats": plugin_stats,
                "job_stats": job_stats,
                "timestamp": datetime.now().isoformat(),
            }

            return FlextResult.ok(dashboard_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to get dashboard data: {e}")

    def start_local_instance(
        self,
        instance_name: str,
        port: int = 8080,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Start local FlexCore instance."""
        try:
            # Use DI container for FLEXT service calls
            result = self.flext_services.clusters.start_local_instance(
                instance_name,
                port,
                config,
            )

            if result.success:
                # Register as local cluster
                local_cluster_id = f"local-{instance_name}"
                cluster_result = self.register_cluster(
                    local_cluster_id,
                    f"Local-{instance_name}",
                    (result.data or {}).get("endpoint", f"http://localhost:{port}"),
                )

                if cluster_result.success:
                    # Update cluster with local instance info
                    cluster = self.clusters[local_cluster_id]
                    cluster.status = "running"
                    cluster.nodes = [
                        {
                            "id": f"local-node-{instance_name}",
                            "type": "local",
                            "status": "running",
                            "pid": (result.data or {}).get("pid"),
                            "port": port,
                        },
                    ]

                    return FlextResult.ok(
                        {
                            "cluster_id": local_cluster_id,
                            "instance_data": result.data,
                            "cluster_registered": True,
                        },
                    )

            return result

        except Exception as e:
            return FlextResult.fail(f"Failed to start local instance: {e}")

    def stop_local_instance(self, instance_name: str) -> FlextResult[bool]:
        """Stop local FlexCore instance."""
        try:
            # Use DI container for FLEXT service calls
            result = self.flext_services.clusters.stop_instance(instance_name)

            if result.success:
                # Update cluster status
                local_cluster_id = f"local-{instance_name}"
                if local_cluster_id in self.clusters:
                    self.clusters[local_cluster_id].status = "stopped"
                    self.clusters[local_cluster_id].nodes = []

            return result

        except Exception as e:
            return FlextResult.fail(f"Failed to stop local instance: {e}")

    def list_local_instances(self) -> FlextResult[list[dict[str, Any]]]:
        """List running local FlexCore instances."""
        return self.flext_services.clusters.list_instances()
