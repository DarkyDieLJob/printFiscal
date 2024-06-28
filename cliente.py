
import asyncio
import websockets
import json

async def conectar_a_websocket(data):
	uri = "ws://169.254.124.42:12000/ws"  # Cambia la IP y el puerto según tu servidor

	# Convertir a formato de bytes
	mensaje_json = json.dumps(data).encode()

	async with websockets.connect(uri) as websocket:
		await websocket.send(mensaje_json)
		respuesta = await websocket.recv()
		while True:
			if respuesta:
				print(respuesta)
				break

# Ejemplo de uso

# Crear el JSON
boletas = [{
	"printTicket": {
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
	},
	"printerName": "IMPRESORA_FISCAL",
	},{
	"printTicket": {
		"cabecera": {
			"tipo_cbte": "FB",
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
	},
	"printerName": "IMPRESORA_FISCAL",
	}]
for boleta in boletas:
	print(boleta)
	asyncio.run(conectar_a_websocket(boleta))



