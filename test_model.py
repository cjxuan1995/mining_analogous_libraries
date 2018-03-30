# import re
import gensim.models.word2vec as w2v
#
#
#
# model = w2v.Word2Vec.load('E:/model_quadgram/myModel')
#
# print model.wv.most_similar("internet-explorer")

# print model.wv.most_similar(postive = ['nltk', 'java'], negative = ['python'])

#if "software-update" in model.wv.vocab:
    #print ""
#else:
    #print "no"

import re
import gensim.models.word2vec as w2v

model = w2v.Word2Vec.load('F:/model_quadgram_600/myModel')
pl_vocab = ['java','c++','c#','python','php','javascript'] #'.net','delphi','perl','ruby','swift','assembly_language','go','r','visual_basic','matlab','sql','objective_c','scratch'
library_list = []

with open('sitemap.txt', 'r') as library_source:
    for line in library_source:
        line = re.sub(r'https://graphofknowledge.appspot.com/similartech/?','', line)
        line = re.sub(r'mobile.html','',line)
        line = re.sub(r'\n','',line)
        if line:
            library_list.append(line)

print library_list
print len(library_list)

count = 0
for library in library_list:
    if library in model.wv.vocab:
        count += 1

print count

tag_sentence_list = []
with open('tag_sentences.txt', 'r') as tag_sentences_file:
    for line in tag_sentences_file:
        line = re.sub(r'\n', '', line)
        tag_sentence_list.append(line.split())

def find_corresponding_pl (lib):
    pl_count_dict = {'java' : 0, 'c++' : 0, 'c#' : 0, 'python' : 0, 'php' : 0, 'javascript' : 0}
    for tag_sentence in tag_sentence_list:
        if lib in tag_sentence:
            for pl in pl_count_dict:
                if pl in tag_sentence:
                    pl_count_dict[pl] += 1

    return max(pl_count_dict, key=pl_count_dict.get)


def find_analogical_libraries(lib):
    analogical_libraries_for_pl = {'java' : [], 'c++' : [], 'c#' : [], 'python' : [], 'php' : [], 'javascript' : []}
    related_pl = find_corresponding_pl(lib)
    for pl in analogical_libraries_for_pl:
        temp_analogical_libraries = [x[0] for x in model.wv.most_similar(positive = [lib, pl], negative = [related_pl])]
        temp_analogical_libraries = list(set(temp_analogical_libraries) & set(library_list))
        for library_returned in temp_analogical_libraries:
            if pl != find_corresponding_pl(library_returned):
                temp_analogical_libraries.remove(library_returned)
        analogical_libraries_for_pl[pl] += temp_analogical_libraries
    return analogical_libraries_for_pl, related_pl

library_list = ('lucene','jackson','jfreechart','weka','libgdx','highcharts','momentjs','jspdf','jplayer','flot','itextsharp','tweetsharp','dotnetzip','dotnetopenauth','naudio','phpexcel','cakephp','mpdf','jpgraph','phpunit','opencv','libxml2','googletest','opencl','log4cxx','beautifulsoup','nltk','urlib','pygame','lxml')

for library in library_list:
    a = find_analogical_libraries(library)
    print ("%s\n" % (library + ':' + a[1]))
    print a[0]
