"""Testes funcionais específicos para cobrir lacunas de cobertura em models.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest

from flext_web import FlextWebModels, FlextWebTypes


class TestModelsMissingCoverage:
    """Testes para cobrir lacunas específicas em models.py."""

    def test_webapp_status_error_transitions(self) -> None:
        """Testa transições de status para ERROR não cobertas."""
        app = FlextWebModels.WebApp(
            id="error-test-app",
            name="Error Test App",
            host="127.0.0.1",
            port=8400,
            status=FlextWebModels.WebAppStatus.STARTING,
        )

        # Transição para ERROR (linha 67-70 não coberta)
        app.status = FlextWebModels.WebAppStatus.ERROR
        assert app.status == FlextWebModels.WebAppStatus.ERROR

    def test_webapp_invalid_host_validation(self) -> None:
        """Testa validação de host inválido (linhas 127-128)."""
        with pytest.raises(ValueError, match="Invalid host format"):
            FlextWebModels.WebApp(
                id="invalid-host-test",
                name="Invalid Host Test",
                host="invalid..host..",  # Host inválido
                port=8401,
            )

    def test_webapp_edge_cases_business_rules(self) -> None:
        """Testa regras de negócio não cobertas."""
        # Teste com porta no limite inferior (linha 99-100)
        app = FlextWebModels.WebApp(
            id="port-edge-test",
            name="Port Edge Test",
            host="localhost",
            port=1024,  # Porta mínima válida (>= 1024)
        )
        assert app.port == 1024

        # Teste com porta no limite superior (linha 105-106)
        app_high_port = FlextWebModels.WebApp(
            id="port-high-test",
            name="Port High Test",
            host="localhost",
            port=65535,  # Porta máxima
        )
        assert app_high_port.port == 65535

    def test_webapp_business_rules_validation(self) -> None:
        """Testa validação de regras de negócio não cobertas."""
        # Teste validate_business_rules com nome vazio (linhas 178-179)
        # Use model_construct para contornar validação Pydantic inicial
        app_empty_name = FlextWebModels.WebApp.model_construct(
            id="empty-name-test",
            name="",  # Nome vazio
            host="127.0.0.1",
            port=8402,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        validation_result = app_empty_name.validate_business_rules()
        assert validation_result.is_failure
        assert validation_result.error is not None
        assert "name is required" in validation_result.error

        # Teste validate_business_rules com host vazio (linha 186)
        app_empty_host = FlextWebModels.WebApp.model_construct(
            id="empty-host-test",
            name="Empty Host Test",
            host="",  # Host vazio
            port=8403,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        validation_result = app_empty_host.validate_business_rules()
        assert validation_result.is_failure
        assert validation_result.error is not None
        assert "Host address is required" in validation_result.error

    def test_webapp_serialization_edge_cases(self) -> None:
        """Testa casos extremos de serialização não cobertos."""
        app = FlextWebModels.WebApp(
            id="serialization-test",
            name="Serialization Test",
            host="0.0.0.0",  # Host especial
            port=8405,
            status=FlextWebModels.WebAppStatus.ERROR,  # Status de erro
        )

        # Testa serialização com status ERROR (linhas 235, 239, 244, 246)
        serialized = app.to_dict()
        # Status é um Enum que é serializado como o próprio enum object
        status_value = serialized["status"]
        assert isinstance(status_value, FlextWebModels.WebAppStatus)
        assert status_value == FlextWebModels.WebAppStatus.ERROR
        assert status_value.value == "error"
        assert serialized["host"] == "0.0.0.0"

        # Testa criação de dados com valores edge case (linha 254)
        app_data = FlextWebTypes.AppData(
            id="edge-case-001",
            name="Edge Case App",
            host="::",  # IPv6 localhost
            port=1024,
            status="STARTING",
            is_running=False,
        )
        assert app_data["host"] == "::"

    def test_webapp_status_machine_comprehensive(self) -> None:
        """Testa máquina de estados completa não coberta."""
        app = FlextWebModels.WebApp(
            id="state-machine-test",
            name="State Machine Test",
            host="127.0.0.1",
            port=8406,
        )

        # Ciclo completo de estados não coberto (linha 268)
        states = [
            FlextWebModels.WebAppStatus.STOPPED,
            FlextWebModels.WebAppStatus.STARTING,
            FlextWebModels.WebAppStatus.RUNNING,
            FlextWebModels.WebAppStatus.STOPPING,
            FlextWebModels.WebAppStatus.STOPPED,
            FlextWebModels.WebAppStatus.ERROR,
        ]

        for state in states:
            app.status = state
            assert app.status == state

    def test_webapp_validation_comprehensive(self) -> None:
        """Testa validações abrangentes não cobertas."""
        # Testa validação com IPv6 (linhas 78-79, 83-84)
        ipv6_app = FlextWebModels.WebApp(
            id="ipv6-test",
            name="IPv6 Test",
            host="::1",  # IPv6 localhost
            port=8407,
        )
        assert ipv6_app.host == "::1"

        # Testa validação com hostname complexo (linhas 110-111)
        complex_host_app = FlextWebModels.WebApp(
            id="complex-host-test",
            name="Complex Host Test",
            host="sub.domain.example.com",
            port=8408,
        )
        assert complex_host_app.host == "sub.domain.example.com"
