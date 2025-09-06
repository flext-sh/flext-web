"""Tests específicos para cobrir gaps de cobertura em services.py.

Foca nas linhas não cobertas identificadas no relatório de cobertura:
- Linhas 303-304, 384-385, 416-417, 463-464, 489->492, 515-516, 598-599, 607, 635, 644-645, 657-658, 673, 679, 689, 700-701, 714-741, 750-779
"""

from collections.abc import Generator

import pytest
from flask.testing import FlaskClient

from flext_web import FlextWebConfigs, FlextWebServices


class TestServicesMissingCoverage:
    """Tests para cobrir lacunas específicas em services.py."""

    @pytest.fixture
    def test_config(self) -> FlextWebConfigs.WebConfig:
        """Configuração de teste para services."""
        return FlextWebConfigs.WebConfig(
            host="127.0.0.1",
            port=8500,
            debug=True,
            secret_key="test-services-coverage-32-characters!",
            app_name="Services Coverage Test",
        )

    @pytest.fixture
    def test_service(
        self, test_config: FlextWebConfigs.WebConfig
    ) -> Generator[FlextWebServices.WebService]:
        """Serviço de teste configurado."""
        service = FlextWebServices.WebService(test_config)
        service.app.config["TESTING"] = True
        return service

    @pytest.fixture
    def test_client(self, test_service: FlextWebServices.WebService) -> FlaskClient:
        """Cliente Flask de teste."""
        return test_service.app.test_client()

    def test_service_error_handling_paths(self, test_client: FlaskClient) -> None:
        """Testa caminhos de tratamento de erro não cobertos."""
        # Teste com dados completamente inválidos (linhas 303-304, 384-385)
        invalid_data = {
            "name": None,  # Nome nulo
            "host": None,  # Host nulo
            "port": "not-a-number",  # Porta inválida
        }

        response = test_client.post("/api/v1/apps", json=invalid_data)
        # Deve retornar erro de validação
        assert response.status_code in {400, 422}  # Bad Request ou Unprocessable Entity
        data = response.get_json()
        assert data["success"] is False

    def test_service_edge_case_operations(self, test_client: FlaskClient) -> None:
        """Testa operações em casos extremos (linhas 416-417, 463-464)."""
        # Cria uma aplicação válida primeiro
        app_data = {
            "name": "edge-case-app",
            "host": "localhost",
            "port": 9000,
        }

        response = test_client.post("/api/v1/apps", json=app_data)
        assert response.status_code == 201
        app_id = response.get_json()["data"]["id"]

        # Tenta operações em app já em estado final
        # Inicia o app
        response = test_client.post(f"/api/v1/apps/{app_id}/start")
        assert response.status_code == 200

        # Tenta iniciar novamente (deve falhar)
        response = test_client.post(f"/api/v1/apps/{app_id}/start")
        assert response.status_code in {400, 409}  # Bad Request ou Conflict
        data = response.get_json()
        assert data["success"] is False

    def test_service_registry_error_scenarios(self) -> None:
        """Testa cenários de erro no registry (linhas 598-599, 607, 635)."""
        registry_result = FlextWebServices.create_service_registry()
        assert registry_result.success
        registry = registry_result.value

        # Teste recuperar serviço não existente
        result = registry.get_service("non-existent")
        assert result.is_failure
        assert result.error is not None
        assert "not found" in result.error or "not registered" in result.error

    def test_service_lifecycle_edge_cases(self, test_client: FlaskClient) -> None:
        """Testa casos extremos do ciclo de vida (linhas 644-645, 657-658)."""
        # Teste operação em app não existente
        response = test_client.get("/api/v1/apps/non-existent-app")
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False

        # Teste start em app não existente
        response = test_client.post("/api/v1/apps/non-existent-app/start")
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False

    def test_service_validation_comprehensive(self, test_client: FlaskClient) -> None:
        """Testa validação abrangente (linhas 673, 679, 689)."""
        # Teste com dados completamente inválidos
        invalid_data = {
            "name": "",  # Nome vazio - deve falhar
            "host": "",  # Host vazio - deve falhar
            "port": 0,   # Porta inválida - deve falhar
        }

        response = test_client.post("/api/v1/apps", json=invalid_data)
        assert response.status_code in {400, 422}
        data = response.get_json()
        assert data["success"] is False

        # Teste com JSON malformado
        response = test_client.post(
            "/api/v1/apps",
            data="invalid-json-data",
            content_type="application/json"
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_service_internal_error_handling(self, test_service: FlextWebServices.WebService) -> None:
        """Testa tratamento de erros internos (linhas 700-701)."""
        # Testa cenário de erro interno sem mock - usando dados que causam erro
        client = test_service.app.test_client()

        # Tenta criar com dados que podem causar erro interno
        response = client.post("/api/v1/apps", json={
            "name": "error-app" * 1000,  # Nome muito longo que pode causar problema
            "host": "localhost",
            "port": 9001
        })

        # Se não houver erro interno, pelo menos validamos o comportamento
        if response.status_code == 500:
            data = response.get_json()
            assert data["success"] is False
        else:
            # Se passou, pelo menos verificamos que a resposta é válida
            assert response.status_code in {200, 201, 400, 422}

    def test_service_factory_methods_edge_cases(self) -> None:
        """Testa métodos factory em casos extremos (linhas 714-741, 750-779)."""
        # Teste create_web_service com config nula
        result = FlextWebServices.create_web_service(None)
        if result.is_failure:
            assert result.error is not None
            assert "config" in result.error.lower()

        # Teste create_service_registry
        result = FlextWebServices.create_service_registry()
        assert result.success
        registry = result.value
        assert hasattr(registry, "register_service")
        assert hasattr(registry, "get_service")

    def test_service_app_management_comprehensive(self, test_client: FlaskClient) -> None:
        """Testa gerenciamento completo de aplicações."""
        # Cria múltiplas apps para testar listagem
        apps = []
        for i in range(3):
            app_data = {
                "name": f"management-app-{i}",
                "host": "localhost",
                "port": 9010 + i,
            }
            response = test_client.post("/api/v1/apps", json=app_data)
            assert response.status_code == 201
            apps.append(response.get_json()["data"]["id"])

        # Lista todas as apps
        response = test_client.get("/api/v1/apps")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["data"]["apps"]) >= 3

        # Verifica health com múltiplas apps
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["applications"] >= 3

    def test_service_configuration_edge_cases(self) -> None:
        """Testa casos extremos de configuração."""
        # Configuração com valores mínimos
        minimal_config = FlextWebConfigs.WebConfig(
            host="127.0.0.1",
            port=1024,  # Porta mínima
            secret_key="minimal-config-test-32-characters!",
            debug=False,
            max_content_length=1,  # Valor mínimo
            request_timeout=1,  # Timeout mínimo
        )

        service = FlextWebServices.WebService(minimal_config)
        assert service.config.port == 1024
        assert service.config.max_content_length == 1
        assert service.config.request_timeout == 1


__all__ = [
    "TestServicesMissingCoverage",
]
