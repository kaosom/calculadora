#!/usr/bin/env python3

import xmlrpc.client
import time
import threading
from calculator_server import CalculatorService, start_server


def demo_server():
    try:
        print("Iniciando servidor de demo...")
        start_server('localhost', 8001)
    except Exception as e:
        print(f"Error al iniciar servidor de demo: {str(e)}")


def demo_client():
    time.sleep(2)
    
    try:
        proxy = xmlrpc.client.ServerProxy("http://localhost:8001")
        
        ping_result = proxy.ping()
        print(f"Ping al servidor: {ping_result}")
        
        operations = [
            ("add", 10, 5),
            ("subtract", 20, 8),
            ("multiply", 7, 6),
            ("divide", 15, 3),
            ("divide", 10, 0),
        ]
        
        print("\nRealizando operaciones de demostracion:")
        print("="*50)
        
        for operation, a, b in operations:
            try:
                result = getattr(proxy, operation)(a, b)
                if result.get('success'):
                    print(f"Operacion exitosa: {result.get('operation')} = {result.get('result')}")
                else:
                    print(f"Error: {result.get('error')}")
            except Exception as e:
                print(f"Excepcion: {str(e)}")
            
            time.sleep(0.5)
        
        stats = proxy.get_stats()
        if stats.get('success'):
            print(f"\nEstadísticas del servidor:")
            print(f"   Total de operaciones: {stats.get('total_operations')}")
            print(f"   Estado: {stats.get('server_status')}")
        
    except Exception as e:
        print(f"Error en el cliente de demo: {str(e)}")


def main():
    print("Demo de la Calculadora RPC")
    print("="*50)
    print("Esta demo muestra:")
    print("- Inicio automático del servidor")
    print("- Conexión del cliente")
    print("- Realización de operaciones")
    print("- Manejo de errores")
    print("- Obtención de estadísticas")
    print("="*50)
    
    try:
        server_thread = threading.Thread(target=demo_server, daemon=True)
        server_thread.start()
        
        demo_client()
        
        print("\nDemo completada!")
        print("Para usar la calculadora interactivamente:")
        print("   1. python3 calculator_server.py")
        print("   2. python3 calculator_client_local.py")
    except Exception as e:
        print(f"Error en la demo: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo cancelada")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
