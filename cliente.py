import socket
import json

# Datos del servidor
host = '169.254.0.251'
port = 12000

# Crear el socket y conectar
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Crear el JSON
data = {
	  "printTicket": {
		"encabezado": ["Nombre del vendedor:", "PEPE GOMEZ", "."],
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
		   "importe": 128.5749995,
		   "ds": "FERNET",
		   "qty": 24,
		   "tasaAjusteInternos": 21.85
		 }, 
		 {
		   "alic_iva": 21,
		   "importe": 164.0160845,
		   "ds": "VINO",
		   "qty": 6
		 }
		],
		"dtosGenerales": [
		 {
		   "alic_iva": 21,
		   "importe": 10,
		   "ds": "Descuento"
		 }
		],
		"formasPago": [
		 {
		  "ds": "Cuenta Corriente",
		  "importe": 4770.22
		 }
		],
		"percepciones": [
		 {
		  "importe": 52.22,
		  "ds": "PERCEPCION CBA",
		  "porcPerc": 2
		 }
		],
		"descuentosRecargos": [
		  {
		   "alic_iva": 21,
		   "importe": 155.5,
		   "ds": "DESCUENTO",
		   "tasaAjusteInternos": 21.85
		  }
		],
		"pie": ["Efectivo 4771.22", "Vuelto: 1.00"]
      },
	  "printerName": "IMPRESORA_FISCAL"
	}

# Convertir a formato de bytes
json_data = json.dumps(data).encode()

# Enviar el JSON
client_socket.sendall(json_data)


