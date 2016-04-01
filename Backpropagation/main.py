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

net = Network([10,4])

net.train(set3, desired_outputs)
for category in set3:
    print "Category %s \n" %(set3.index(category) + 1)
    print str(desired_outputs[set3.index(category)]) + "\n"
    for pattern in category:
        net.test(pattern)
# net.reveal_network()
