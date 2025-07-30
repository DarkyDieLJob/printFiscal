#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import ioloop, gen, websocket
import json
import argparse

@gen.coroutine
def conectar_a_websocket(data):
    """
    Función para conectar al WebSocket y enviar el comando de cierre Z
    """
    try:
        # Conectar al WebSocket
        print("Conectando al servidor WebSocket...")
        ws = yield websocket.websocket_connect('ws://localhost:12000/ws')
        
        # Enviar el mensaje al servidor
        print("Enviando comando de cierre Z...")
        ws.write_message(json.dumps(data))
        
        # Esperar la respuesta del servidor
        print("Esperando respuesta...")
        respuesta = yield ws.read_message()
        print("\n" + "="*50)
        print("RESPUESTA DEL SERVIDOR:")
        try:
            # Intentar formatear la respuesta JSON
            respuesta_json = json.loads(respuesta)
            print(json.dumps(respuesta_json, indent=2, ensure_ascii=False))
        except:
            # Si no es JSON, mostrarla tal cual
            print(respuesta)
        print("="*50 + "\n")
        
        # Cerrar la conexión
        ws.close()
    except Exception as e:
        print("\n" + "!"*50)
        print("ERROR EN LA CONEXIÓN:")
        print(str(e))
        print("!"*50 + "\n")


def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Enviar comando de cierre Z a la impresora fiscal')
    parser.add_argument('--tipo', type=str, default='Z', 
                       choices=['Z', 'X'],
                       help='Tipo de cierre: Z (cierre total) o X (cierre parcial)')
    
    # Obtener los argumentos
    args = parser.parse_args()
    
    # Crear el mensaje para el cierre Z
    mensaje = {
        "dailyClose": args.tipo,
        "printerName": "IMPRESORA_FISCAL"
    }
    
    print("\n" + "*"*60)
    print("INICIANDO CIERRE {}".format(args.tipo))
    print("*"*60)
    print("\nConfiguración:")
    print("- Tipo de cierre: {}".format(args.tipo))
    print("- Impresora: IMPRESORA_FISCAL")
    print("\nPresione Ctrl+C para cancelar...")
    
    try:
        # Ejecutar el bucle de eventos de Tornado
        ioloop.IOLoop.current().run_sync(lambda: conectar_a_websocket(mensaje))
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print("\nError inesperado: {}".format(str(e)))


if __name__ == "__main__":
    main()
