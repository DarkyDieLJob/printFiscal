#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import logging
from serial import SerialException

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ConnectionManager')

class ConnectionError(Exception):
    """Excepción para errores de conexión"""
    pass

class ConnectionManager(object):
    """
    Maneja la conexión con la impresora fiscal con reconexión automática.
    """
    
    def __init__(self, port, baudrate=9600, retry_interval=5):
        """
        Inicializa el manejador de conexión.
        
        Args:
            port (str): Puerto serial o 'auto' para detección automática
            baudrate (int): Velocidad en baudios (por defecto: 9600)
            retry_interval (int): Segundos entre reintentos de conexión
        """
        self.port = port
        self.baudrate = baudrate
        self.retry_interval = retry_interval
        self.serial_conn = None
        self.running = True
        
        # Iniciar la conexión
        self._connect()
    
    def _connect(self):
        """Establece la conexión con la impresora"""
        while self.running:
            try:
                if self.serial_conn is not None:
                    try:
                        self.serial_conn.close()
                    except:
                        pass
                
                logger.info("Conectando a %s..." % self.port)
                self.serial_conn = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1,
                    write_timeout=1
                )
                
                logger.info("Conexión exitosa con %s" % self.port)
                return True
                
            except (SerialException, OSError) as e:
                logger.error("Error de conexión: %s" % str(e))
                logger.info("Reintentando en %d segundos..." % self.retry_interval)
                time.sleep(self.retry_interval)
            except Exception as e:
                logger.error("Error inesperado: %s" % str(e))
                time.sleep(self.retry_interval)
    
    def ensure_connection(self):
        """
        Verifica la conexión y la restablece si es necesario.
        
        Returns:
            bool: True si la conexión está activa, False en caso contrario
        """
        if self.serial_conn is None or not self.serial_conn.isOpen():
            logger.warning("Conexión perdida, intentando reconectar...")
            return self._connect()
        return True
    
    def write(self, data):
        """
        Envía datos a través de la conexión serial.
        
        Args:
            data (bytes): Datos a enviar
            
        Returns:
            int: Número de bytes escritos
        """
        if not self.ensure_connection():
            raise ConnectionError("No se pudo establecer la conexión con la impresora")
            
        try:
            return self.serial_conn.write(data)
        except (SerialException, OSError) as e:
            logger.error("Error al escribir en el puerto serial: %s" % str(e))
            self.serial_conn = None
            raise ConnectionError("Error de comunicación con la impresora")
    
    def read(self, size=1):
        """
        Lee datos de la conexión serial.
        
        Args:
            size (int): Número de bytes a leer
            
        Returns:
            bytes: Datos leídos
        """
        if not self.ensure_connection():
            raise ConnectionError("No se pudo establecer la conexión con la impresora")
            
        try:
            return self.serial_conn.read(size)
        except (SerialException, OSError) as e:
            logger.error("Error al leer del puerto serial: %s" % str(e))
            self.serial_conn = None
            raise ConnectionError("Error de comunicación con la impresora")
    
    def close(self):
        """Cierra la conexión"""
        self.running = False
        if self.serial_conn is not None:
            try:
                self.serial_conn.close()
            except:
                pass
            self.serial_conn = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
