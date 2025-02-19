import glob
import sys

from sklearn.metrics import confusion_matrix
from ParetoLib.Geometry.Zone import Zone
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

def testing(attack: str, positive_examples: list[str], negative_examples: list[str], query_pred: dict) -> tuple[int, int, int, int]:
    def check_attack(zones_by_trace: list[Zone]) -> bool:
        # We detect an attack if at least one zone is detected
        return len(zones_by_trace) > 0

    # A TRE classifier detects if there is an attack in the system.
    # The TRE classifier is based on the input signals and the expression of the attack.
    # The TRE classifier returns the zones of the attack.
    # The TRE classifier musts detect at least one zone in the input signals to consider that the attack is present.
    true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0

    expression_file = f"./tre/{attack}.txt"
    # expression = "(low ; high) [3 : 4]"
    expression = read_expression(expression_file)

    prec = 1
    # tre_expression: str, trace_file: str, precision: float, dtype: str, query_preds
    positive_tre_engine = [
        TimedrelInterface(tre_expression=expression, trace_file=positive_attack, precision=prec, dtype="float",
                          query_preds=query_pred, ) for positive_attack in positive_examples]
    positive_zones = [tre_engine.run() for tre_engine in positive_tre_engine]
    true_positive = sum([check_attack(zones_by_trace) for zones_by_trace in positive_zones])

    negative_tre_engine = [
        TimedrelInterface(tre_expression=expression, trace_file=negative_attack, precision=prec, dtype="float",
                          query_preds=query_pred, ) for negative_attack in negative_examples]
    negative_zones = [tre_engine.run() for tre_engine in negative_tre_engine]
    true_negative = sum([not check_attack(zones_by_trace) for zones_by_trace in negative_zones])

    false_negative = len(positive_zones) - true_positive
    false_positive = len(negative_zones) - true_negative

    # Create confusion matrix based on the results
    y_true = [1] * true_positive + [0] * false_negative + [0] * true_negative + [1] * false_positive
    y_pred = [1] * (true_positive + false_positive) + [0] * (true_negative + false_negative)

    cm = confusion_matrix(y_true, y_pred)
    print(cm)

    return true_positive, false_positive, true_negative, false_negative

if __name__=="__main__":
    attack = sys.argv[1]

    positive_examples_fnames = f"./day_0_360_user_1143/{attack}/*.csv"
    total_examples_fnames = f"./day_0_360_user_1143/*/*.csv"

    # Read positive examples files from the directory
    positive_examples = glob.glob(positive_examples_fnames, recursive=True)
    negative_examples = list(set(glob.glob(total_examples_fnames, recursive=True)) - set(positive_examples))

    print(f"Positive examples: {len(positive_examples)}, Negative examples: {len(negative_examples)}")
    query_pred = {'lower': lower, 'low': low, 'medium': medium, 'high': high, 'higher': higher}
    testing(attack, positive_examples, negative_examples, query_pred)