import sys

from ParetoLib.TRE.TRE import TimedrelInterface
from signals2prsignal import plot_zones, plot_prsignal_with_zones, signals2prsignal


def read_expression(filename: str) -> str:
    f = open(filename, "r")
    expression = f.read()
    f.close()
    return expression

def lower(x):
    return 0.0 <= x[2] < 0.36


def low(x):
    return 0.36 <= x[2] < 0.71

def medium(x):
    return 0.71 <= x[2] < 1.42

def high(x):
    return 1.42 <= x[2] < 2.42

def higher(x):
    return x[2] >= 2.42


if __name__=="__main__":
    attack = sys.argv[1]
    input_signals = sys.argv[2:]

    signals2prsignal(f"./csv/{attack}.csv", input_signals)

    prec = 1

    expression_file = f"./tre/{attack}.txt"
    # expression = "(low ; high) [3 : 4]"
    expression = read_expression(expression_file)

    trace_file = f"./csv/{attack}.csv"
    # tre_expression: str, trace_file: str, precision: float, dtype: str, query_preds
    tre_engine = TimedrelInterface(tre_expression=expression, trace_file=trace_file, precision=prec, dtype="float",
                                   query_preds={'lower': lower, 'low': low, 'medium': medium, 'high': high,
                                                'higher': higher}, )

    zones = tre_engine.run()
    print(zones)

    plot_zones(f"./svg/{attack}_zones.svg", zones)
    plot_prsignal_with_zones(f"./svg/{attack}_signal_and_zones.svg", input_signals, zones)