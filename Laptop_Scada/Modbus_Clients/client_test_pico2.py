from pymodbus.client.sync import ModbusTcpClient
import time

HOST, PORT, UNIT = "192.168.10.10", 5020, 1
ADDRESS, COUNT = 0, 1
INTERVAL_S = 2.0

c = ModbusTcpClient(HOST, port=PORT, timeout=3)

try:
    while True:
        if not c.connect():
            time.sleep(INTERVAL_S)
            continue
        r = c.read_input_registers(ADDRESS, COUNT, unit=UNIT)
        if r and not r.isError():
            val = r.registers[0] / 10.0
            print(f"{val:.1f}°C")   # divide entre 10 y muestra 1 decimal, sin comas extra
        else:
            print("Error de lectura")
        time.sleep(INTERVAL_S)
except KeyboardInterrupt:
    pass
finally:
    c.close()
