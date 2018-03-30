import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib


precision = []
recall = []
precision_recall_dict = {}
tuple_list = []
with open("recall_precision_500.txt", "r") as precision_recall_data:
    for line in precision_recall_data:
        temp_precison = re.sub(r"^.*:", "", line)
        temp_precison = re.sub(r",.*$", "", temp_precison)
        temp_recall = re.sub(r"^.*,", "", line)
        precision.append(float(temp_precison))
        recall.append(float(temp_recall))

a = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
b = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]

for x in a:
    for y in b:
        tuple_list.append((x,y))

print tuple_list
precision_recall_dict = dict(zip(tuple_list, zip(precision,recall)))
print precision_recall_dict
special_coord = precision_recall_dict[(0.5, 0.75)]
# max = 0
# for key in precision_recall_dict:
#     temp = precision_recall_dict[key][0] + precision_recall_dict[key][1]
#     if temp > max:
#         max = temp
#         key_max = key
#
# print key_max, precision_recall_dict[key_max]
# print precision_recall_dict[key_max][0] + precision_recall_dict[key_max][1]

# sum_precision_recall = [a + b for a, b in zip(recall, precision)]

# x = np.arange(0, 81, 1)
# print len(precision)
# print len(recall)
# print len(precision_recall_dict)

color_list = []
for tuple in tuple_list:
    if tuple == (0.5, 0.75):
        color_list.append(0)
    else:
        color_list.append(0)
#print color_list.index(1)

font = {'family' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)
# plt.subplot(211)
plt.figure(figsize=(20,10))
plt.scatter(precision, recall, c=color_list)
#plt.annotate("(threshold1, threshold2) = (0.5, 0.75)", xy=special_coord, xytext=(special_coord[0], special_coord[1]+0.02), arrowprops=dict(facecolor='black', shrink=0.05),)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# plt.subplot(212)
# x = [0.06, 0.54]
# plt.hist(x, bins=4)
# plt.show()

