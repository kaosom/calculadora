#!/usr/bin/env python3

import sys
import os

def main():
    print("Calculadora RPC")
    print("="*50)
    print("Selecciona una opcion:")
    print("1. Iniciar servidor")
    print("2. Cliente local")
    print("3. Cliente remoto")
    print("4. Demo automática")
    print("5. Salir")
    
    while True:
        try:
            choice = input("\nOpción (1-5): ").strip()
            
            if choice == '1':
                print("Iniciando servidor...")
                try:
                    os.system("python3 calculator_server.py")
                except Exception as e:
                    print(f"Error al iniciar servidor: {str(e)}")
                break
            elif choice == '2':
                print("Iniciando cliente local...")
                try:
                    os.system("python3 calculator_client_local.py")
                except Exception as e:
                    print(f"Error al iniciar cliente local: {str(e)}")
                break
            elif choice == '3':
                print("Iniciando cliente remoto...")
                try:
                    os.system("python3 calculator_client_remote.py")
                except Exception as e:
                    print(f"Error al iniciar cliente remoto: {str(e)}")
                break
            elif choice == '4':
                print("Ejecutando demo...")
                try:
                    os.system("python3 demo.py")
                except Exception as e:
                    print(f"Error al ejecutar demo: {str(e)}")
                break
            elif choice == '5':
                print("Hasta luego!")
                sys.exit(0)
            else:
                print("Error: Opción invalida. Selecciona 1-5.")
        except KeyboardInterrupt:
            print("\nHasta luego!")
            sys.exit(0)
        except Exception as e:
            print(f"Error inesperado: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
