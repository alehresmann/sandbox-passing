import sys
import pandas
import matplotlib.pyplot as plt

# settings for fig size.
plt.figure(num=None, figsize=(15, 5), dpi=500, facecolor="w", edgecolor="k")

colours = ["blue", "red", "gold", "chartreuse", "darkturquoise", "darkorchid"]
m_colours = ["navy", "firebrick", "goldenrod", "forestgreen", "dodgerblue", "purple"]

df = pandas.read_csv(sys.argv[1])

for i in range(0, len(df.columns)):
    col = colours[i % len(df.columns)]
    m_col = colours[i % len(m_colours)]
    plt.plot(df.columns[i], data=df, color=col, linewidth=1, label=df.columns[i])

plt.legend(df.columns)
plt.xlabel(" random attempt")
plt.ylabel("number of rounds needed")
plt.savefig("test.png")
