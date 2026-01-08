from pymodbus.client.sync import ModbusTcpClient
import time

client = ModbusTcpClient("192.168.10.10", port=5021)

if client.connect():
    print("Conectado al servidor Modbus")
    while True:
        rr = client.read_input_registers(0, 1, unit=1)
        if not rr.isError():
            print("IR0 =", rr.registers[0])
        else:
            print("Error de lectura")
        time.sleep(1)
else:
    print("No se pudo conectar")

client.close() 