# /lib/umqtt/simple.py
import usocket as socket
import ustruct as struct

class MQTTException(Exception):
    pass

class MQTTClient:
    def __init__(self, client_id, server, port=1883, user=None, password=None, keepalive=60):
        self.client_id = client_id if isinstance(client_id, bytes) else str(client_id).encode()
        self.server = server; self.port = port
        self.user = None if user is None else (user if isinstance(user, bytes) else str(user).encode())
        self.pswd = None if password is None else (password if isinstance(password, bytes) else str(password).encode())
        self.keepalive = keepalive
        self.sock = None
        self.lwt_topic = None; self.lwt_msg = None; self.lwt_retain = 0; self.lwt_qos = 0

    def set_last_will(self, topic, msg, retain=False, qos=0):
        self.lwt_topic = topic if isinstance(topic, bytes) else str(topic).encode()
        self.lwt_msg = msg if isinstance(msg, bytes) else str(msg).encode()
        self.lwt_retain = 1 if retain else 0
        self.lwt_qos = qos

    def _send_varlen(self, n):
        out = bytearray()
        while True:
            b = n & 0x7F; n >>= 7
            if n > 0: b |= 0x80
            out.append(b)
            if n == 0: break
        self.sock.write(out)

    def _send_str(self, s):
        if not isinstance(s, bytes): s = str(s).encode()
        self.sock.write(struct.pack("!H", len(s))); self.sock.write(s)

    def connect(self, clean_session=True):
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock = socket.socket(); self.sock.connect(addr)
        proto_name=b"MQTT"; proto_level=4; flags=0
        if clean_session: flags|=0x02
        if self.user is not None:
            flags|=0x80
            if self.pswd is not None: flags|=0x40
        if self.lwt_topic is not None:
            flags|=0x04 | (self.lwt_qos<<3) | (self.lwt_retain<<5)
        payload_len = 2+len(self.client_id)
        if self.lwt_topic is not None: payload_len += 2+len(self.lwt_topic)+2+len(self.lwt_msg)
        if self.user is not None:
            payload_len += 2+len(self.user)
            if self.pswd is not None: payload_len += 2+len(self.pswd)
        # Fixed header CONNECT (0x10)
        self.sock.write(b"\x10"); self._send_varlen(10 + payload_len)
        # Variable header
        self._send_str(proto_name); self.sock.write(bytes([proto_level, flags])); self.sock.write(b"\x00\x3c")
        # Payload
        self._send_str(self.client_id)
        if self.lwt_topic is not None: self._send_str(self.lwt_topic); self._send_str(self.lwt_msg)
        if self.user is not None:
            self._send_str(self.user)
            if self.pswd is not None: self._send_str(self.pswd)
        resp = self.sock.read(4)
        if not resp or resp[0]!=0x20 or resp[1]!=0x02 or resp[3]!=0x00:
            raise MQTTException("CONNACK error: %s" % (resp,))

    def publish(self, topic, msg, retain=False, qos=0):
        if not isinstance(topic, bytes): topic = str(topic).encode()
        if not isinstance(msg, bytes): msg = str(msg).encode()
        hdr = 0x30 | (0x01 if retain else 0x00)
        self.sock.write(bytes([hdr]))
        rem_len = 2 + len(topic) + len(msg)
        self._send_varlen(rem_len); self._send_str(topic); self.sock.write(msg)

    def disconnect(self):
        try: self.sock.write(b"\xE0\x00")
        except: pass
        try: self.sock.close()
        except: pass
        self.sock = None
