import re

tag_list_syn = []
tag_list = []
precision = []
recall = []
with open("tagSynonym_manual.txt", "r") as tag_syn:
    for line in tag_syn:
        line = re.sub(r"\t|\n", " ", line)
        line = line.strip(' ')
        tag_list_syn.append(re.split(r" |,", line))

with open("synonyms_for_joint_tags_no_filter.txt", "r") as model_result:
    for line in model_result:
        line = re.sub(r"\n", "", line)
        tag_list.append(line.split())


def calculate_precision(list_a, list_b): #list_b is the ground truth
    joint_list_len = len(list(set(list_a) & set(list_b)))
    return float(joint_list_len) / float(len(list_a))

def calculate_recall(list_a, list_b):
    joint_list_len = len(list(set(list_a) & set(list_b)))
    return float(joint_list_len) / float(len(list_b))

for tags in tag_list:
    for tags_sample in tag_list_syn:
        if tags[0] in tags_sample:
            precision.append(calculate_precision(tags, tags_sample))
            recall.append(calculate_recall(tags, tags_sample))
            break

print len(precision)
print precision
print sum(precision) / float(len(precision))
print len(recall)
print recall
print sum(recall) / float(len(recall))



