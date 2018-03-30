import gensim.models as gm
import re
import os

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = MySentences('E:/sample_data')  # a memory-friendly iterator
#
# word_list = []
# with open("10000rows.txt", "r") as sample_data:
#     for line in sample_data:
#         line = re.sub(r"\n", "", line)
#         word_list.append(line.split())

# phrases = gm.Phrases(sentences)
# bigram = gm.phrases.Phraser(phrases)
# tri_phrases = gm.Phrases(bigram[sentences])
# trigram = gm.phrases.Phraser(tri_phrases)
# quad_phrase = gm.Phrases(trigram[sentences])
# quadgram = gm.phrases.Phraser(quad_phrase)
# trigram.save("E:/phrase_detection/quadgram")
quadgram = gm.Phrases.load("E:/phrase_detection/quadgram")

def convert_to_quadgram(filename1, filename2):
    with open(filename1, "r") as unprocessed_file:
        with open(filename2, "w") as trigram_file:
            for line in unprocessed_file:
                line = re.sub(r"\n", "", line)
                word_list = line.split()
                word_list = quadgram[word_list]
                new_str = " "
                trigram_file.write("%s\n" % new_str.join(word_list))

convert_to_quadgram('processed_data2.txt','processed_data2_quadgram.txt')
convert_to_quadgram('processed_data3.txt','processed_data3_quadgram.txt')
convert_to_quadgram('processed_data4.txt','processed_data4_quadgram.txt')
convert_to_quadgram('processed_data5.txt','processed_data5_quadgram.txt')
convert_to_quadgram('processed_data6.txt','processed_data6_quadgram.txt')
convert_to_quadgram('processed_data7.txt','processed_data7_quadgram.txt')
#
# with open("10000rows_bigram.txt", "w") as sample_data_phrases:
#     for words in bigram[word_list]:
#         new_str = " "
#         sample_data_phrases.write("%s\n" % new_str.join(words))













