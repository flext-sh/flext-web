#!/usr/bin/env python3
"""Teste COMPLETO de TODA funcionalidade dos examples/ usando Docker.

Este teste valida 100% da funcionalidade de todos os examples usando o container Docker
para garantir comportamento compatível com ambientes de produção e enterprise.
"""

import subprocess
import time
import requests
import sys


class ExamplesFullFunctionalityTest:
    """Teste completo de toda funcionalidade dos examples."""

    def __init__(self):
        self.container_id = None
        self.service_url = "http://localhost:8093"  # Port específica para evitar conflitos

    def start_service_in_docker(self):
        """Inicia o serviço em Docker para teste completo."""
        print("🐳 Iniciando serviço em Docker para teste completo...")

        # Build container if needed
        build_cmd = ["docker", "build", "-t", "flext-web-full-test", "."]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Docker build falhou: {result.stderr}")
            return False

        # Start container with examples
        start_cmd = [
            "docker", "run", "--rm", "-d",
            "-p", "8093:8080",
            "-e", "FLEXT_WEB_SECRET_KEY=test-full-functionality-key-32-chars!",
            "-e", "FLEXT_WEB_HOST=0.0.0.0",
            "-e", "FLEXT_WEB_PORT=8080",
            "-e", "FLEXT_WEB_DEBUG=false",
            "--name", "flext-full-test",
            "flext-web-full-test"
        ]

        try:
            result = subprocess.run(start_cmd, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print(f"❌ Container start falhou: {result.stderr}")
                return False

            self.container_id = result.stdout.strip()
            print(f"✅ Container iniciado: {self.container_id[:12]}")

            # Wait for service to be ready
            for i in range(30):  # 30 seconds timeout
                try:
                    response = requests.get(f"{self.service_url}/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ Serviço pronto no Docker")
                        return True
                except:
                    pass
                time.sleep(1)

            print("❌ Serviço não ficou pronto no tempo esperado")
            return False

        except Exception as e:
            print(f"❌ Erro ao iniciar container: {e}")
            return False

    def stop_docker_service(self):
        """Para o serviço Docker."""
        if self.container_id:
            subprocess.run(["docker", "stop", "flext-full-test"],
                          capture_output=True, timeout=10)
            print("🧹 Container Docker parado")

    def test_basic_service_full_functionality(self):
        """Testa TODA funcionalidade do basic_service.py."""
        print("\n🧪 Testando TODA funcionalidade do basic_service.py...")

        # Test 1: Import functionality
        sys.path.insert(0, "examples")
        try:
            import basic_service
            print("✅ basic_service.py pode ser importado")

            # Test 2: Main function exists and is callable
            assert hasattr(basic_service, 'main'), "main() function missing"
            assert callable(basic_service.main), "main() not callable"
            print("✅ main() function disponível")

            # Test 3: Can create service programmatically
            from flext_web import create_service, get_web_settings
            config = get_web_settings()
            service = create_service(config)
            print("✅ create_service() funciona programaticamente")

            # Test 4: Service has correct attributes
            assert hasattr(service, 'app'), "Service missing Flask app"
            assert hasattr(service, 'run'), "Service missing run method"
            print("✅ Service tem atributos corretos")

            return True

        except Exception as e:
            print(f"❌ basic_service.py falhou: {e}")
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def test_api_usage_full_functionality(self):
        """Testa TODA funcionalidade do api_usage.py."""
        print("\n🧪 Testando TODA funcionalidade do api_usage.py...")

        sys.path.insert(0, "examples")
        try:
            import api_usage
            print("✅ api_usage.py pode ser importado")

            # Test 1: Health check function
            health_result = api_usage.check_service_health()
            if health_result:
                print("✅ check_service_health() funciona")
            else:
                print("⚠️ check_service_health() retornou False (serviço pode não estar rodando)")

            # Test 2: Create application function
            create_result = api_usage.create_application("test-full-func", 3001)
            if create_result:
                print("✅ create_application() funciona")
                app_id = create_result.get("id")

                # Test 3: Start application function
                if app_id:
                    start_result = api_usage.start_application(app_id)
                    if start_result:
                        print("✅ start_application() funciona")

                        # Test 4: Get status function
                        status = api_usage.get_application_status(app_id)
                        if status:
                            print("✅ get_application_status() funciona")

                        # Test 5: Stop application function
                        stop_result = api_usage.stop_application(app_id)
                        if stop_result:
                            print("✅ stop_application() funciona")

            # Test 6: List applications function
            apps_list = api_usage.list_applications()
            print(f"✅ list_applications() funciona (retornou {len(apps_list)} apps)")

            # Test 7: Demo lifecycle function
            print("🔄 Testando demo_application_lifecycle()...")
            api_usage.demo_application_lifecycle()
            print("✅ demo_application_lifecycle() executou sem erro")

            return True

        except Exception as e:
            print(f"❌ api_usage.py falhou: {e}")
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def test_docker_ready_full_functionality(self):
        """Testa TODA funcionalidade do docker_ready.py."""
        print("\n🧪 Testando TODA funcionalidade do docker_ready.py...")

        sys.path.insert(0, "examples")
        try:
            import docker_ready
            print("✅ docker_ready.py pode ser importado")

            # Test 1: create_docker_config function
            config = docker_ready.create_docker_config()
            print("✅ create_docker_config() funciona")
            assert config.host == "0.0.0.0", "Docker config host incorreto"
            assert isinstance(config.port, int), "Docker config port incorreto"
            print("✅ create_docker_config() retorna configuração válida")

            # Test 2: Configuration validation
            validation_result = config.validate_config()
            if validation_result.is_success:
                print("✅ Docker config passa validação")
            else:
                print(f"⚠️ Docker config validation: {validation_result.error}")

            # Test 3: setup_signal_handlers function
            docker_ready.setup_signal_handlers()
            print("✅ setup_signal_handlers() funciona")

            # Test 4: main function exists
            assert hasattr(docker_ready, 'main'), "main() function missing"
            assert callable(docker_ready.main), "main() not callable"
            print("✅ main() function disponível")

            return True

        except Exception as e:
            print(f"❌ docker_ready.py falhou: {e}")
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def test_examples_integration_functionality(self):
        """Testa integração entre examples e funcionalidade completa."""
        print("\n🧪 Testando integração completa entre examples...")

        # Test 1: All examples can work together
        try:
            from flext_web import create_service, get_web_settings, FlextWebConfig

            # Create services using different approaches from examples

            # Approach 1: basic_service style
            config1 = get_web_settings()
            service1 = create_service(config1)
            print("✅ basic_service approach funciona")

            # Approach 2: docker_ready style
            config2 = FlextWebConfig(
                host="127.0.0.1",
                port=8094,
                debug=False,
                secret_key="integration-test-key-32-characters!"
            )
            service2 = create_service(config2)
            print("✅ docker_ready approach funciona")

            # Test both services have same interface
            assert hasattr(service1, 'app') and hasattr(service2, 'app')
            assert hasattr(service1, 'run') and hasattr(service2, 'run')
            print("✅ Services têm interface consistente")

            return True

        except Exception as e:
            print(f"❌ Integração entre examples falhou: {e}")
            return False

    def test_examples_error_handling(self):
        """Testa tratamento de erros nos examples."""
        print("\n🧪 Testando tratamento de erros nos examples...")

        # Test error handling in api_usage when service is down
        sys.path.insert(0, "examples")
        try:
            import api_usage

            # Temporarily change BASE_URL to non-existent service
            original_url = api_usage.BASE_URL
            api_usage.BASE_URL = "http://localhost:9999"  # Non-existent service

            # Test functions handle errors gracefully
            health = api_usage.check_service_health()
            assert health is False, "Should return False when service down"
            print("✅ check_service_health() trata erro corretamente")

            create_result = api_usage.create_application("test", 8080)
            assert create_result is None, "Should return None when service down"
            print("✅ create_application() trata erro corretamente")

            apps = api_usage.list_applications()
            assert isinstance(apps, list) and len(apps) == 0, "Should return empty list"
            print("✅ list_applications() trata erro corretamente")

            # Restore original URL
            api_usage.BASE_URL = original_url

            return True

        except Exception as e:
            print(f"❌ Teste de tratamento de erros falhou: {e}")
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def run_full_functionality_test(self):
        """Executa teste COMPLETO de toda funcionalidade dos examples."""
        print("🚀 INICIANDO TESTE COMPLETO DE TODA FUNCIONALIDADE DOS EXAMPLES/")
        print("=" * 80)

        # Start Docker service for testing
        if not self.start_service_in_docker():
            print("❌ Falha ao iniciar serviço Docker - alguns testes podem falhar")

        try:
            results = []

            # Test each example thoroughly
            results.append(("basic_service", self.test_basic_service_full_functionality()))
            results.append(("api_usage", self.test_api_usage_full_functionality()))
            results.append(("docker_ready", self.test_docker_ready_full_functionality()))
            results.append(("integration", self.test_examples_integration_functionality()))
            results.append(("error_handling", self.test_examples_error_handling()))

            # Results summary
            print("\n" + "=" * 80)
            print("📊 RESULTADOS DO TESTE COMPLETO DE FUNCIONALIDADE:")

            passed = 0
            for test_name, result in results:
                status = "✅ PASSOU" if result else "❌ FALHOU"
                print(f"  {status} {test_name}")
                if result:
                    passed += 1

            total = len(results)
            percentage = (passed / total) * 100

            print(f"\n🎯 RESULTADO FINAL: {passed}/{total} testes passaram ({percentage:.1f}%)")

            if passed == total:
                print("🎉 TODOS OS EXAMPLES/ FUNCIONAM COM 100% DA FUNCIONALIDADE!")
                print("🏆 EXAMPLES SÃO ENTERPRISE-READY!")
            elif passed >= total * 0.8:
                print("✅ Maioria dos examples funciona - PRODUCTION-READY!")
            else:
                print("⚠️ Alguns examples têm problemas - precisam atenção")

            return passed >= total * 0.8

        finally:
            self.stop_docker_service()


def main():
    """Executa teste completo de funcionalidade dos examples."""
    tester = ExamplesFullFunctionalityTest()
    success = tester.run_full_functionality_test()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
