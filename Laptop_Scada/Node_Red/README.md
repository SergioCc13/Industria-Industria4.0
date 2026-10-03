# Node-RED (laptop)

This folder contains the Node-RED flow I used on the laptop for the supervision/visualization part
of the thesis lab.
**Important:** Node-RED ran on the laptop, not on the Raspberry Pi. The Raspberry Pi acts as the
gateway (Mosquitto + Modbus bridges), and the laptop is the HMI/supervision side.

---

## Contents

- `flows.json`: export of the Node-RED flow used in the project.

---

## What this flow uses

My lab had these pieces:

- **MQTT (Mosquitto on the Raspberry Pi):**
  - Broker: `192.168.0.143`
  - Port: `1883`
  - Topics: `temperatura`, `volt`
  - Test topic: `tf/sensor/analog`

- **Modbus/TCP (gateway on the Raspberry Pi):**
  - `5020/tcp` (temperature)
  - `5021/tcp` (ADC)

> Note: IP addresses may change if the DHCP lease or the network changes. If you import the flow on
> another network, you will usually only need to update the IPs.

---

## Requirements (laptop)

- **Node.js** and **Node-RED** installed.
- Connected to the same network as the lab.
- Services running:
  - Mosquitto on the Raspberry Pi (1883)
  - Modbus bridges (5020/5021) if you use the OT/Modbus part

---

## Exporting the JSON file

To export `flows.json` again:

1. Open Node-RED in the browser: `http://localhost:1880`
2. Open the menu (≡) and select **Export**
3. Export the flow (or tab) as JSON
4. Save it as `flows.json` in this folder

---

## Importing the flow (`flows.json`)

1. Start Node-RED:

   ```bash
   node-red
   ```

2. Open the editor in the browser: `http://localhost:1880`

3. Import the flow:
   - Menu (≡) → **Import** → **Clipboard**
   - Paste the contents of `flows.json`
   - Click **Import**, then **Deploy**
