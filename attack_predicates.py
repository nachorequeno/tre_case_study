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

query_preds = {'lower': lower, 'low': low, 'medium': medium, 'high': high,
     'higher': higher}