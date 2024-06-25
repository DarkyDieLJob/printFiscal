
import asyncio
import websockets
import json

async def conectar_a_websocket(data):
	uri = "ws://169.254.0.251:12000/ws"  # Cambia la IP y el puerto según tu servidor

	# Convertir a formato de bytes
	mensaje_json = json.dumps(data).encode()

	async with websockets.connect(uri) as websocket:
		await websocket.send(mensaje_json)
		respuesta = await websocket.recv()
		print(f"Respuesta del servidor: {respuesta}")

# Ejemplo de uso

# Crear el JSON
data = {
	"printTicket": {
		"encabezado": [
			"Nombre del vendedor:",
			"PEPE GOMEZ",
			"."
		],
		"cabecera": {
			"tipo_cbte": "FA",
			"nro_doc": 11111111111,
			"domicilio_cliente": "CALLE DE LA DIRECCION 1234",
			"tipo_doc": "CUIT",
			"nombre_cliente": "JOSE LOPEZ",
			"tipo_responsable": "RESPONSABLE_INSCRIPTO"
		},
		"items": [
			{
			"alic_iva": 21,
			"importe": 128.57,
			"ds": "FERNET",
			"qty": 24,
			"tasaAjusteInternos": 0
			}, 
			{
			"alic_iva": 21,
			"importe": 164.01,
			"ds": "VINO",
			"qty": 6
			}
		],
		"formasPago": [
			{
			"ds": "Cuenta Corriente",
			"importe": 4924.39
			}
		],
		"pie": [
			"Efectivo 4924.39",
			"Vuelto: 0"
		]
	},
	"printerName": "IMPRESORA_FISCAL"
	}
asyncio.run(conectar_a_websocket(data))



