#!/usr/bin/env python3

import xmlrpc.client
import sys
import logging
import socket
from typing import Union, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RemoteCalculatorClient:
    
    def __init__(self):
        self.proxy = None
        self.connected = False
        self.server_url = None
        self.server_info = None
    
    def discover_servers(self, port: int = 8000, timeout: float = 1.0) -> list:
        try:
            print("Buscando servidores en la red local...")
            available_servers = []
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(("8.8.8.8", 80))
                    local_ip = s.getsockname()[0]
            except:
                local_ip = "127.0.0.1"
            
            network = ".".join(local_ip.split(".")[:-1])
            
            print(f"Escaneando red: {network}.0/24 en puerto {port}")
            
            for i in range(1, 255):
                ip = f"{network}.{i}"
                if ip == local_ip:
                    continue
                    
                try:
                    url = f"http://{ip}:{port}"
                    proxy = xmlrpc.client.ServerProxy(url)
                    
                    import threading
                    import time
                    
                    result = None
                    def ping_server():
                        nonlocal result
                        try:
                            result = proxy.ping()
                        except:
                            result = None
                    
                    thread = threading.Thread(target=ping_server)
                    thread.daemon = True
                    thread.start()
                    thread.join(timeout)
                    
                    if result and result.get('success'):
                        available_servers.append({
                            'ip': ip,
                            'port': port,
                            'url': url,
                            'status': 'online'
                        })
                        print(f"Servidor encontrado: {ip}:{port}")
                    
                except:
                    continue
            
            if not available_servers:
                print("No se encontraron servidores en la red local")
                print("Asegurate de que el servidor esté ejecutandose en otro dispositivo")
            
            return available_servers
        except Exception as e:
            print(f"Error al buscar servidores: {str(e)}")
            return []
    
    def connect_to_server(self, server_url: str) -> bool:
        try:
            logger.info(f"Conectando al servidor remoto: {server_url}")
            self.proxy = xmlrpc.client.ServerProxy(server_url)
            
            response = self.proxy.ping()
            if response.get('success'):
                self.connected = True
                self.server_url = server_url
                self.server_info = response
                logger.info("Conexión remota establecida exitosamente")
                return True
            else:
                logger.error("Error en la respuesta del servidor")
                return False
                
        except ConnectionRefusedError:
            logger.error(f"No se pudo conectar al servidor en {server_url}")
            logger.error("Verifica que el servidor esté ejecutándose y accesible")
            return False
        except Exception as e:
            logger.error(f"Error de conexión: {str(e)}")
            return False
    
    def disconnect(self):
        self.connected = False
        self.proxy = None
        self.server_url = None
        self.server_info = None
        logger.info("Desconectado del servidor remoto")
    
    def _validate_numbers(self, a: str, b: str) -> tuple[Optional[float], Optional[float], Optional[str]]:
        try:
            num_a = float(a)
            num_b = float(b)
            
            if num_a < -1000000 or num_a > 1000000:
                return None, None, "Error: El primer número debe estar entre -1,000,000 y 1,000,000"
            
            if num_b < -1000000 or num_b > 1000000:
                return None, None, "Error: El segundo número debe estar entre -1,000,000 y 1,000,000"
            
            return num_a, num_b, None
        except ValueError as e:
            return None, None, f"Error: Los valores deben ser números válidos. {str(e)}"
    
    def _execute_operation(self, operation: str, a: str, b: str) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor remoto'
            }
        
        num_a, num_b, error = self._validate_numbers(a, b)
        if error:
            logger.error(f"Error de validación: {error}")
            return {
                'success': False,
                'error': error
            }
        
        try:
            logger.info(f"Enviando petición remota de {operation}: {num_a} {operation} {num_b}")
            result = getattr(self.proxy, operation)(num_a, num_b)
            
            if result.get('success'):
                logger.info(f"Resultado remoto recibido: {result.get('result')}")
            else:
                logger.error(f"Error del servidor remoto: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la comunicación remota: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def add(self, a: str, b: str) -> dict:
        return self._execute_operation('add', a, b)
    
    def subtract(self, a: str, b: str) -> dict:
        return self._execute_operation('subtract', a, b)
    
    def multiply(self, a: str, b: str) -> dict:
        return self._execute_operation('multiply', a, b)
    
    def divide(self, a: str, b: str) -> dict:
        return self._execute_operation('divide', a, b)
    
    def get_stats(self) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor remoto'
            }
        
        try:
            logger.info("Solicitando estadísticas del servidor remoto")
            result = self.proxy.get_stats()
            return result
        except Exception as e:
            error_msg = f"Error al obtener estadísticas remotas: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def test_connection(self) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor'
            }
        
        try:
            logger.info("Probando conexión remota...")
            result = self.proxy.ping()
            return result
        except Exception as e:
            error_msg = f"Error en la prueba de conexión: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }


def display_result(result: dict):
    print("\n" + "="*50)
    if result.get('success'):
        print(f"Operación remota exitosa: {result.get('operation')}")
        print(f"Resultado: {result.get('result')}")
        if 'operation_id' in result:
            print(f"ID de operación: {result.get('operation_id')}")
    else:
        print(f"Error remoto: {result.get('error')}")
        if 'operation' in result:
            print(f"Operación: {result.get('operation')}")
    print("="*50 + "\n")


def display_server_info(client: RemoteCalculatorClient):
    if client.connected and client.server_url:
        print(f"\nServidor remoto conectado: {client.server_url}")
        if client.server_info:
            print(f"Estado: {client.server_info.get('server_status', 'unknown')}")
    else:
        print("\nNo hay servidor remoto conectado")


