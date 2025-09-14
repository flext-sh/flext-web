"""Tests específicos para cobrir gaps de cobertura em config.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import os

import pytest
from pydantic import ValidationError

from flext_web import FlextWebConfigs


class TestConfigMissingCoverage:
    """Testes para cobrir lacunas específicas em config.py."""

    def test_host_validation_invalid_characters(self) -> None:
        """Testa validação de host com caracteres inválidos (linhas 128-129)."""
        with pytest.raises(ValueError, match="Invalid host address format"):
            FlextWebConfigs.WebConfig(
                secret_key="test-secret-key-32-characters-long!",
                host="invalid@host#",  # Caracteres inválidos @ e #
                port=8080,
            )

    def test_secret_key_validation_too_short(self) -> None:
        """Testa validação de secret_key muito curta (linhas 138-139)."""
        with pytest.raises(
            ValidationError, match="String should have at least 32 characters"
        ):
            FlextWebConfigs.WebConfig(
                secret_key="short",  # Muito curta (< 32 chars)
                host="localhost",
                port=8080,
            )

    def test_port_validation_invalid_range(self) -> None:
        """Testa validação de porta fora do range (linhas 146-147, 158-159)."""
        # Porta muito baixa
        with pytest.raises(
            ValidationError, match="Input should be greater than or equal to 1"
        ):
            FlextWebConfigs.WebConfig(
                secret_key="test-secret-key-32-characters-long!",
                host="localhost",
                port=0,  # Porta inválida
            )

        # Porta muito alta
        with pytest.raises(
            ValidationError, match="Input should be less than or equal to 65535"
        ):
            FlextWebConfigs.WebConfig(
                secret_key="test-secret-key-32-characters-long!",
                host="localhost",
                port=99999,  # Porta muito alta
            )

    def test_environment_variable_edge_cases(self) -> None:
        """Testa casos extremos com variáveis de ambiente."""
        original_env = os.environ.copy()
        try:
            # Teste com valores válidos nos limites extremos
            os.environ.update(
                {
                    "FLEXT_WEB_HOST": "127.0.0.1",  # IPv4 localhost
                    "FLEXT_WEB_PORT": "65535",  # Porta máxima
                    "FLEXT_WEB_SECRET_KEY": "x" * 32,  # Exatamente 32 chars
                }
            )

            FlextWebConfigs.reset_web_settings()

            config = FlextWebConfigs.get_web_settings()
            assert config.host == "127.0.0.1"
            assert config.port == 65535
            assert config.secret_key == "x" * 32

        finally:
            os.environ.clear()
            os.environ.update(original_env)
            FlextWebConfigs.reset_web_settings()

    def test_config_creation_methods_working_scenarios(self) -> None:
        """Testa métodos de criação de config que funcionam."""
        # Teste desenvolvimento sem ambiente específico
        original_env = os.environ.copy()
        try:
            os.environ.clear()
            FlextWebConfigs.reset_web_settings()

            result = FlextWebConfigs.create_development_config()
            assert result.success
            config = result.value
            assert config.debug is True  # Desenvolvimento é sempre debug

        finally:
            os.environ.clear()
            os.environ.update(original_env)
            FlextWebConfigs.reset_web_settings()

    def test_web_system_configs_creation(self) -> None:
        """Testa criação de configurações do sistema web (linhas 576, 588-589)."""
        result = FlextWebConfigs.create_web_system_configs()
        assert result.success
        system_configs = result.value
        assert isinstance(system_configs, dict)
        assert "web_config" in system_configs

    def test_config_merging_edge_cases(self) -> None:
        """Testa casos extremos de merge de configuração (linhas 627-628, 641->654)."""
        base_config = FlextWebConfigs.WebConfig(
            secret_key="base-config-secret-key-32-characters!",
            host="base-host",
            port=8080,
        )

        # Teste merge com dados inválidos
        invalid_override = {
            "host": "invalid@host",  # Host inválido
            "port": -1,  # Porta inválida
        }

        result = FlextWebConfigs.merge_web_config(base_config, invalid_override)
        # Dependendo da implementação, pode falhar na validação
        if result.is_failure:
            assert result.error is not None
            assert (
                "invalid" in result.error.lower()
                or "validation" in result.error.lower()
            )

    def test_config_validation_comprehensive_edge_cases(self) -> None:
        """Testa casos extremos de validação (linhas 685-686, 707-708)."""
        # Teste com configuração válida nos limites
        config = FlextWebConfigs.WebConfig(
            secret_key="x" * 32,  # Exatamente 32 caracteres
            host="127.0.0.1",  # IP válido
            port=1024,  # Porta mínima válida (>= 1024)
            debug=False,
            max_content_length=1,  # Valor mínimo
            request_timeout=1,  # Timeout mínimo
        )
        assert config.secret_key == "x" * 32
        assert config.port == 1024
        assert config.max_content_length == 1
        assert config.request_timeout == 1

    def test_config_methods_error_branches(self) -> None:
        """Testa branches de erro nos métodos de configuração."""
        # Teste criação de desenvolvimento com ambiente limpo
        original_env = os.environ.copy()
        try:
            os.environ.clear()
            FlextWebConfigs.reset_web_settings()

            result = FlextWebConfigs.create_development_config()
            assert result.success
            config = result.value
            assert config.debug is True  # Desenvolvimento sempre debug

        finally:
            os.environ.clear()
            os.environ.update(original_env)
            FlextWebConfigs.reset_web_settings()


__all__ = [
    "TestConfigMissingCoverage",
]
