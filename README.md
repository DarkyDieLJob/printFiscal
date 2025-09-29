# Impresora Fiscal - Documentación

Este proyecto permite la comunicación con impresoras fiscales a través de una API REST. Actualmente, es compatible con impresoras Hasar 715v2, pero puede extenderse a otros modelos.

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Configuración Inicial](#configuración-inicial)
3. [Uso con Docker](#uso-con-docker)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [API de Ejemplo](#api-de-ejemplo)
6. [Solución de Problemas](#solución-de-problemas)
7. [Licencia](#licencia)

## Requisitos del Sistema

- Python 2.7
- Docker (opcional, para despliegue en contenedores)
- Impresora fiscal compatible (Hasar 715v2 probada)
- Permisos de escritura en el puerto USB (/dev/ttyUSB0)

## Configuración Inicial

### 1. Instalación de Dependencias

```bash
# Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y python-pip python-serial

# Instalar dependencias de Python
pip install -r requirements_fiscal.txt
```

### 2. Configuración de la Impresora

Edite el archivo `config.ini` con los parámetros de su impresora:

```ini
[IMPRESORA_FISCAL]
path = /dev/ttyUSB0
speed = 9600
driver = Hasar
```

### 3. Permisos del Puerto USB

Asegúrese de que el usuario tenga permisos para acceder al puerto USB:

```bash
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB0
```

## Uso con Docker

### Construir la imagen

```bash
docker build -t print-fiscal .
```

### Ejecutar el contenedor

```bash
docker run -d --name fiscal-printer \
  -p 12000:12000 \
  --device=/dev/ttyUSB0 \
  -v /dev/ttyUSB0:/dev/ttyUSB0 \
  --group-add dialout \
  --privileged \
  print-fiscal
```

## Estructura del Proyecto

- `server.py`: Punto de entrada del servidor
- `cliente.py`: Cliente de ejemplo para probar la impresión
- `ConfigFiscal.py`: Manejo de configuración
- `Traductores/`: Lógica de traducción para diferentes impresoras
- `Drivers/`: Controladores para diferentes modelos de impresoras

## API de Ejemplo

### Enviar un ticket

```python
import asyncio
import websockets
import json

async def enviar_ticket():
    data = {
        "printTicket": {
            "cabecera": {
                "tipo_cbte": "T",
                "nro_doc": "20123456789",
                "domicilio_cliente": "CALLE FALSA 123",
                "tipo_doc": "CUIT",
                "nombre_cliente": "CLIENTE DE PRUEBA",
                "tipo_responsable": "RESPONSABLE_INSCRIPTO",
                "condicion_venta": "CONTADO"
            },
            "items": [
                {
                    "ds": "PRODUCTO DE PRUEBA 1",
                    "qty": 2.0,
                    "importe": 200.0,
                    "alic_iva": 21.0,
                    "tasaAjusteInternos": 0,
                    "itemNegative": False
                }
            ],
            "formasPago": [
                {
                    "ds": "EFECTIVO",
                    "importe": 200.0
                }
            ]
        },
        "printerName": "IMPRESORA_FISCAL"
    }
    
    async with websockets.connect('ws://localhost:12000/ws') as websocket:
        await websocket.send(json.dumps(data))
        respuesta = await websocket.recv()
        print(respuesta)

asyncio.get_event_loop().run_until_complete(enviar_ticket())
```

## Solución de Problemas

### Error: "could not open port COM1"

Asegúrese de que:
1. El puerto USB esté correctamente configurado en `config.ini`
2. La impresora esté conectada y encendida
3. Los permisos del puerto sean correctos

### Error: "object of type 'int' has no len()"

Verifique que los tipos de datos en el JSON sean los correctos (usar cadenas en lugar de números donde corresponda).

## Licencia

Este proyecto está bajo la licencia MIT.
