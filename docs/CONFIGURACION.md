# Guía Detallada de Configuración de Impresora Fiscal

## Índice
1. [Configuración Básica](#configuración-básica)
2. [Parámetros del Archivo config.ini](#parámetros-del-archivo-configini)
3. [Configuración de Red](#configuración-de-red)
4. [Permisos de Puerto USB](#permisos-de-puerto-usb)
5. [Configuración Avanzada](#configuración-avanzada)
6. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

## Configuración Básica

### Requisitos Previos
- Python 2.7
- Acceso de superusuario (sudo)
- Conexión física a la impresora fiscal vía USB

### Instalación de Dependencias

```bash
# Actualizar lista de paquetes
sudo apt-get update

# Instalar dependencias del sistema
sudo apt-get install -y python-pip python-serial

# Instalar dependencias de Python
pip install -r requirements_fiscal.txt
```

## Parámetros del Archivo config.ini

El archivo `config.ini` contiene la configuración principal de la impresora fiscal. A continuación se detallan los parámetros disponibles:

```ini
[IMPRESORA_FISCAL]
# Ruta al dispositivo de la impresora (generalmente /dev/ttyUSB0 o COM1 en Windows)
path = /dev/ttyUSB0

# Velocidad de comunicación en baudios
speed = 9600

# Controlador a utilizar (Hasar, Epson, etc.)
driver = Hasar

# (Opcional) Tipo de documento fiscal (T=tique, F=factura, etc.)
tipo_cbte = T

# (Opcional) Tipo de documento del cliente (80=CUIT, 96=DNI, etc.)
tipo_doc = 80

# (Opcional) Tipo de responsable fiscal (1=Responsable Inscripto, etc.)
tipo_responsable = 1
```

## Configuración de Red

Si necesita acceder a la impresora desde otra máquina en la red:

1. Asegúrese de que el puerto 12000 esté abierto en el firewall:
   ```bash
   sudo ufw allow 12000/tcp
   ```

2. Para exponer el servicio en la red, modifique la configuración en `server.py`:
   ```python
   app.listen(12000, '0.0.0.0')  # Escucha en todas las interfaces de red
   ```

## Permisos de Puerto USB

Para evitar problemas de permisos con el puerto USB, siga estos pasos:

1. Agregue su usuario al grupo dialout:
   ```bash
   sudo usermod -a -G dialout $USER
   ```

2. Establezca los permisos correctos en el dispositivo:
   ```bash
   sudo chmod 666 /dev/ttyUSB0
   ```

3. Para hacer este cambio permanente, cree un archivo udev rule:
   ```bash
   echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="067b", MODE="0666"' | sudo tee /etc/udev/rules.d/99-impresora-fiscal.rules
   sudo udevadm control --reload-rules
   ```

## Configuración Avanzada

### Variables de Entorno

Puede sobrescribir la configuración usando variables de entorno:

```bash
export FISCAL_PRINTER_PORT=/dev/ttyUSB0
export FISCAL_PRINTER_BAUDRATE=9600
export FISCAL_PRINTER_DRIVER=Hasar
```

### Configuración de Logs

Para habilitar logs detallados, modifique el nivel de log en `server.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Solución de Problemas Comunes

### La impresora no responde

1. Verifique la conexión USB
2. Confirme que la impresora esté encendida
3. Verifique los permisos del puerto:
   ```bash
   ls -l /dev/ttyUSB0
   ```

### Error de permisos

Si ve un error como `Permission denied: '/dev/ttyUSB0'`:

```bash
# Verificar el grupo actual del puerto
ls -l /dev/ttyUSB0

# Agregar su usuario al grupo correspondiente (generalmente dialout)
sudo usermod -a -G dialout $USER

# O cambiar los permisos temporalmente
sudo chmod 666 /dev/ttyUSB0
```

### La impresora responde lentamente

1. Intente reducir la velocidad de comunicación en `config.ini`
2. Verifique la calidad del cable USB
3. Asegúrese de que no haya interferencias electromagnéticas

### Reiniciar el servicio

Si necesita reiniciar el servicio:

```bash
# Detener el contenedor si está en uso
docker stop fiscal-printer

# Iniciar el servicio manualmente
python server.py
```

Para más ayuda, consulte la documentación del fabricante de su impresora fiscal o abra un issue en el repositorio del proyecto.
