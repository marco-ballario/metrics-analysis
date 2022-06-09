import json
import glob
import os
import csv

f = open('./FastCSV_ABC.csv', 'w')
writer = csv.writer(f)
writer.writerow(["File","A","B","C","Magnitude"])
assignments = list()
branches = list()
conditions = list()
magnitude = list()
for filename in glob.iglob("data" + '**/**/*.json', recursive=True):
	#print(filename)
	with open(filename,"r") as file:
		jsonData = json.load(file)
		assignments.append(('%.3f'%float(jsonData["metrics"]["abc"]["assignments"])))
		branches.append(('%.3f'%float(jsonData["metrics"]["abc"]["branches"])))
		conditions.append(('%.3f'%float(jsonData["metrics"]["abc"]["conditions"])))
		magnitude.append(('%.3f'%float(jsonData["metrics"]["abc"]["magnitude"])))
		#print("Datatype of variable: ", type(jsonData))
		#for i in jsonData:
		v = [os.path.basename(jsonData["name"]), '%.0f'%(jsonData["metrics"]["abc"]["assignments"]), '%.0f'%(jsonData["metrics"]["abc"]["branches"]), '%.0f'%(jsonData["metrics"]["abc"]["conditions"]), '%.3f'%(jsonData["metrics"]["abc"]["magnitude"])]
		writer.writerow(v)
		print(os.path.basename(jsonData["name"]))
		print(jsonData["metrics"]["abc"]["magnitude"])
assignments = [float(x) for x in assignments]
branches = [float(x) for x in branches]
conditions = [float(x) for x in conditions]
magnitude = [float(x) for x in magnitude]
writer.writerow(["MIN",'%.0f'%min(assignments),'%.0f'%min(branches),'%.0f'%min(conditions),min(magnitude)])
writer.writerow(["MAX",'%.0f'%max(assignments),'%.0f'%max(branches),'%.0f'%max(conditions),max(magnitude)])
print(conditions)
writer.writerow(["AVG",'%.3f'%(sum(assignments)/len(assignments)),'%.3f'%(sum(branches)/len(branches)),'%.3f'%(sum(conditions)/len(conditions)),'%.3f'%(sum(magnitude)/len(magnitude))])
f.close()