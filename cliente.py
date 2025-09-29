
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
<<<<<<< HEAD
		"pie": [
			"Efectivo 4924.39",
			"Vuelto: 0"
		]
	},
	"printerName": "IMPRESORA_FISCAL"
	}
asyncio.run(conectar_a_websocket(data))
=======
	},
	"printerName": "IMPRESORA_FISCAL",
	},
'''
# Crear el JSON
boletas = [{
    "printTicket": {
        "cabecera": {
            "tipo_cbte": "T",  # T para Tique, F para Factura, etc.
            "nro_doc": "20123456789",  # Número de documento (CUIT)
            "domicilio_cliente": "CALLE FALSA 123",
            "tipo_doc": "CUIT",  # Usar el nombre del tipo de documento, no el número
            "nombre_cliente": "CLIENTE DE PRUEBA",
            "tipo_responsable": "RESPONSABLE_INSCRIPTO",  # Usar el nombre del tipo de responsable
            "condicion_iva": "RESPONSABLE_INSCRIPTO",  # Usar el nombre de la condición de IVA
            "condicion_venta": "CONTADO",  # Usar el nombre de la condición de venta
            "cae": "12345678901234",  # CAE de prueba
            "vencimiento_cae": "20301231"  # Fecha de vencimiento del CAE
        },
        "items": [
            {
                "ds": "PRODUCTO DE PRUEBA 1",  # Descripción del producto
                "qty": 2.0,                   # Cantidad
                "importe": 200.0,              # Precio total (cantidad * precio unitario)
                "alic_iva": 21.0,              # Porcentaje de IVA (21%)
                "tasaAjusteInternos": 0,       # Tasa de ajuste internos (si aplica)
                "itemNegative": False,          # Indica si es un ítem negativo (para NC)
                "discount": 0,                 # Descuento aplicado al ítem
                "discountDescription": "",     # Descripción del descuento
                "discountNegative": True        # Indica si el descuento es negativo
            },
            {
                "ds": "PRODUCTO DE PRUEBA 2",
                "qty": 1.0,
                "importe": 150.0,
                "alic_iva": 10.5,              # 10.5% de IVA
                "tasaAjusteInternos": 0,
                "itemNegative": False,
                "discount": 0,
                "discountDescription": "",
                "discountNegative": True
            }
        ],
        "formasPago": [
            {
                "ds": "EFECTIVO",      # Descripción de la forma de pago
                "importe": 350.0       # Monto a pagar con esta forma de pago
            }
        ]
    },
    "printerName": "IMPRESORA_FISCAL"
}]
if __name__ == "__main__":
    for boleta in boletas:
        print("Enviando boleta:")
        print(boleta)
        ioloop.IOLoop.current().run_sync(lambda b=boleta: conectar_a_websocket(b))
>>>>>>> 5d141564bec8d2194f04867f4c0ccffcaa47639e



