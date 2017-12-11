import math

attributes = ["Outlook",    "Temperature",  "Humidity",     "Wind",     "Tennis"]
dataset =   [["Sunny",      "Hot",          "High",         "Weak",     "No"],
             ["Sunny",      "Hot",          "High",         "Strong",   "No"],
             ["Overcast",   "Hot",          "High",         "Weak",     "Yes"],
             ["Rain",       "Mild",         "High",         "Weak",     "Yes"],
             ["Rain",       "Cool",         "Normal",       "Weak",     "Yes"],
             ["Rain",       "Cool",         "Normal",       "Strong",   "No"],
             ["Overcast",   "Cool",         "Normal",       "Strong",   "Yes"],
             ["Sunny",      "Mild",         "High",         "Weak",     "No"],
             ["Sunny",      "Cool",         "Normal",       "Weak",     "Yes"],
             ["Rain",       "Mild",         "Normal",       "Weak",     "Yes"],
             ["Sunny",      "Mild",         "Normal",       "Strong",   "Yes"],
             ["Overcast",   "Mild",         "High",         "Strong",   "Yes"],
             ["Overcast",   "Hot",          "Normal",       "Weak",     "Yes"],
             ["Rain",       "Mild",         "High",         "Strong",   "No"]]


def find(item, lst):
    for i in lst:
        if item(i): 
            return True
        else:
            return False


def majority(attributes, data, target):
    val_freq = {}
    index = attributes.index(target)

    for point in data:
        if (point[index]) in val_freq:
            val_freq[point[index]] += 1
        else:
            val_freq[point[index]] = 1

    max_freq = 0
    major = ""

    for key in val_freq.keys():
        if val_freq[key] > max_freq:
            max_freq = val_freq[key]
            major = key

    return major


def entropy(attributes, data, target_attr):
    val_freq = {}
    data_entropy = 0.0

    i = 0
    for entry in attributes:
        if target_attr == entry:
            break
        i += 1

    for entry in data:
        if entry[i] in val_freq:
            val_freq[entry[i]] += 1.0
        else:
            val_freq[entry[i]] = 1.0

    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2)
        
    return data_entropy


def gain(attributes, data, attr, target_attr):
    """
    Calculates the information gain (reduction in entropy) that would result by splitting the data on the chosen
    attribute.
    """
    val_freq = {}
    subset_entropy = 0.0

    i = attributes.index(attr)

    for entry in data:
        if entry[i] in val_freq:
            val_freq[entry[i]] += 1.0
        else:
            val_freq[entry[i]] = 1.0

    for val in val_freq.keys():
        val_prob = val_freq[val] / sum(val_freq.values())
        data_subset = [entry for entry in data if entry[i] == val]
        subset_entropy += val_prob * entropy(attributes, data_subset, target_attr)

    return entropy(attributes, data, target_attr) - subset_entropy


def choose_attribute(data, attributes, target):
    best = attributes[0]
    max_gain = 0

    for attr in attributes:
        new_gain = gain(attributes, data, attr, target)
        if new_gain > max_gain:
            max_gain = new_gain
            best = attr

    return best


def get_values(data, attributes, attr):
    index = attributes.index(attr)
    values = []
    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])
    return values


def get_examples(data, attributes, best, val):
    examples = [[]]
    index = attributes.index(best)

    for entry in data:

        # find entries with the given value
        if entry[index] == val:
            new_entry = []

            # add value if it is not in best column
            for i in range(len(entry)):
                if i != index:
                    new_entry.append(entry[i])

            examples.append(new_entry)

    examples.remove([])

    return examples


def make_decision_tree(data, attributes, target):
    """
    Returns a new decision tree based on the examples given.
    :param data:
    :param attributes:
    :param target:
    :return:
    """

    # Possible values of the target attribute
    vals = [record[attributes.index(target)] for record in data]
    default = majority(attributes, data, target)

    if not data or (len(attributes) - 1) <= 0:
        return default
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = choose_attribute(data, attributes, target)
        tree = {best: {}}

        for val in get_values(data, attributes, best):
            examples = get_examples(data, attributes, best, val)
            new_attr = attributes[:]
            new_attr.remove(best)
            subtree = make_decision_tree(examples, new_attr, target)
            tree[best][val] = subtree
    
    return tree


if __name__ == "__main__":
    print(make_decision_tree(dataset, attributes, attributes[0]))
