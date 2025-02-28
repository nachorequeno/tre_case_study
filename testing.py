import glob
import sys
from multiprocessing import Pool

import numpy as np
import seaborn as sn
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix

import attack_predicates
import attack_predicates_for_rsa

from ParetoLib.Geometry.Zone import Zone
from ParetoLib.TRE.TRE import TimedrelInterface


def read_expression(filename: str) -> str:
    f = open(filename, "r")
    expression = f.read()
    f.close()
    return expression

def confusion_matrix_heatmap(cm: np.ndarray, attack: str) -> None:
    # Visualize the confusion matrix using a heatmap
    plt.figure(figsize=(10, 7))
    sn.heatmap(cm, annot=True, fmt='d', # fmt='.2f'
               cmap='Blues',
               xticklabels=['Predicted Negative', 'Predicted Positive'],
               yticklabels=['Actual Negative', 'Actual Positive'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix Heatmap for {attack}')
    plt.show()

def normalize_confusion_matrix(cm: np.ndarray) -> np.ndarray:
    # Normalize the confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    return cm_normalized

def run_tre(tre_engine: TimedrelInterface) -> list[Zone]:
    return tre_engine.run()

def check_attack(zones_by_trace: list[Zone]) -> bool:
    # We detect an attack if at least one zone is detected
    # Additionally, we can impose constraints about the duration of the zones (e.g, cover at least 50% of the day)
    # return len(zones_by_trace) > 0 and sum(zone.dmin for zone in zones_by_trace) > 0
    return len(zones_by_trace) > 0

def not_check_attack(zones_by_trace: list[Zone]) -> bool:
    return not check_attack(zones_by_trace)

def testing(attack: str, positive_examples: list[str], negative_examples: list[str], query_pred: dict) -> tuple[int, int, int, int]:

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
    # positive_zones = [tre_engine.run() for tre_engine in positive_tre_engine]
    # positive_pred = [check_attack(zones_by_trace) for zones_by_trace in positive_zones]

    p = Pool()
    positive_zones = p.map(run_tre, positive_tre_engine)
    positive_pred = p.map(check_attack, positive_zones)

    negative_tre_engine = [
        TimedrelInterface(tre_expression=expression, trace_file=negative_attack, precision=prec, dtype="float",
                          query_preds=query_pred, ) for negative_attack in negative_examples]
    # negative_zones = [tre_engine.run() for tre_engine in negative_tre_engine]
    # negative_pred = [not check_attack(zones_by_trace) for zones_by_trace in negative_zones]

    negative_zones = p.map(run_tre, negative_tre_engine)
    negative_pred = p.map(not_check_attack, negative_zones)
    # p.join()

    # true_positive = sum(positive_pred)
    # true_negative = sum(negative_pred)
    # false_negative = len(positive_zones) - true_positive
    # false_positive = len(negative_zones) - true_negative

    true_positive, true_negative = len(positive_zones), len(negative_zones)
    # Create confusion matrix based on the results
    # y_true = [1] * true_positive + [0] * false_negative + [0] * true_negative + [1] * false_positive
    # y_pred = [1] * (true_positive + false_positive) + [0] * (true_negative + false_negative)
    y_true = [True] * true_positive + [False] * true_negative
    y_pred = positive_pred + negative_pred

    cm = confusion_matrix(y_true, y_pred)
    print(cm)

    normalize_confusion_matrix(cm)
    confusion_matrix_heatmap(cm, attack)

    return true_positive, false_positive, true_negative, false_negative

if __name__=="__main__":
    attack = sys.argv[1]

    positive_examples_fnames = f"./day_0_360_user_1143/{attack}/*.csv"
    total_examples_fnames = f"./day_0_360_user_1143/*/*.csv"

    # Read positive examples files from the directory
    positive_examples = glob.glob(positive_examples_fnames, recursive=True)
    negative_examples = list(set(glob.glob(total_examples_fnames, recursive=True)) - set(positive_examples))

    print(f"Testing attack: {attack}")
    print(f"Positive examples: {len(positive_examples)}, Negative examples: {len(negative_examples)}")

    # query_pred = {'lower': lower, 'low': low, 'medium': medium, 'high': high, 'higher': higher}
    if attack.startswith("rsa"):
        query_pred = attack_predicates_for_rsa.query_preds
    else:
        query_pred = attack_predicates.query_preds
    testing(attack, positive_examples, negative_examples, query_pred)