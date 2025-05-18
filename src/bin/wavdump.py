import urllib.request, urllib.error, urllib.parse
import sys

url = sys.argv[1]
req = urllib.request.Request(url)
handler = urllib.request.urlopen(req)
buffer = handler.read()
sys.stdout.write(buffer)
sys.stdout.flush()
