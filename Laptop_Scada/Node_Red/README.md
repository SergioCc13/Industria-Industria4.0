# Node-RED (portátil)

En esta carpeta dejo el flujo de Node-RED que utilicé en el portátil para la parte de supervisión/visualización del laboratorio del TFG.
**Importante:** Node-RED lo tuve corriendo en el portátil (no en la Raspberry Pi). La Raspberry Pi hace de gateway (Mosquitto + bridges Modbus),
y el portátil es la parte de “HMI/supervisión”.
---

## Contenido

- `flows.json`: export del flujo de Node-RED usado en el proyecto.
---

## Qué usa este flujo

En mi caso, el laboratorio tenía estas piezas:

- **MQTT (Mosquitto en la Raspberry Pi):**
  - Broker: `192.168.0.143`
  - Puerto: `1883`
  - Topics usados: `temperatura`, `volt`
  - Topic de pruebas: `tf/sensor/analog`

- **Modbus/TCP (gateway en la Raspberry Pi):**
  - `5020/tcp` (temperatura)
  - `5021/tcp` (ADC)

> Nota: la IP puede cambiar si cambia el DHCP/red. Si importas el flujo en otra red, lo normal es que solo tengas que actualizar IPs.
---

## Requisitos (portátil)

- Tener instalado **Node.js** y **Node-RED**.
- Estar conectado a la misma red que el laboratorio.
- Que los servicios estén levantados:
  - Mosquitto en la Raspberry Pi (1883)
  - Bridges Modbus (5020/5021) si se usa la parte OT/Modbus
---

## Exportar el archivo JSON

Si en algún momento necesito volver a sacar el `flows.json`:

1. Abrir Node-RED en el navegador: `http://localhost:1880`
2. Menú (≡), seleccionar **Export**
3. Exportar el flow (o pestaña) a JSON
4. Guardarlo como `flows.json` en esta carpeta
---

## Importar el flujo (`flows.json`)

1. Arrancar Node-RED:
   node-red
   
2. Abrir el editor en el navegador:
http://localhost:1880

3. Importar el flow:
-Menú (≡) → Import → Clipboard.
-Copiar y pegar el contenido de "flows.json".
-Pulsar Import y después Deploy.