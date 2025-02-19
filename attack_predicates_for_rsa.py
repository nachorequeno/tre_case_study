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

query_preds = {'lower': lower, 'low': low, 'medium': medium, 'high': high,
     'higher': higher}