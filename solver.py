#!/usr/bin/python
# -*- coding: utf-8 -*-
import knapsack
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

capacity = 0

def trivial(items):
        # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)    

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return (value, taken)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    global capacity 
    capacity = int(firstLine[1])    

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))


    


    min,max,total = knapsack.min_max(items)

    value = 0
    taken = []
    optimal = 0

    #if total > 50000000:
    #    value, taken, optimal=knapsack.greedy(items, capacity)
    #else:
    value, taken, optimal=knapsack.dynamic(items, capacity)

    print(f"DP: {value}\n{' '.join(map(str,taken))}")

    #Havin some issues on ks_50_0
    value, taken, optimal=knapsack.bnb(items, capacity)

    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(optimal) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

