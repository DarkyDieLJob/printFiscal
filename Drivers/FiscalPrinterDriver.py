#!/usr/bin/env python
# -*- coding: utf-8 -*-
from DriverInterface import DriverInterface
import sys
import os
import logging
import time

# Agregar el directorio raíz al path para importar ConnectionManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ConnectionManager import ConnectionManager, ConnectionError
from USBManager import USBManager

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FiscalPrinterDriver')

def debugEnabled(*args):
    logger.debug(" ".join([str(arg) for arg in args]))

def debugDisabled(*args):
    pass

debug = debugDisabled

class PrinterException(Exception):
    pass

class UnknownServerError(PrinterException):
    errorNumber = 1

class ComunicationError(PrinterException):
    errorNumber = 2

class PrinterStatusError(PrinterException):
    errorNumber = 3

class FiscalStatusError(PrinterException):
    errorNumber = 4

ServerErrors = [UnknownServerError, ComunicationError, PrinterStatusError, FiscalStatusError]

class ProxyError(PrinterException):
    errorNumber = 5

class FiscalPrinterDriver(DriverInterface):
    WAIT_TIME = 10
    RETRIES = 4
    WAIT_CHAR_TIME = 0.1
    NO_REPLY_TRIES = 200
    CONNECTION_RETRY_INTERVAL = 5  # segundos entre reintentos de conexión

    def __init__(self, path='auto', speed=9600):
        """
        Inicializa el driver de la impresora fiscal.
        
        Args:
            path (str): Ruta del puerto serial o 'auto' para detección automática
            speed (int): Velocidad en baudios (por defecto: 9600)
        """
        self._port = path
        self._baudrate = speed
        self._connection = None
        self._init_connection()
        self._initSequenceNumber()
        
    def _init_connection(self):
        """Inicializa la conexión con la impresora"""
        if self._port.lower() == 'auto':
            # Usar detección automática de USB
            usb_manager = USBManager()
            device = usb_manager.wait_for_device()
            if not device:
                raise ComunicationError("No se pudo detectar la impresora fiscal")
            self._port = device
            logger.info("Usando puerto detectado automáticamente: %s" % self._port)
        
        # Iniciar la conexión con reintentos infinitos
        self._connection = ConnectionManager(
            port=self._port,
            baudrate=self._baudrate,
            retry_interval=self.CONNECTION_RETRY_INTERVAL
        )
    
    def close(self):
        """Cierra la conexión con la impresora"""
        if hasattr(self, '_connection') and self._connection is not None:
            try:
                self._connection.close()
            except Exception as e:
                logger.error("Error al cerrar la conexión: %s" % str(e))
            self._connection = None

    def sendCommand(self, commandNumber, fields, skipStatusErrors=False):
        """
        Envía un comando a la impresora fiscal.
        
        Args:
            commandNumber (int): Número de comando
            fields (list): Lista de campos del comando
            skipStatusErrors (bool): Si es True, omite la verificación de errores de estado
            
        Returns:
            list: Respuesta de la impresora
            
        Raises:
            ComunicationError: Si hay un error de comunicación con la impresora
        """
        # Asegurar que la conexión esté activa
        if not hasattr(self, '_connection') or self._connection is None:
            self._init_connection()
        
        # Convertir campos a bytes si es necesario
        encoded_fields = []
        for field in fields:
            if isinstance(field, str):
                encoded_fields.append(field.encode("latin-1", 'ignore'))
            else:
                encoded_fields.append(field)
        
        # Construir el mensaje
        message = bytearray()
        message.append(0x02)  # STX
        message.append(self._sequenceNumber)
        message.append(commandNumber)
        
        if encoded_fields:
            message.append(0x1c)  # Separador
            
        # Agregar campos separados por 0x1c
        for i, field in enumerate(encoded_fields):
            if i > 0:
                message.append(0x1c)  # Separador entre campos
            if isinstance(field, str):
                message.extend(bytearray(field))
            else:
                message.extend(field)
            
        message.append(0x03)  # ETX
        
        # Calcular checksum
        check_sum = sum(ord(c) for c in message) if isinstance(message, str) else sum(message)
        check_sum_hex = ("0000" + hex(check_sum)[2:])[-4:].upper()
        message.extend(bytearray(check_sum_hex, 'ascii'))
        
        # Enviar mensaje y obtener respuesta
        try:
            reply = self._sendMessage(message)
            self._incrementSequenceNumber()
            return self._parseReply(reply, skipStatusErrors)
        except ConnectionError as e:
            logger.error("Error de conexión: %s" % str(e))
            # Intentar reconectar
            self._init_connection()
            # Reintentar el envío una vez más
            reply = self._sendMessage(message)
            self._incrementSequenceNumber()
            return self._parseReply(reply, skipStatusErrors)




    def _write(self, data):
        """
        Envía datos a la impresora.
        
        Args:
            data (bytes): Datos a enviar
            
        Raises:
            ComunicationError: Si hay un error de comunicación
        """
        debug("_write " + " ".join(["%02x" % (ord(b) if isinstance(b, str) else b) for b in data]))
        try:
            if not hasattr(self, '_connection') or self._connection is None:
                self._init_connection()
            return self._connection.write(data)
        except Exception as e:
            logger.error("Error al escribir en la impresora: %s" % str(e))
            raise ComunicationError("Error de comunicación: %s" % str(e))

    def _read(self, count):
        """
        Lee datos de la impresora.
        
        Args:
            count (int): Número de bytes a leer
            
        Returns:
            bytes: Datos leídos
            
        Raises:
            ComunicationError: Si hay un error de comunicación
        """
        try:
            if not hasattr(self, '_connection') or self._connection is None:
                self._init_connection()
            data = self._connection.read(count)
            debug("_read " + " ".join(["%02x" % (ord(b) if isinstance(b, str) else b) for b in data]))
            return data
        except Exception as e:
            logger.error("Error al leer de la impresora: %s" % str(e))
            raise ComunicationError("Error de comunicación: %s" % str(e))

    def __del__(self):
        if hasattr(self, "_connection"):
            try:
                self._connection.close()
            except Exception as e:
                logger.error("Error en el destructor: %s" % str(e))

    def _parseReply( self, reply, skipStatusErrors ):
        r = reply[4:-1] # Saco STX <Nro Seq> <Nro Comando> <Sep> ... ETX
        fields = r.split( chr(28) )
        printerStatus = fields[0]
        fiscalStatus = fields[1]
        if not skipStatusErrors:
            self._parsePrinterStatus( printerStatus )
            self._parseFiscalStatus( fiscalStatus )
        return fields

    def _parsePrinterStatus(self, printerStatus):
        x = int(printerStatus, 16)
        for value, message in self.printerStatusErrors:
            if (value & x) == value:
                raise PrinterStatusError(message)

    def _parseFiscalStatus(self, fiscalStatus):
        x = int(fiscalStatus, 16)
        for value, message in self.fiscalStatusErrors:
            if (value & x) == value:
                raise FiscalStatusError(message)

    

    def _checkReplyBCC( self, reply, bcc ):
        debug( "reply", reply, [ord(x) for x in reply] )
        checkSum = sum( [ord(x) for x in reply ] )
        debug( "checkSum", checkSum )
        checkSumHexa = ("0000" + hex(checkSum)[2:])[-4:].upper()
        debug( "checkSumHexa", checkSumHexa )
        debug( "bcc", bcc )
        return checkSumHexa == bcc.upper()



