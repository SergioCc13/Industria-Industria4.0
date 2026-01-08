from machine import Pin
class MCP3008:
    def __init__(self, spi, cs, vref=3.3):
        self.spi=spi; self.cs=cs; self.vref=vref
        self.cs.value(1)
    def read_raw(self, ch):
        assert 0 <= ch <= 7
        tx=bytearray([0x01, 0x80 | (ch<<4), 0x00]); rx=bytearray(3)
        self.cs.value(0); self.spi.write_readinto(tx, rx); self.cs.value(1)
        return ((rx[1] & 0x03) << 8) | rx[2]
