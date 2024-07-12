import sys

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ParetoLib.TRE.TRE import TimedrelInterface

def read_expression(filename: str) -> str:
    f = open(filename, "r")
    expression = f.read()
    f.close()
    return expression

def lower(x):
    None

def low(x):
    return 0.0 <= x[2] < 0.71

def medium(x):
    return 0.71 <= x[2] < 1.42

def high(x):
    return x[2] > 1.42

def higher(x):
    None


if __name__=="__main__":
    attack = sys.argv[1]

    prec = 1

    expression_file = f"./tre/{attack}.txt"
    # expression = "(low ; high) [3 : 4]"
    expression = read_expression(expression_file)


    trace_file = f"./csv/{attack}.csv"
    # tre_expression: str, trace_file: str, precision: float, dtype: str, query_preds
    tre_engine = TimedrelInterface(tre_expression=expression, trace_file=trace_file, precision=prec, dtype="float",
                                   query_preds={'lower': lower, 'low': low, 'medium': medium, 'high': high,
                                                'higher': higher},)

    zones = tre_engine.run()
    print(zones)

    f: Figure = plt.figure()
    f.add_subplot(111)
    for zone in zones:
        zone.plot_2D(fig=f)

    plt.show()