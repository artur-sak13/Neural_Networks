from Activations import *


def calc_amount_of_distortion(pattern, d_pattern):
    sum_of_square_errors = 0.0
    for node, d_node in zip(pattern, d_pattern):
        sum_of_square_errors += (node - d_node)**2
    return sum_of_square_errors

def fuzz(node):
    if node == 0:
        node += random.uniform(0,0.5)
    return node

def distort(pattern):
    rel_pattern = [fuzz(x) for x in pattern]
    return rel_pattern

def create_encoder_patterns():
    patterns = [[1.0 if i == j else 0.0 for i in range(8)] for j in range(7)]
    return patterns

set1 = [
       [[0,0,0,0,0,1,0,0,0,0], [0,0,0,0,0,0,0,0,0,1]],
       [[0,0,0,0,1,0,0,0,1,0], [0,0,0,1,0,0,0,0,0,0]],
       [[0,0,0,0,0,0,0,1,0,0], [0,0,1,0,0,0,0,0,0,0]],
       [[0,1,0,0,0,0,1,0,0,0], [1,0,0,0,0,0,1,0,0,0]]
       ]

set2 = [
       [[1,1,0,1,0,0,0,0,0,1], [1,1,0,0,1,0,0,0,0,1]],
       [[1,1,0,0,0,1,0,0,1,0], [1,1,0,0,0,0,0,0,1,0]],
       [[1,0,1,1,0,0,0,1,0,0], [1,0,1,0,1,0,0,1,0,0]],
       [[1,0,1,0,0,1,1,0,0,0], [1,0,1,0,0,0,1,0,0,0]]
       ]

set3 = [
       [[1,1,1,1,0,0,0,0,0,0], [0,0,0,0,0,0,1,1,1,1]],
       [[1,1,0,1,1,0,0,1,0,0], [0,0,1,0,0,1,1,0,1,1]]
       ]

desired_outputs = [
                  [0.98,0.02,0.02,0.02],
                  [0.02,0.98,0.02,0.02],
                  [0.02,0.02,0.98,0.02],
                  [0.02,0.02,0.02,0.98]
                  ]

training_sets = [set1, set2, set3]

def run_undistorted(net):
    for training_set in training_sets:
        print "TRAINING SET %d" %(training_sets.index(training_set) + 1)
        net.train(training_set, desired_outputs)
        for category in training_set:
            print "Category %s \n" %(training_set.index(category) + 1)
            print str(desired_outputs[training_set.index(category)]) + "\n"
            for pattern in category:
                net.test(pattern, pattern)
        print "_________________________________________________________________________________"

def run_distorted(net):
    for training_set in training_sets:
        print "TRAINING SET %d" %(training_sets.index(training_set) + 1)
        net.train(training_set, desired_outputs)
        for category in training_set:
            print "Category %s \n" %(training_set.index(category) + 1)
            print str(desired_outputs[training_set.index(category)]) + "\n"
            for pattern in category:
                d_pattern = distort(pattern)
                print "Distortion Level: %s" %(calc_amount_of_distortion(pattern, d_pattern))
                net.test(pattern, d_pattern)
        print "_________________________________________________________________________________"

def run_encoder(net, patterns):
    net.train_encoder(patterns, patterns)
    for pattern in patterns:
        print "PATTERN %s" %(patterns.index(pattern) + 1)
        print pattern
        net.test(pattern)

# [[1,1,1,0,0,0,0,0],[0,0,0,1,1,1,0,0]]
# [0,0,1,1,0,0,0,0]
net = Network([10,10,4])
run_distorted(net)
# run_distorted(net)
# run_distorted(net)
# net = Network([8,3,8])
# patterns = create_encoder_patterns()
# run_encoder(net, patterns)
