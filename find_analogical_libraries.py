import re
import gensim.models.word2vec as w2v
import operator

def intersection(list1, list2):
    for item in list2:
        if not (item in list1):
            list2.remove(item)
    return list2

model = w2v.Word2Vec.load('F:/model_quadgram_600/myModel')
pl_vocab = ['java','c++','c#','python','php','javascript'] #'.net','delphi','perl','ruby','swift','assembly_language','go','r','visual_basic','matlab','sql','objective_c','scratch'
library_list = []

with open("library_synonym_processed.txt", "r") as lib_syn_file:
    lib_syn_list = []
    for line in lib_syn_file:
        line = re.sub(r"\n", "", line)
        lib_syn_list.append(line.split())
    print "lib_syn_list is ready"

def normalize(lib, original_list, original_lib):
    for lib_syn_pair in lib_syn_list:
        if lib in lib_syn_pair and lib != lib_syn_pair[0]:
            if lib_syn_pair[0] not in original_list and lib_syn_pair[0] != original_lib:
                return lib_syn_pair[0]
    return lib

with open('sitemap.txt', 'r') as library_source:
    for line in library_source:
        line = re.sub(r'https://graphofknowledge.appspot.com/similartech/?','', line)
        line = re.sub(r'mobile.html','',line)
        line = re.sub(r'\n','',line)
        if line:
            library_list.append(line)


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


def find_analogical_libraries(lib, library_list):
    analogical_libraries_for_pl = {'java' : [], 'c++' : [], 'c#' : [], 'python' : [], 'php' : [], 'javascript' : []}
    related_pl = corresponding_pl_dict[lib]
    for pl in analogical_libraries_for_pl:
        temp_analogical_libraries = model.wv.most_similar(positive = [lib, pl], negative = [related_pl], topn = 40)
        temp_analogical_libraries_copy = temp_analogical_libraries
        temp_analogical_libraries_name = [lib_tuple[0] for lib_tuple in temp_analogical_libraries_copy]
        temp_analogical_libraries = [(normalize(lib_tuple[0], temp_analogical_libraries_name, lib), lib_tuple[1]) for lib_tuple in temp_analogical_libraries_copy if normalize(lib_tuple[0], temp_analogical_libraries_name, lib) in library_list]
        temp_analogical_libraries_copy = temp_analogical_libraries
        temp_analogical_libraries = [lib_tuple for lib_tuple in temp_analogical_libraries_copy if pl == corresponding_pl_dict[lib_tuple[0]]]
        temp_analogical_libraries_copy = temp_analogical_libraries
        temp_analogical_libraries = [lib_tuple for lib_tuple in temp_analogical_libraries_copy if lib_tuple[1] > 0.4]
        analogical_libraries_for_pl[pl] += temp_analogical_libraries
    return analogical_libraries_for_pl


with open("corresponding_pl.txt","r") as corr_pl_file:
    corresponding_pl_dict = {}
    for line in corr_pl_file:
        line = re.sub(r"\n","",line)
        temp_lib = re.sub(r" :.*$","", line)
        temp_pl = re.sub(r"^.*: ","",line)
        corresponding_pl_dict[temp_lib] = temp_pl
    print corresponding_pl_dict

with open("tags_high_frequency.txt","r") as tag_high_freq_file:
    library_list_freq = {}
    for line in tag_high_freq_file:
        line = re.sub(r"\n","",line)
        temp_lib = re.sub(r" .*$","",line)
        temp_freq = int(re.sub(r"^.* ","", line))
        if temp_lib in library_list:
            library_list_freq[temp_lib] = temp_freq
    library_list_freq_sorted = sorted(library_list_freq.items(), key=operator.itemgetter(1), reverse=True)
    library_list_high_freq = library_list_freq_sorted[0:100]
    library_list_high_freq = [tuple[0] for tuple in library_list_high_freq]
    library_list_low_freq = library_list_freq_sorted[-100:]
    library_list_low_freq = [tuple[0] for tuple in library_list_low_freq]

with open("analogical_library.txt","w") as sample_file:
     for library in library_list:
         sample_file.write("%s\n" % library)
         if library in model.wv.vocab:
             a = find_analogical_libraries(library,library_list)
             for pl in a:
                 new_str = " "
                 sample_file.write("%s : " % pl)
                 sample_file.write('%s\n' % str(a[pl]))
         sample_file.write("\n")
     print "Finding analogical libraries for high frequency library is completed."






