# -*- coding: utf-8 -*-
import json, threading, logging, time, glob
import serial
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)

PICO_PORT = r"/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_148736bce176a80d-if00"

BAUD      = 115200
BIND_ADDR = ("0.0.0.0", 5021)
UNIT_ID   = 1

di = ModbusSequentialDataBlock(0, [0]*16)
co = ModbusSequentialDataBlock(0, [0]*16)
ir = ModbusSequentialDataBlock(0, [0]*64)
hr = ModbusSequentialDataBlock(0, [0]*64)

store = ModbusSlaveContext(di=di, co=co, ir=ir, hr=hr)
context = ModbusServerContext(slaves={UNIT_ID: store}, single=False)

def reader():
    logging.info("Abriendo puerto serie: %s", PICO_PORT)
    while True:
        try:
            with serial.Serial(PICO_PORT, BAUD, timeout=2) as s:
                for raw in s:
                    try:
                        msg = json.loads(raw.decode(errors="ignore").strip() or "{}")
                        v = int(msg.get("ch0_raw", 0))
                        store.setValues(4, 0, [v])
                        store.setValues(3, 0, [v])
                    except Exception as e:
                        logging.debug("Linea invalida %r (%s)", raw, e)
        except Exception as e:
            logging.error("Error serie: %s (reintento en 1s)", e)
            time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    threading.Thread(target=reader, daemon=True).start()
    logging.info("Servidor Modbus/TCP en %s:%s (UNIT=%s, IR0/HR0 = ch0_raw)",
                 BIND_ADDR[0], BIND_ADDR[1], UNIT_ID)
    StartTcpServer(context, address=BIND_ADDR)
