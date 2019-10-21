import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen

from arwenlib import startArwenClient



client = startArwenClient()

respPing = client.pingArwenClient()
print(respPing)

respTime = client.timeArwenClient()
print(respTime)

