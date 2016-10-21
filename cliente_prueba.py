from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:8000')

proxy.ping()

proxy.cambia_direccion('0', 1)
proxy.yo_juego()
proxy.estado_del_juego()
