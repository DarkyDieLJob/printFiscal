#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TestUSBConnection')

def test_usb_detection():
    """Prueba la detección de dispositivos USB"""
    from USBManager import USBManager
    
    logger.info("=== Iniciando prueba de detección USB ===")
    
    # Crear instancia del gestor USB
    usb_manager = USBManager()
    
    # Buscar dispositivo
    logger.info("Buscando dispositivo USB...")
    device = usb_manager.find_usb_device()
    
    if device:
        logger.info("Dispositivo encontrado en: %s" % device)
        return True
    else:
        logger.warning("No se encontró ningún dispositivo USB compatible")
        return False

def test_printer_connection():
    """Prueba la conexión con la impresora fiscal"""
    from Drivers.FiscalPrinterDriver import FiscalPrinterDriver
    
    logger.info("\n=== Iniciando prueba de conexión con impresora ===")
    
    try:
        # Inicializar el driver con detección automática
        logger.info("Inicializando driver con detección automática...")
        printer = FiscalPrinterDriver(path='auto')
        
        # Intentar un comando simple
        logger.info("Enviando comando de estado...")
        response = printer.sendCommand(0x0101, [])  # Comando de estado
        logger.info("Respuesta de la impresora: %s" % str(response))
        
        return True
    except Exception as e:
        logger.error("Error en la prueba de conexión: %s" % str(e))
        return False

def test_reconnection():
    """Prueba la reconexión automática"""
    from Drivers.FiscalPrinterDriver import FiscalPrinterDriver
    
    logger.info("\n=== Iniciando prueba de reconexión ===")
    
    try:
        # Inicializar el driver
        logger.info("Inicializando driver...")
        printer = FiscalPrinterDriver(path='auto')
        
        # Verificar conexión inicial
        logger.info("Verificando conexión inicial...")
        response = printer.sendCommand(0x0101, [])  # Comando de estado
        logger.info("Conexión inicial exitosa. Respuesta: %s" % str(response))
        
        # Simular desconexión
        logger.info("\n=== Simulando desconexión física de la impresora ===")
        logger.info("Por favor, desconecte la impresora y espere...")
        time.sleep(10)  # Dar tiempo para desconectar
        
        # Intentar operación durante la desconexión
        try:
            logger.info("Intentando operación con impresora desconectada...")
            response = printer.sendCommand(0x0101, [])  # Esto debería fallar
            logger.warning("ADVERTENCIA: Se esperaba un error pero la operación tuvo éxito")
        except Exception as e:
            logger.info("Error esperado al operar con impresora desconectada: %s" % str(e))
        
        # Simular reconexión
        logger.info("\n=== Simulando reconexión de la impresora ===")
        logger.info("Por favor, conecte la impresora de nuevo...")
        
        # Esperar y verificar reconexión automática
        max_attempts = 5
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info("Intento %d/%d de verificar reconexión..." % (attempt, max_attempts))
                response = printer.sendCommand(0x0101, [])  # Comando de estado
                logger.info("¡Reconexión exitosa en el intento %d! Respuesta: %s" % (attempt, str(response)))
                return True
            except Exception as e:
                logger.warning("Intento %d fallado: %s" % (attempt, str(e)))
                time.sleep(2)  # Esperar antes de reintentar
        
        logger.error("No se pudo reconectar después de varios intentos")
        return False
        
    except Exception as e:
        logger.error("Error en la prueba de reconexión: %s" % str(e))
        return False

if __name__ == "__main__":
    print("=== Prueba de Conexión USB y Reconexión Automática ===\n")
    
    # Ejecutar pruebas
    usb_ok = test_usb_detection()
    
    if usb_ok:
        print("\n¿Desea continuar con las pruebas de conexión con la impresora? (s/n): "),
        if raw_input().strip().lower() == 's':
            printer_ok = test_printer_connection()
            
            if printer_ok:
                print("\n¿Desea probar la reconexión automática? (s/n): "),
                if raw_input().strip().lower() == 's':
                    test_reconnection()
    
    print("\n=== Pruebas completadas ===")
