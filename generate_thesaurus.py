import re

def union(list1, list2):
    for item in list2:
        if not (item in list1):
            list1.append(item)
    return list1

def complement(list1, list2):
    for item in list2:
        if item in list1:
            list1.remove(item)
    return list1

thesaurus = []
with open("synonyms_for_high_frequency_tags.txt", "r") as raw_thesaurus_file:
    for line in raw_thesaurus_file:
        line = re.sub(r'\n','', line)
        thesaurus.append(line.split())

print thesaurus

pos_neg_set = []
with open("synonymPosNeg.txt", "r") as pos_neg_file:
    for line in pos_neg_file:
        line = re.sub(r'\n','',line)
        pos_neg_list = line.split()
        if len(pos_neg_list) > 1:
            pos_neg_set.append([pos_neg_list[0].split(','),pos_neg_list[1].split(',')])
        else:
            pos_neg_set.append([pos_neg_list[0].split(',')])

print len(pos_neg_set)

tag_list_syn = []

with open("tagSynonym_manual.txt", "r") as tag_syn:
    for line in tag_syn:
        line = re.sub(r"\t|\n", " ", line)
        line = line.strip(' ')
        tag_list_syn.append([item for item in re.split(r" |,", line) if item != ''])

print len(tag_list_syn)

pos_neg_set_extended = pos_neg_set

for syn_list in tag_list_syn:
    if len(syn_list) > 1:
        for pos_neg_pair in pos_neg_set:
            if syn_list[0] in pos_neg_pair[0]:
                break;
        else:
            pos_neg_set_extended.append([syn_list])

print len(pos_neg_set_extended)

print len(thesaurus)

count = 0

for pos_neg_pair in pos_neg_set_extended:
    for idx in range(len(thesaurus)):
        if pos_neg_pair[0][0] == thesaurus[idx][0]:
            if len(pos_neg_pair) > 1:
                thesaurus[idx] = complement(union(thesaurus[idx], pos_neg_pair[0]), pos_neg_pair[1])
                count += 1
                break
            else:
                thesaurus[idx] = union(thesaurus[idx], pos_neg_pair[0])
                count += 1
                break

print count
with open('thesaurus_processed.txt','w') as thesaurus_processed_file:
    for syn_terms in thesaurus:
        new_str = " "
        thesaurus_processed_file.write("%s\n" % new_str.join(syn_terms))



