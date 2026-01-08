# Repositorio del Trabajo de Fin de Grado

## Descripción
Este repositorio contiene el código y los archivos de configuración utilizados en el desarrollo del prototipo del Trabajo de Fin de Grado. 
El laboratorio se compone de dos Raspberry Pi Pico 2W y sensores, una Raspberry Pi como gateway y un portátil para la parte de supervisión.

## Estructura
El contenido se organiza por componentes del sistema:

- `Pi_Pico/`: código de las Raspberry Pi Pico 2W (sensores y publicación por MQTT).
- `Raspberry_PI4/`: gateway OT (broker Mosquitto y bridges serial a Modbus).
- `Laptop_Scada/`: portátil (Node-RED y scripts/pruebas de cliente Modbus y MQTT).

## Licencia
Este repositorio forma parte de un Trabajo de Fin de Grado y se publica bajo la licencia **Creative Commons Reconocimiento-NoComercial-SinObraDerivada 3.0 España**.

## Reproducibilidad
Para reproducir correctamente el entorno del proyecto, es necesario seguir las indicaciones incluidas en el documento principal del TFG y los Anexos, donde se detallan los pasos para montar el laboratorio, configurar los servicios y ejecutar las pruebas.

Como referencia rápida, el laboratorio utiliza:
- MQTT (Mosquitto) en el puerto `1883`.
- Modbus/TCP en los puertos `5020` (temperatura) y `5021` (Volt).

## Nota
La memoria, anexos y presentación no se incluyen en este repositorio para mantenerlo ligero. Se entregan por el canal oficial de la asignatura.
