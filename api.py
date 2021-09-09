import json
import subprocess

samsung=open('samsung.json', 'r')
samsungs=samsung.read()
response = json.loads(samsungs)

#print(response)

while response["clusterState"]!="ACTIVE":
    subprocess.call("api.sh")
