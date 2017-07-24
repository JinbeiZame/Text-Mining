# -*- coding: utf-8 -*-
from collections import Iterable

x = [[14, 15], [14, 15], [14, 15], [26, 27], [26, 27], [15, 17],[26, 28], [14, 15], [14, 15], [26, 27], [26, 27], [15, 17]]
countt =1
#print len(x)/2
text_file = open("Output.txt", "w")
for el in list(x):
        #print ( " ".join([str(index) for index, value in enumerate(x) if value == el]))
        text_file.write( " ".join([str(index) for index, value in enumerate(x) if value == el]))
        text_file.write('\n')
text_file.close()
#print text_file
text_file1 = open("Output1.txt", "w")
for el in list(x):

    text_file1.write(" ".join([str(index) for index, value in enumerate(x) if value == el]))
    text_file1.write('\n')
text_file1.close()

with open('Output.txt', 'r') as file1:
    with open('Output1.txt', 'r') as file2:
        same = set(file1).intersection(file2)
        print same
same.discard('\n')

with open('some_output_file.txt', 'w') as file_out:
    for line in same:
        file_out.write(line)

'''
with open('Output.txt', 'r') as file1:
    with open('Output1.txt', 'r') as file2:
        print file2
        same = set(file1).intersection(file2)
        print same
same.discard('\n')

with open('some_output_file1.txt', 'w') as file_out:
    for line in same:
        #print same
        file_out.write(line)
'''
f = open("some_output_file.txt", "r")
g = open("intersection.txt", "w")

for line in f:

    if line.strip():
        g.write("\n".join(line.split()[1:]) + "\n")

f.close()
g.close()


f = open("intersection.txt", "r")
contents = f.readlines()
#print contents
f.close()

contents.insert(0, "\n")                                 #Insert \n in first line text file

f = open("intersection1.txt", "w")
contents = "".join(contents)
#print contents
f.write(contents)
f.close()


with open('intersection.txt') as f:
    h = [int(x) for x in next(f).split()]
    array = [[int(x) for x in line.split()] for line in f]
    #print array

list2 = [x for x in array if x]
#print(list2)



def flatten(list2):
    for item in list2:
        if isinstance(item, Iterable) and not isinstance(item, basestring):
            for x in flatten(item):
                yield x                                                             #Convert nest list to list of integer
        else:
            yield item

#print(list(flatten(list2)))
import numbers
CNLTLOI = list(flatten(list2))

results_integer = list(map(int, [x for x in CNLTLOI if isinstance(x, numbers.Number)]))
#print results_integer

sort_list = sorted(results_integer, reverse=False)
print(sort_list)
