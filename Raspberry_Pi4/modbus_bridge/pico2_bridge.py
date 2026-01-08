# -*- coding: utf-8 -*-
import json, threading, logging, time, serial
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)

PICO_PORT = r"/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_a8e33bad38be2fd1-if00"

BAUD      = 115200
BIND_ADDR = ("0.0.0.0", 5020)
UNIT_ID   = 1

di = ModbusSequentialDataBlock(0, [0]*16)
co = ModbusSequentialDataBlock(0, [0]*16)
ir = ModbusSequentialDataBlock(0, [0]*64)
hr = ModbusSequentialDataBlock(0, [0]*64)

store = ModbusSlaveContext(di=di, co=co, ir=ir, hr=hr)
context = ModbusServerContext(slaves={UNIT_ID: store}, single=False)

def reader():
    while True:
        try:
            with serial.Serial(PICO_PORT, BAUD, timeout=2) as s:
                for raw in s:
                    try:
                        msg = json.loads(raw.decode(errors="ignore").strip() or "{}")
                        temp = float(msg.get("t", 0.0))
                        # Escalar a décimas para guardarlo en un registro de 16 bits
                        val = int(temp * 10)
                        store.setValues(4, 0, [val])
                        store.setValues(3, 0, [val])
                    except Exception:
                        pass
        except Exception as e:
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=reader, daemon=True).start()
    StartTcpServer(context, address=BIND_ADDR)
