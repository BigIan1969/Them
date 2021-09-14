from http.server import HTTPServer, BaseHTTPRequestHandler
import theminit
import themhttp
import themcontrols

def start():
    #with auger.magic([themcontrols.Expresions]):
    print("""
    Them server is currently running at {0} on port {1}
    Press CTRL-C or CTRL-Break to end process
    """.format('localhost',8000))

    httpd = HTTPServer(('localhost', 8000), themhttp.SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    start()
