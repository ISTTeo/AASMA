import pickle
metrics = open("savedMetrics.pickle","rb")
metrics = pickle.load(metrics)


print(metrics)
oldNames = ["'RndBot'","'TurtleBot'","'RLBot1'","'RLBot2'"]
newNames = ["Rnd","T","RL1","RL2"]

newMetrics = {}
latex = []
for metric in metrics.keys():
    newMetrics[metric] = {}
    for key in metrics[metric]:
        newKey = key[1:]
        newKey = newKey[:-1]
        for i in range(len(oldNames)):
            newKey = newKey.replace(oldNames[i],newNames[i])
        
        newMetrics[metric][newKey] = metrics[metric][key]


for key in newMetrics.keys():

    metric = newMetrics[key]

    linesSingle = []
    linesSingle.append("\\begin{table}[H]")
    linesSingle.append("\\begin{tabular}{|c|c|c|c|c|}")
    linesSingle.append("\\hline")

    linesComb = []
    linesComb.append("\\begin{table}[H]")
    linesComb.append("\\begin{tabular}{|c|c|c|c|c|}")
    linesComb.append("\\hline")
    for i in range(len(metric["RL1"])+1):
        if(i==0):
            #headers = []
            headersSingle = "\\textbf{Interval}"
            headersComb = "\\textbf{Interval}"
            for cName in metric.keys():
                if(len(metric[cName]) != 0):
                    if(len(cName) <= len("RL1")):
                        headersSingle += " & \\textbf{"  + cName + "}"
                    else:
                        headersComb += " & \\textbf{"  + cName + "}"
            headersSingle += " \\\\ \\hline"
            headersComb += " \\\\ \\hline"
            linesSingle.append(headersSingle)
            linesComb.append(headersComb)
        else:
            index = i-1
            
            lineSingle = "\\textbf{" + str(i) + "}"
            lineComb = "\\textbf{" + str(i) + "}"
            for cName in metric.keys():
                if(len(metric[cName]) != 0):
                    if(len(cName) <= len("RL1")):
                        lineSingle += " & " + str(metric[cName][index]) + "\\%"
                    else:
                        lineComb += " & " + str(metric[cName][index]) + "\\%"
            lineSingle += " \\\\ \\hline"
            linesSingle.append(lineSingle)

            lineComb += " \\\\ \\hline"
            linesComb.append(lineComb)
    
    captionSingle = "\\caption{\\label{tab:" + str(key) + "single}" + str(key) + " for single agents}"
    captionComb = "\\caption{\\label{tab:" + str(key) + "comb}" + str(key) + " for combinations of agents}"

    linesSingle.append("\\end{tabular}")
    linesSingle.append(captionSingle)
    linesSingle.append("\\end{table}")
    linesComb.append("\\end{tabular}")
    linesComb.append(captionComb)
    linesComb.append("\\end{table}")

    print("'-------------------'" + key + '-------------------')
    print()
    for l in linesSingle:
        print(l)
    print()
    for l in linesComb:
        print(l)

    print()

    """ metricLatex = []
    if(len(lineSingle) != 0):
        metricLatex.append(lineSingle)
    if(len(lineComb) != 0):
        metricLatex.append(linesComb)
    latex.append(metricLatex)
     """

""" keys = list(newMetrics.keys())

for ikey in range(len(keys)):
    print(str(ikey) + " - " + keys[ikey])

x = int(input("Enter number:"))

toPrint = latex[x]
print(toPrint) """
""" for lines in toPrint:
    for l in lines:
        print(l) """
