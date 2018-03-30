import gensim.models.word2vec as w2v
import re
from difflib import SequenceMatcher
import numpy as np

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def is_abbrev(abbrev, text):
    if len(abbrev) > len(text):
        temp = abbrev
        abbrev = text
        text = temp
    pattern = re.sub('azk', '.*', re.escape('azk'.join(abbrev)))
    return re.match(pattern, text) is not None

def calculate_precision(list_a, list_b): #list_b is the ground truth
    joint_list_len = len(list(set(list_a) & set(list_b)))
    return float(joint_list_len) / float(len(list_a))

def calculate_recall(list_a, list_b):
    joint_list_len = len(list(set(list_a) & set(list_b)))
    return float(joint_list_len) / float(len(list_b))


def extract_similar_terms(a, b, tag_list, model):
    similar_word_list = []
    for tag in tag_list:
        if tag in model.wv.vocab:
            tup_list = model.most_similar(tag, topn = 40) #topn 20 or 30?
            if '-' in tag:
                tag_dash = re.sub(r'-', '_', tag)
                if tag_dash in model.wv.vocab:
                    tup_list += model.most_similar(tag_dash, topn = 40) # e.g. search for similar terms for end-of-line and end_of_line
            temp_similar_word_list = [tag]
            for tup in tup_list:
                if tup[1] >= a and not (tup[1] in temp_similar_word_list): # a range [0.2, 0.6]
                    if similar(tag, tup[0]) > b or is_abbrev(tup[0], tag): # b range [0.4, 0.8]
                        temp_similar_word_list.append(tup[0])
            similar_word_list.append(temp_similar_word_list)
    return similar_word_list



tag_list = []
tag_list_syn = []

with open("tagSynonym_manual.txt", "r") as tag_syn:
    for line in tag_syn:
        line = re.sub(r"\t|\n", " ", line)
        line = line.strip(' ')
        tag_list_syn.append([item for item in re.split(r" |,", line) if item != ''])

with open("joint_tags.txt", "w") as joint_tags_file:
    with open("tags_revised_dash.txt", "r") as tags_vocab:
        for line in tags_vocab:
            tag_list.append(re.sub(r"\n", "" ,line))
        tag_list_syn_flatten = [item for sublist in tag_list_syn for item in sublist]
        joint_tag_list = list(set(tag_list) & set(tag_list_syn_flatten))
        for tag in joint_tag_list:
            joint_tags_file.write("%s\n" % tag)

print len(joint_tag_list), len(tag_list_syn), len(tag_list)

# with open("similar_terms_for_joint_tags_pd.txt","w") as similar_terms_file:
#     for line in extract_similar_terms(0.4, 0.6, joint_tag_list):
#         new_str = " "
#         similar_terms_file.write("%s\n" % new_str.join(line))

def cal_pre_re(model_location, file_name):
    with open(file_name, "w") as pre_re_file:
        model = w2v.Word2Vec.load(model_location)
        for a in np.arange(0.2, 0.65, 0.05):
            for b in np.arange(0.4, 0.85, 0.05):
                precision = []
                recall = []
                for tags in extract_similar_terms(a, b, joint_tag_list, model):
                    for tags_sample in tag_list_syn:
                        if tags[0] in tags_sample:
                            precision.append(calculate_precision(tags, tags_sample))
                            recall.append(calculate_recall(tags, tags_sample))
                            break
                pre_re_file.write("%s\n" % (str(a) +',' + str(b) + ':' + str(sum(precision) / float(len(precision))) +',' + str(sum(recall) / float(len(recall)))))
                # print (str(a) +',' + str(b) + ':' + str(sum(precision) / float(len(precision))) +',' + str(sum(recall) / float(len(recall))))
        print ("%s is completed" % file_name)


cal_pre_re('F:\model_quadgram_200\myModel', 'recall_precision_200.txt')
cal_pre_re('F:\model_quadgram_300\myModel', 'recall_precision_300.txt')
cal_pre_re('F:\model_quadgram_400\myModel', 'recall_precision_400.txt')
cal_pre_re('F:\model_quadgram_500\myModel', 'recall_precision_500.txt')
cal_pre_re('F:\model_quadgram_600\myModel', 'recall_precision_600.txt')

