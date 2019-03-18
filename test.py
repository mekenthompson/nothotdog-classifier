########### Python 2.7 #############
import httplib, urllib, base64

TRAINING_KEY = os.environ["TRAINING_KEY"]
PREDICTION_KEY= os.environ["PREDICTION_KEY"]

headers = {
    # Request headers
    'Training-Key': '',
    'Training-key': '{subscription key}',
}

params = urllib.urlencode({
    # Request parameters
    'threshold': '{number}',
    'overlapThreshold': '{number}',
})

try:
    conn = httplib.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
    conn.request("GET", "/customvision/v2.2/Training/projects/{projectId}/iterations/{iterationId}/performance?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Training-Key': '',
    'Training-key': '{subscription key}',
}

params = urllib.parse.urlencode({
    # Request parameters
    'threshold': '{number}',
    'overlapThreshold': '{number}',
})

try:
    conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
    conn.request("GET", "/customvision/v2.2/Training/projects/{projectId}/iterations/{iterationId}/performance?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################