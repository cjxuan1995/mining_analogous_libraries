import re
import gensim.models.word2vec as w2v
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
# with open('tags.txt', 'r') as tags_file:
#     for tag in tags_file:
#         tag = re.sub(r'\n', '', tag)
#         tag_list.append(tag)
#
# print tag_list
# tag_count_dict = {}
# for tag in tag_list:
#     tag_count_dict[tag] = 0
#
# with open('tag_sentences.txt', 'r') as tag_sentences_file:
#     for tag_sentence in tag_sentences_file:
#         tag_sentence = re.sub(r'\n', '', tag_sentence)
#         for tag in tag_sentence.split():
#             tag_count_dict[tag] += 1
#
# with open('tags_high_frequency.txt','w') as tags_high_freq_file:
#     for tag in tag_count_dict:
#         if tag_count_dict[tag] > 50:
#             tags_high_freq_file.write("%s\n" % (tag + " " + str(tag_count_dict[tag])))


with open('joint_tags.txt','r') as tags_high_freq_file:
    with open('synonyms_for_joint_tags_no_filter.txt', 'w') as synonym_file:
        model = w2v.Word2Vec.load('F:/model_quadgram_600/myModel')
        for line in tags_high_freq_file:
            line = re.sub(r'\n','',line)
            tag_list.append(line)
        for list in extract_similar_terms(0, 0, tag_list, model): #recall = 0.78 precision = 0.54
            if len(list) > 1:
                new_str = ' '
                synonym_file.write("%s\n" % new_str.join(list))