def get_valid_number(prompt: str) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Error: Debes ingresar un número")
                continue
            
            num = float(value)
            if num < -1000000 or num > 1000000:
                print("Error: El número debe estar entre -1,000,000 y 1,000,000")
                continue
            
            return value
        except ValueError:
            print("Error: Debes ingresar un número válido")
        except KeyboardInterrupt:
            print("\nOperación cancelada")
            return ""


def main():
    print("Calculadora RPC - Cliente Remoto")
    print("="*50)
    
    client = RemoteCalculatorClient()
    
    while True:
        print("\nOpciones de conexión:")
        print("1. Buscar servidores automáticamente")
        print("2. Conectar a servidor específico")
        print("3. Salir")
        
        while True:
            try:
                choice = input("\nSelecciona una opción (1-3): ").strip()
                if choice in ['1', '2', '3']:
                    break
                else:
                    print("Error: Opción inválida. Selecciona 1-3.")
            except KeyboardInterrupt:
                print("\nHasta luego!")
                sys.exit(0)
        
        if choice == '3':
            print("Hasta luego!")
            break
        
        elif choice == '1':
            servers = client.discover_servers()
            
            if not servers:
                print("No se encontraron servidores. Intenta conectar manualmente.")
                continue
            
            print(f"\nSe encontraron {len(servers)} servidor(es):")
            for i, server in enumerate(servers, 1):
                print(f"   {i}. {server['ip']}:{server['port']} - {server['status']}")
            
            while True:
                try:
                    server_choice = int(input(f"\nSelecciona un servidor (1-{len(servers)}): ")) - 1
                    if 0 <= server_choice < len(servers):
                        selected_server = servers[server_choice]
                        if client.connect_to_server(selected_server['url']):
                            print(f"Conectado exitosamente a {selected_server['ip']}:{selected_server['port']}")
                            break
                        else:
                            print("No se pudo conectar al servidor seleccionado")
                            break
                    else:
                        print("Error: Selección inválida")
                except ValueError:
                    print("Error: Por favor ingresa un número válido")
                except KeyboardInterrupt:
                    print("\nHasta luego!")
                    sys.exit(0)
            
            if client.connected:
                break
        
        elif choice == '2':
            print("\nConectar a servidor específico:")
            
            while True:
                try:
                    ip = input("Ingresa la IP del servidor: ").strip()
                    if not ip:
                        print("Error: Debes ingresar una IP")
                        continue
                    break
                except KeyboardInterrupt:
                    print("\nHasta luego!")
                    sys.exit(0)
            
            while True:
                try:
                    port_input = input("Ingresa el puerto (default: 8000): ").strip() or "8000"
                    port = int(port_input)
                    if port < 1 or port > 65535:
                        print("Error: Puerto debe estar entre 1 y 65535")
                        continue
                    break
                except ValueError:
                    print("Error: Puerto inválido")
                except KeyboardInterrupt:
                    print("\nHasta luego!")
                    sys.exit(0)
            
            server_url = f"http://{ip}:{port}"
            
            if client.connect_to_server(server_url):
                print(f"Conectado exitosamente a {ip}:{port}")
                break
            else:
                print("No se pudo conectar al servidor")
    
    if not client.connected:
        print("No se pudo establecer conexión. Saliendo...")
        sys.exit(1)
    
    display_server_info(client)
    
    try:
        while True:
            print("\nOperaciónes disponibles:")
            print("1. Suma (+)")
            print("2. Resta (-)")
            print("3. Multiplicación (*)")
            print("4. División (/)")
            print("5. Ver estadísticas del servidor")
            print("6. Probar conexión")
            print("7. Desconectar y salir")
            
            while True:
                try:
                    choice = input("\nSelecciona una opción (1-7): ").strip()
                    if choice in ['1', '2', '3', '4', '5', '6', '7']:
                        break
                    else:
                        print("Error: Opción inválida. Selecciona 1-7.")
                except KeyboardInterrupt:
                    print("\nHasta luego!")
                    client.disconnect()
                    sys.exit(0)
            
            if choice == '7':
                print("Desconectando...")
                break
            
            elif choice == '6':
                result = client.test_connection()
                if result.get('success'):
                    print("Conexión remota funcionando correctamente")
                else:
                    print(f"Error de conexión: {result.get('error')}")
                continue
            
            elif choice == '5':
                result = client.get_stats()
                if result.get('success'):
                    print(f"\nEstadísticas del servidor remoto:")
                    print(f"   Total de operaciones: {result.get('total_operations')}")
                    print(f"   Estado: {result.get('server_status')}")
                else:
                    print(f"Error: {result.get('error')}")
                continue
            
            elif choice in ['1', '2', '3', '4']:
                try:
                    a = get_valid_number("Ingresa el primer número: ")
                    if not a:
                        continue
                    
                    b = get_valid_number("Ingresa el segundo número: ")
                    if not b:
                        continue
                    
                    if choice == '1':
                        result = client.add(a, b)
                    elif choice == '2':
                        result = client.subtract(a, b)
                    elif choice == '3':
                        result = client.multiply(a, b)
                    elif choice == '4':
                        result = client.divide(a, b)
                    
                    display_result(result)
                    
                except KeyboardInterrupt:
                    print("\nOperación cancelada")
                    continue
                except Exception as e:
                    print(f"Error inesperado: {str(e)}")
                    continue
    
    except KeyboardInterrupt:
        print("\nHasta luego!")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
