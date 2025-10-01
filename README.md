# Calculadora RPC

Una calculadora implementada con conectividad RPC (Remote Procedure Call) que permite comunicacion cliente-servidor tanto local como remota entre diferentes dispositivos.

## Caracteristicas

- **4 Operaciones basicas**: Suma, Resta, Multiplicacion, Division
- **Comunicacion RPC local**: Cliente y servidor en el mismo dispositivo
- **Comunicacion RPC remota**: Cliente y servidor en diferentes dispositivos
- **Descubrimiento automatico**: Busqueda automatica de servidores en la red local
- **Manejo de errores**: Mensajes de fallo detallados en servidor, cliente y funciones
- **Interfaz de usuario**: Entrada de datos por parte del usuario (cliente)
- **Estadisticas**: Seguimiento de operaciones realizadas
- **Verificacion de conectividad**: Ping para verificar estado del servidor

## Arquitectura

```
┌─────────────────┐    RPC     ┌─────────────────┐
│   Cliente       │ ◄─────────► │   Servidor      │
│                 │             │                 │
│ - Interfaz UI   │             │ - Operaciones   │
│ - Validacion    │             │ - Logging       │
│ - Manejo errores│             │ - Estadisticas  │
└─────────────────┘             └─────────────────┘
```

## Estructura del Proyecto

```
calculadora/
├── calculator_server.py          # Servidor RPC
├── calculator_client_local.py    # Cliente RPC local
├── calculator_client_remote.py   # Cliente RPC remoto
├── requirements.txt              # Dependencias
├── README.md                     # Documentacion
└── main.py                       # Archivo principal
```

## Instalacion y Configuracion

### Requisitos
- Python 3.7 o superior
- No se requieren dependencias externas (usa librerias estandar)

### Instalacion
```bash
# Clonar o descargar el proyecto
cd calculadora

# No se requiere pip install (usa librerias estandar)
# Verificar que Python 3.7+ este instalado
python3 --version
```

## Uso

### 1. Servidor RPC

Inicia el servidor en cualquier dispositivo:

```bash
# Servidor local (puerto 8000)
python3 calculator_server.py

# Servidor en IP especifica
python3 calculator_server.py --host 0.0.0.0 --port 8000

# Servidor en IP y puerto personalizados
python3 calculator_server.py --host 192.168.1.100 --port 9000
```

**Opciones del servidor:**
- `--host`: Direccion IP del servidor (default: localhost)
- `--port`: Puerto del servidor (default: 8000)

### 2. Cliente RPC Local

Para comunicacion local (mismo dispositivo):

```bash
python3 calculator_client_local.py
```

**Caracteristicas del cliente local:**
- Se conecta automaticamente a `localhost:8000`
- Interfaz de menu interactiva
- Validacion de entrada de datos
- Manejo de errores de conexion

### 3. Cliente RPC Remoto

Para comunicacion remota (diferentes dispositivos):

```bash
python3 calculator_client_remote.py
```

**Caracteristicas del cliente remoto:**
- Descubrimiento automatico de servidores en la red local
- Conexion manual a servidor especifico
- Escaneo de red para encontrar servidores disponibles
- Prueba de conectividad

## Ejemplos de Uso

### Ejemplo 1: Comunicacion Local

**Terminal 1 (Servidor):**
```bash
python3 calculator_server.py
# Salida: Servidor RPC iniciado en localhost:8000
```

**Terminal 2 (Cliente):**
```bash
python3 calculator_client_local.py
# Seleccionar operacion y ingresar numeros
```

### Ejemplo 2: Comunicacion Remota

**Dispositivo A (Servidor):**
```bash
python3 calculator_server.py --host 0.0.0.0 --port 8000
# Servidor escuchando en todas las interfaces
```

**Dispositivo B (Cliente):**
```bash
python3 calculator_client_remote.py
# Seleccionar "Buscar servidores automaticamente"
# O conectar manualmente a la IP del Dispositivo A
```

