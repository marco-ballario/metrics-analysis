import json
import glob
for filename in glob.iglob("data" + '**/**/*.json', recursive=True):
	#print(filename)
	with open(filename,"r") as file:
		jsonData = json.load(file)
		#print("Datatype of variable: ", type(jsonData))
		#for i in jsonData:
		print(jsonData["name"])
		print(jsonData["metrics"]["wmc"])

