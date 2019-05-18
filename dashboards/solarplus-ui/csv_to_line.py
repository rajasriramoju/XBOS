import pandas as pd
#convert csv's to line protocol

#convert sample data to line protocol (with nanosecond precision)
df = pd.read_csv("Price.csv")
lines = [
           "Time," + str(df["Time"][d])
         + ", "
         + "pi_e," + str(df["pi_e"][d])
         for d in range(len(df))]
thefile = open('price_in_line.csv', 'w')
for item in lines:
    thefile.write("%s\n" % item)
