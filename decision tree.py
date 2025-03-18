import numpy as np
# Training dataset
# x1 atmospheric pressure
x1 = ['high', 'high', 'low', 'low', 'low', 'high']  
# x2 is weather type
x2 = ['partly cloudy', 'sunny', 'sunny', 'cloudy', 'cloudy', 'cloudy']  
X = np.array([x1, x2]).T
y = np.array([False, False, True, False, False, True]) # rain (True) and no-rain (False)
X # features
y # labels
# Splitting a set
# Input is an array of feature observations and output is a dictionary with "unique feature value" as key and indices as value
def partition(a):
    return {c: (a==c).nonzero()[0] for c in np.unique(a)}

# Picking which attribute to split
# Calculate entropy of a list
def entropy(s):
    res = 0
    val, counts = np.unique(s, return_counts=True)
    freqs = counts.astype('float')/len(s)
    for p in freqs:
        if p != 0.0:
            res -= p * np.log2(p)
    return res

# Calculate decrease in impurity (information gains)
# 
def mutual_information(y, x):
    
    # Calculate entropy of observation classes
    res = entropy(y)

    # We partition x, according to attribute values x_i
    val, counts = np.unique(x, return_counts=True)
    freqs = counts.astype('float')/len(x)

    # We calculate a weighted average of the entropy and subtract it from parent entropy
    for p, v in zip(freqs, val):
        res -= p * entropy(y[x == v])

    return res

# Checks for pureness of elements in a list
def is_pure(s):
#     print('d- ',s)
#     print('f- ',set(s))
#     print('g',len(set(s)))
    return len(set(s)) == 1

# Helper function to print decision tree
def print_tree(d, depth = 0):
    for key, value in d.items():
        for i in range(depth):
                print(' ', end='')
        if type(value) is dict:
            print(key, end=':\n')
            print_tree(value, depth + 1)
        else:
            print(key, end=': ')
            print(value)
            
# Get the most common element of an array
def most_common(a):
    (values,counts) = np.unique(a,return_counts=True)
#     print('g ',values,counts)
    ind=np.argmax(counts)
#     print('q ',values[ind])
    return values[ind]

# Recursive split of observations
def recursive_split(x, y):
    
    # If set to be split is pure or empty, return it as leaf
    if is_pure(y) or len(y) == 0:
        return most_common(y)

    # Calculate decrease in impurity (information gain) and split attribute with maximum gain
    gain = np.array([mutual_information(y, x_attr) for x_attr in x.T])
    selected_attr = np.argmax(gain)

    # Sufficiently pure, return it as leaf
    if np.all(gain < 1e-6):
        return most_common(y)

    # Split using the selected attribute
    sets = partition(x[:, selected_attr])

    # Perform recursive splits and collect results
    res = {}
    for key, value in sets.items():
        y_subset = y.take(value, axis=0)
        x_subset = x.take(value, axis=0)
        res["x_%d = %s" % (selected_attr, key)] = recursive_split(x_subset, y_subset)

    return res

# Perform algorithm on the example dataset to create a decision tree
d = recursive_split(X, y)
print_tree(d)
print(type(d))
print(d)



# New dataset (which shall be classified by the above generated decision tree)
x1 = ['high', 'low', 'low', 'high', 'low', 'high', 'high', 'low', 'low', 'high', 'low', 'low']
x2 = ['sunny', 'sunny', 'cloudy', 'cloudy', 'partly cloudy', 'cloudy', 'partly cloudy', 'cloudy', 'sunny', 'cloudy', 'cloudy', 'partly cloudy']
X = np.array([x1, x2]).T
y = np.array([False, True, True, False, False, True, False, True, True, False, True, True]) # ground-truth of classification
# print(X) # features

#Method to traverse given tree sructure
def predictFromTree(a_dict, features, level):
    predictionResult='none'  # initial prediction
    for key in a_dict:  # start iterating through decision tree
        if (features[level] == key[6:]): # matching feature with (node values) keys in decision tree
            if type(a_dict.get(key)) is dict: #check if need to further traverse child node
                predictionResult=predictFromTree(a_dict.get(key), features, level-1)  # Next attribute to check is atmos pressure 
            else:
                predictionResult=a_dict.get(key) # get prediction from tree
    return predictionResult
            
predictions=list()         # list to hold our all predictions 
for i in X:
    predictions.append(predictFromTree(d, i, 1)) # level 1 is weather condition attribute
    
result = np.array([x1, x2, predictions]).T
print(result)