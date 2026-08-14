from http.server import SimpleHTTPRequestHandler, HTTPServer

server = HTTPSERVER(("", 8080), SimpleHTTPRequestHandler)
print("Serving HTTP on port 8080...")
server.serve_forever()