## Operaciones Disponibles

| Operacion | Simbolo | Descripcion | Ejemplo |
|-----------|---------|-------------|---------|
| Suma | + | Suma dos numeros | 5 + 3 = 8 |
| Resta | - | Resta dos numeros | 10 - 4 = 6 |
| Multiplicacion | * | Multiplica dos numeros | 7 * 6 = 42 |
| Division | / | Divide dos numeros | 15 / 3 = 5 |

## Manejo de Errores

### Errores del Servidor
- **Division por cero**: `Error: Division por cero no permitida`
- **Datos invalidos**: `Error en [operacion]: [detalle]`
- **Logging**: Todos los errores se registran en el servidor

### Errores del Cliente
- **Sin conexion**: `No hay conexion con el servidor`
- **Validacion**: `Error: Los valores deben ser numeros validos`
- **Comunicacion**: `Error en la comunicacion: [detalle]`

### Errores de Red
- **Conexion rechazada**: `No se pudo conectar al servidor`
- **Timeout**: `Error de conexion: [detalle]`
- **Servidor no encontrado**: `No se encontraron servidores en la red local`

## Funciones Adicionales

### Estadisticas del Servidor
```python
# Obtener estadisticas
result = client.get_stats()
# Retorna: total_operations, server_status
```

### Verificacion de Conectividad
```python
# Ping al servidor
result = client.ping()
# Retorna: success, message, server_status
```

### Descubrimiento de Red
```python
# Buscar servidores automaticamente
servers = client.discover_servers(port=8000)
# Retorna lista de servidores disponibles
```

## Configuracion de Red

### Para Comunicacion Remota

1. **Asegurar conectividad de red:**
   - Ambos dispositivos en la misma red
   - Firewall configurado para permitir el puerto
   - IPs accesibles entre dispositivos

2. **Configuracion del servidor:**
   ```bash
   # Para escuchar en todas las interfaces
   python3 calculator_server.py --host 0.0.0.0 --port 8000
   ```

3. **Configuracion del cliente:**
   - Usar la IP real del servidor
   - Verificar que el puerto este abierto

## Solucion de Problemas

### Problema: "No se pudo conectar al servidor"
**Soluciones:**
- Verificar que el servidor este ejecutandose
- Comprobar la IP y puerto
- Verificar firewall/antivirus
- Probar con `localhost` primero

### Problema: "No se encontraron servidores"
**Soluciones:**
- Verificar que ambos dispositivos esten en la misma red
- Comprobar que el servidor este escuchando en `0.0.0.0`
- Verificar configuracion de firewall
- Intentar conexion manual

### Problema: "Error de validacion"
**Soluciones:**
- Ingresar solo numeros validos
- Usar punto (.) para decimales
- No dejar campos vacios

## Logging

El sistema incluye logging detallado:

- **Servidor**: Registra todas las operaciones y errores
- **Cliente**: Registra conexiones y comunicaciones
- **Nivel**: INFO por defecto
- **Formato**: `timestamp - level - message`

## Consideraciones de Seguridad

- **Solo red local**: El sistema esta diseñado para redes confiables
- **Sin autenticacion**: No incluye autenticacion (para simplicidad)
- **XML-RPC**: Protocolo estandar pero sin cifrado
- **Firewall**: Configurar apropiadamente para produccion

## Extensibilidad

El sistema esta diseñado para ser extensible:

- **Nuevas operaciones**: Agregar metodos al `CalculatorService`
- **Autenticacion**: Implementar en el servidor
- **Cifrado**: Usar HTTPS en lugar de HTTP
- **Persistencia**: Guardar estadisticas en base de datos
- **Interfaz grafica**: Crear GUI con tkinter/PyQt

## Soporte

Para problemas o preguntas:
1. Verificar logs del servidor y cliente
2. Comprobar conectividad de red
3. Revisar configuracion de firewall
4. Probar con configuracion local primero

---

**Hecho con Python 3.7+ y XML-RPC**