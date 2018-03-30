import re

tag_list_syn = []
count = 0
with open("tagSynonym_manual.txt", "r") as tag_syn:
    for line in tag_syn:
        line = re.sub(r"\t|\n", " ", line)
        line = line.strip(' ')
        tag_list_syn += re.split(r" |,", line)
        count += 1
    print tag_list_syn

print len(tag_list_syn)

tag_list = []
with open("tags.txt", "r") as tag_file:
    for line in tag_file:
        line = re.sub(r"\t|\n", "", line)
        line = line.strip(' ')
        tag_list.append(line)

print tag_list

joint_tag_list = list(set(tag_list_syn) & set(tag_list))

print len(joint_tag_list)

with open("joint_tags.txt", "w") as joint_tags:
    for tag in joint_tag_list:
        joint_tags.write("%s\n" % tag)





