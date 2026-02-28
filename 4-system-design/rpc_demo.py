import socket
import json
import threading
import time
import struct

def send_message(sock, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    length_prefix = struct.pack(">I", len(data))
    sock.sendall(length_prefix + data)


def recv_message(sock) -> dict:
    raw_length = _recv_exact(sock, 4)
    if not raw_length:
        return None
    length = struct.unpack(">I", raw_length)[0]
    data = _recv_exact(sock, length)
    return json.loads(data.decode("utf-8"))


def _recv_exact(sock, n: int) -> bytes:
    buffer = b""
    while len(buffer) < n:
        chunk = sock.recv(n - len(buffer))
        if not chunk:
            return None
        buffer += chunk
    return buffer


class RPCServer:

    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        self._registry = {}

    def register(self, func):
        self._registry[func.__name__] = func
        return func

    def _handle_client(self, conn, addr):
        print(f"[SERVER] Connection from {addr}")
        try:
            while True:
                request = recv_message(conn)
                if request is None:
                    break

                method   = request.get("method")
                args     = request.get("args", [])
                kwargs   = request.get("kwargs", {})
                call_id  = request.get("id")

                print(f"[SERVER] Received call  ->  {method}({args}, {kwargs})")

                if method not in self._registry:
                    response = {
                        "id"    : call_id,
                        "result": None,
                        "error" : f"Method '{method}' not found on server"
                    }
                else:
                    try:
                        result = self._registry[method](*args, **kwargs)
                        response = {"id": call_id, "result": result, "error": None}
                    except Exception as exc:
                        response = {"id": call_id, "result": None, "error": str(exc)}

                print(f"[SERVER] Sending result ->  {response['result'] or response['error']}\n")
                send_message(conn, response)

        finally:
            conn.close()
            print(f"[SERVER] Connection closed  {addr}")

    def serve_forever(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        server_sock.listen(5)
        print(f"[SERVER] Listening on {self.host}:{self.port}")
        print(f"[SERVER] Registered methods: {list(self._registry.keys())}\n")

        while True:
            conn, addr = server_sock.accept()
            t = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
            t.start()


class RPCClient:

    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        self._call_counter = 0
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))
        print(f"[CLIENT] Connected to {self.host}:{self.port}\n")

    def _next_id(self):
        self._call_counter += 1
        return self._call_counter

    def call(self, method: str, *args, **kwargs):
        request = {
            "id"    : self._next_id(),
            "method": method,
            "args"  : args,
            "kwargs": kwargs
        }
        print(f"[CLIENT] Calling remote method  ->  {method}({args}, {kwargs})")
        send_message(self._sock, request)
        response = recv_message(self._sock)

        if response["error"]:
            raise RuntimeError(f"Remote error: {response['error']}")

        print(f"[CLIENT] Got result             ->  {response['result']}\n")
        return response["result"]

    def close(self):
        self._sock.close()

def setup_server() -> RPCServer:
    server = RPCServer()

    @server.register
    def add(a, b):
        return a + b

    @server.register
    def multiply(a, b):
        return a * b

    @server.register
    def factorial(n):
        if n < 0:
            raise ValueError("Factorial undefined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @server.register
    def reverse_string(text):
        return text[::-1]

    @server.register
    def word_count(sentence):
        return len(sentence.split())

    @server.register
    def celsius_to_fahrenheit(celsius):
        return celsius * 9 / 5 + 32

    return server


def run_server():
    server = setup_server()
    server.serve_forever()


def run_client():
    time.sleep(0.5)
    client = RPCClient()

    print("=" * 60)
    print("  REMOTE PROCEDURE CALL  —  LIVE DEMONSTRATION")
    print("=" * 60)
    print()

    print("--- Arithmetic ---")
    client.call("add", 42, 58)
    client.call("multiply", 7, 6)

    print("--- Math ---")
    client.call("factorial", 10)

    print("--- String operations ---")
    client.call("reverse_string", "Remote Procedure Call")
    client.call("word_count", "The quick brown fox jumps over the lazy dog")

    print("--- Unit conversion ---")
    client.call("celsius_to_fahrenheit", 100)

    print("--- Error propagation across the network ---")
    try:
        client.call("factorial", -5)
    except RuntimeError as e:
        print(f"[CLIENT] Caught remote exception: {e}\n")

    try:
        client.call("non_existent_method", 1, 2)
    except RuntimeError as e:
        print(f"[CLIENT] Caught remote exception: {e}\n")

    client.close()
    print("=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    run_client()