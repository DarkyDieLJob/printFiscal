from tornado import ioloop, gen, websocket
import json

@gen.coroutine
def conectar_a_websocket(data):
    try:
        # Conectar al WebSocket
        ws = yield websocket.websocket_connect('ws://localhost:12000/ws')
        
        # Enviar el mensaje al servidor
        ws.write_message(json.dumps(data))
        
        # Esperar la respuesta del servidor
        respuesta = yield ws.read_message()
        print(respuesta)
        
        # Cerrar la conexión
        ws.close()
    except Exception as e:
        print("Error en la conexión WebSocket: {0}".format(str(e)))

# Ejemplo de uso
'''
{
	
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



