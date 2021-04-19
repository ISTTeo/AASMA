FILENAME = "FOREX_EURUSD_1H_ASK"
f = open(FILENAME + ".csv", "r")
k = open(FILENAME + "DAILY.csv", "w")
lines = f.readlines()
for i in range(len(lines)):
    if(i==0 or "00:00:00.000" in lines[i]):
        k.write(lines[i])
    