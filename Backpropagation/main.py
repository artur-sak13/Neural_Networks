from Activations import *


def toggle(node):
    if node == 1:
        return 0
    else:
        return 1

def distort(pattern):
    rel_pattern = [toggle(x) if random.random() < 0.125 else x for x in pattern]
    return rel_pattern

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
        net.train(training_set, desired_outputs)
        for category in training_set:
            print "Category %s \n" %(training_set.index(category) + 1)
            print str(desired_outputs[training_set.index(category)]) + "\n"
            for pattern in category:
                net.test(pattern)
        print "_________________________________________________________________________________"

def run_distorted(net):
    for training_set in training_sets:
        net.train(training_set, desired_outputs)
        for category in training_set:
            print "Category %s \n" %(training_set.index(category) + 1)
            print str(desired_outputs[training_set.index(category)]) + "\n"
            for pattern in category:
                pattern = distort(pattern)
                net.test(pattern)
        print "_________________________________________________________________________________"

net = Network([10,10,4])
run_distorted(net)
