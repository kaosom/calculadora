#!/usr/bin/env python3

import xmlrpc.client
import sys
import logging
from typing import Union, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CalculatorClient:
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.proxy = None
        self.connected = False
    
    def connect(self) -> bool:
        try:
            logger.info(f"Conectando al servidor: {self.server_url}")
            self.proxy = xmlrpc.client.ServerProxy(self.server_url)
            
            response = self.proxy.ping()
            if response.get('success'):
                self.connected = True
                logger.info("Conexión establecida exitosamente")
                return True
            else:
                logger.error("Error en la respuesta del servidor")
                return False
                
        except ConnectionRefusedError:
            logger.error(f"No se pudo conectar al servidor en {self.server_url}")
            logger.error("Asegúrate de que el servidor esté ejecutándose")
            return False
        except Exception as e:
            logger.error(f"Error de conexión: {str(e)}")
            return False
    
    def disconnect(self):
        self.connected = False
        self.proxy = None
        logger.info("Desconectado del servidor")
    
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
    
    def add(self, a: str, b: str) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor'
            }
        
        num_a, num_b, error = self._validate_numbers(a, b)
        if error:
            logger.error(f"Error de validación: {error}")
            return {
                'success': False,
                'error': error
            }
        
        try:
            logger.info(f"Enviando petición de suma: {num_a} + {num_b}")
            result = self.proxy.add(num_a, num_b)
            
            if result.get('success'):
                logger.info(f"Resultado recibido: {result.get('result')}")
            else:
                logger.error(f"Error del servidor: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la comunicación: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def subtract(self, a: str, b: str) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor'
            }
        
        num_a, num_b, error = self._validate_numbers(a, b)
        if error:
            logger.error(f"Error de validación: {error}")
            return {
                'success': False,
                'error': error
            }
        
        try:
            logger.info(f"Enviando petición de resta: {num_a} - {num_b}")
            result = self.proxy.subtract(num_a, num_b)
            
            if result.get('success'):
                logger.info(f"Resultado recibido: {result.get('result')}")
            else:
                logger.error(f"Error del servidor: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la comunicación: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def multiply(self, a: str, b: str) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor'
            }
        
        num_a, num_b, error = self._validate_numbers(a, b)
        if error:
            logger.error(f"Error de validación: {error}")
            return {
                'success': False,
                'error': error
            }
        
        try:
            logger.info(f"Enviando petición de multiplicación: {num_a} * {num_b}")
            result = self.proxy.multiply(num_a, num_b)
            
            if result.get('success'):
                logger.info(f"Resultado recibido: {result.get('result')}")
            else:
                logger.error(f"Error del servidor: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la comunicación: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def divide(self, a: str, b: str) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor'
            }
        
        num_a, num_b, error = self._validate_numbers(a, b)
        if error:
            logger.error(f"Error de validación: {error}")
            return {
                'success': False,
                'error': error
            }
        
        try:
            logger.info(f"Enviando petición de división: {num_a} / {num_b}")
            result = self.proxy.divide(num_a, num_b)
            
            if result.get('success'):
                logger.info(f"Resultado recibido: {result.get('result')}")
            else:
                logger.error(f"Error del servidor: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la comunicación: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def get_stats(self) -> dict:
        if not self.connected:
            return {
                'success': False,
                'error': 'No hay conexión con el servidor'
            }
        
        try:
            logger.info("Solicitando estadísticas del servidor")
            result = self.proxy.get_stats()
            return result
        except Exception as e:
            error_msg = f"Error al obtener estadísticas: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }


def display_result(result: dict):
    print("\n" + "="*50)
    if result.get('success'):
        print(f"Operación exitosa: {result.get('operation')}")
        print(f"Resultado: {result.get('result')}")
        if 'operation_id' in result:
            print(f"ID de operación: {result.get('operation_id')}")
    else:
        print(f"Error: {result.get('error')}")
        if 'operation' in result:
            print(f"Operación: {result.get('operation')}")
    print("="*50 + "\n")


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
    print("Calculadora RPC - Cliente Local")
    print("="*50)
    
    client = CalculatorClient()
    
    if not client.connect():
        print("No se pudo conectar al servidor. Asegurate de que esté ejecutándose.")
        print("Ejecuta: python3 calculator_server.py")
        sys.exit(1)
    
    try:
        while True:
            print("\nOperaciónes disponibles:")
            print("1. Suma (+)")
            print("2. Resta (-)")
            print("3. Multiplicación (*)")
            print("4. División (/)")
            print("5. Ver estadísticas del servidor")
            print("6. Salir")
            
            while True:
                try:
                    choice = input("\nSelecciona una opción (1-6): ").strip()
                    if choice in ['1', '2', '3', '4', '5', '6']:
                        break
                    else:
                        print("Error: Opción inválida. Selecciona 1-6.")
                except KeyboardInterrupt:
                    print("\nHasta luego!")
                    client.disconnect()
                    sys.exit(0)
            
            if choice == '6':
                print("Hasta luego!")
                break
            
            elif choice == '5':
                result = client.get_stats()
                if result.get('success'):
                    print(f"\nEstadísticas del servidor:")
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
