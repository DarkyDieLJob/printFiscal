#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import re
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('USBManager')

class USBManager(object):
    """
    Maneja la detección de dispositivos USB compatibles con la impresora fiscal.
    """
    
    def __init__(self, vendor_id='0403', product_id='6001'):
        """
        Inicializa el gestor de dispositivos USB.
        
        Args:
            vendor_id (str): ID del vendedor (por defecto: '0403' para FTDI)
            product_id (str): ID del producto (por defecto: '6001' para FT232)
        """
        self.vendor_id = vendor_id.lower()
        self.product_id = product_id.lower()
    
    def find_usb_device(self):
        """
        Busca un dispositivo USB compatible.
        
        Returns:
            str: Ruta del dispositivo (ej: '/dev/ttyUSB0') o None si no se encuentra
        """
        try:
            # Listar dispositivos USB
            result = subprocess.check_output(['lsusb'])
            
            # Buscar dispositivos que coincidan con el vendedor y producto
            for line in result.split('\n'):
                if not line.strip():
                    continue
                    
                # Extraer información del dispositivo
                match = re.search(r'ID ([0-9a-fA-F]{4}):([0-9a-fA-F]{4})', line)
                if match:
                    vendor = match.group(1).lower()
                    product = match.group(2).lower()
                    
                    if vendor == self.vendor_id and product == self.product_id:
                        # Buscar el puerto tty asociado
                        try:
                            ports = subprocess.check_output(['ls', '/dev/ttyUSB*'], 
                                                         stderr=open(os.devnull, 'w')).split()
                            if ports:
                                return ports[0]  # Devolver el primer puerto encontrado
                        except subprocess.CalledProcessError:
                            pass
            
            return None
            
        except Exception as e:
            logger.error("Error al buscar dispositivos USB: %s" % str(e))
            return None
    
    def wait_for_device(self, check_interval=5):
        """
        Espera hasta que se detecte un dispositivo USB compatible.
        
        Args:
            check_interval (int): Segundos entre verificaciones
            
        Returns:
            str: Ruta del dispositivo cuando se encuentra
        """
        logger.info("Esperando por dispositivo USB compatible...")
        
        while True:
            device = self.find_usb_device()
            if device:
                logger.info("Dispositivo detectado en %s" % device)
                return device
                
            logger.debug("Dispositivo no encontrado, reintentando en %d segundos..." % check_interval)
            time.sleep(check_interval)
