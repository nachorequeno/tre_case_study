import sys
import os
import attack_predicates
import attack_predicates_for_rsa

from ParetoLib.TRE.TRE import TimedrelInterface
from signals2prsignal import plot_zones, plot_prsignal_with_zones, signals2prsignal

def read_expression(filename: str) -> str:
    f = open(filename, "r")
    expression = f.read()
    f.close()
    return expression

if __name__=="__main__":
    # attack = sys.argv[1]
    # input_signals = sys.argv[2:]
    attack = "fdi50"
    # input_signals = "/mnt/d/git_projects/papers/tre_case_study/day_0_360_user_1143/fdi50/days_*"
    input_signals = [f"/mnt/d/git_projects/papers/tre_case_study/day_0_360_user_1143/fdi50/{filename}" for filename in
                     os.listdir("/mnt/d/git_projects/papers/tre_case_study/day_0_360_user_1143/fdi50") if
                     filename.startswith("days_")]

    #signals2prsignal(f"./csv/{attack}.csv", input_signals)
    signals2prsignal(f"/mnt/d/git_projects/papers/tre_case_study/csv/{attack}.csv", input_signals)

    prec = 1

    #expression_file = f"./tre/{attack}.txt"
    expression_file = f"/mnt/d/git_projects/papers/tre_case_study/tre/{attack}.txt"
    # expression = "(low ; high) [3 : 4]"
    expression = read_expression(expression_file)

    if attack.startswith("rsa"):
        query_preds = attack_predicates_for_rsa.query_preds
    else:
        query_preds = attack_predicates.query_preds

    trace_file = f"./csv/{attack}.csv"
    # tre_expression: str, trace_file: str, precision: float, dtype: str, query_preds
    tre_engine = TimedrelInterface(tre_expression=expression, trace_file=trace_file, precision=prec, dtype="rational",
                                   query_preds=query_preds,)

    zones = tre_engine.run()
    print(zones)

    plot_zones(f"./svg/{attack}_zones.svg", zones)
    plot_prsignal_with_zones(f"./svg/{attack}_signal_and_zones.svg", input_signals, zones)