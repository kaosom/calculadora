#!/usr/bin/env python3

import xmlrpc.server
import sys
import logging
from typing import Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CalculatorService:
    
    def __init__(self):
        self.operations_count = 0
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> dict:
        try:
            self.operations_count += 1
            result = a + b
            print(f"Solicitud recibida: SUMA - {a} + {b}")
            logger.info(f"Operación #{self.operations_count}: {a} + {b} = {result}")
            return {
                'success': True,
                'result': result,
                'operation': f"{a} + {b}",
                'operation_id': self.operations_count
            }
        except Exception as e:
            error_msg = f"Error en suma: {str(e)}"
            print(f"Error en servidor: {error_msg}")
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'operation': f"{a} + {b}"
            }
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> dict:
        try:
            self.operations_count += 1
            result = a - b
            print(f"Solicitud recibida: RESTA - {a} - {b}")
            logger.info(f"Operación #{self.operations_count}: {a} - {b} = {result}")
            return {
                'success': True,
                'result': result,
                'operation': f"{a} - {b}",
                'operation_id': self.operations_count
            }
        except Exception as e:
            error_msg = f"Error en resta: {str(e)}"
            print(f"Error en servidor: {error_msg}")
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'operation': f"{a} - {b}"
            }
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> dict:
        try:
            self.operations_count += 1
            result = a * b
            print(f"Solicitud recibida: MULTIPLICACIÓN - {a} * {b}")
            logger.info(f"Operación #{self.operations_count}: {a} * {b} = {result}")
            return {
                'success': True,
                'result': result,
                'operation': f"{a} * {b}",
                'operation_id': self.operations_count
            }
        except Exception as e:
            error_msg = f"Error en multiplicación: {str(e)}"
            print(f"Error en servidor: {error_msg}")
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'operation': f"{a} * {b}"
            }
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> dict:
        try:
            self.operations_count += 1
            print(f"Solicitud recibida: DIVISION - {a} / {b}")
            
            if b == 0:
                error_msg = "Error: División por cero no permitida"
                print(f"Error en servidor: {error_msg}")
                logger.error(f"Operación #{self.operations_count}: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                    'operation': f"{a} / {b}"
                }
            
            result = a / b
            logger.info(f"Operación #{self.operations_count}: {a} / {b} = {result}")
            return {
                'success': True,
                'result': result,
                'operation': f"{a} / {b}",
                'operation_id': self.operations_count
            }
        except Exception as e:
            error_msg = f"Error en división: {str(e)}"
            print(f"Error en servidor: {error_msg}")
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'operation': f"{a} / {b}"
            }
    
    def get_stats(self) -> dict:
        try:
            print("Solicitud recibida: ESTADÍSTICAS")
            return {
                'success': True,
                'total_operations': self.operations_count,
                'server_status': 'running'
            }
        except Exception as e:
            error_msg = f"Error al obtener estadísticas: {str(e)}"
            print(f"Error en servidor: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def ping(self) -> dict:
        try:
            print("Solicitud recibida: PING")
            return {
                'success': True,
                'message': 'pong',
                'server_status': 'alive'
            }
        except Exception as e:
            error_msg = f"Error en ping: {str(e)}"
            print(f"Error en servidor: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }


def start_server(host='localhost', port=8000):
    try:
        server = xmlrpc.server.SimpleXMLRPCServer((host, port), allow_none=True)
        
        calculator = CalculatorService()
        server.register_instance(calculator)
        
        server.register_function(calculator.add, 'add')
        server.register_function(calculator.subtract, 'subtract')
        server.register_function(calculator.multiply, 'multiply')
        server.register_function(calculator.divide, 'divide')
        server.register_function(calculator.get_stats, 'get_stats')
        server.register_function(calculator.ping, 'ping')
        
        logger.info(f"Servidor RPC iniciado en {host}:{port}")
        logger.info("Operaciones disponibles: add, subtract, multiply, divide, get_stats, ping")
        logger.info("Presiona Ctrl+C para detener el servidor")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Calculadora RPC Server')
    parser.add_argument('--host', default='localhost', help='Dirección del servidor (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Puerto del servidor (default: 8000)')
    
    args = parser.parse_args()
    
    start_server(args.host, args.port)
