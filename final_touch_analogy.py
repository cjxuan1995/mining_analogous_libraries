import re
count = 0

def normalize(string):
    return re.sub(r"_0\..*$","", string)

def uni_index(list_1, std_lib):
    new_list = []
    index_list = []
    for element in list_1:
        if element not in new_list and element != std_lib:
            new_list.append(element)
            index_list.append(list_1.index(element))
    return index_list

pl_list = ['java','c#', 'javascript','c++','python','php']
with open("analogical_library.txt", "r") as draft_1:
    with open("analogical_library_draft1.txt", "w") as draft_3:
        for line in draft_1:
            line = re.sub(r"\), \(", " ", line)
            line = re.sub(r"[][()']", "", line)
            line = re.sub(r": ", "\t", line)
            line = re.sub(r", ", "_", line)
            lib_list = re.sub(r".*?\t?","", line).split()
            #draft_2.write("%s" % line)
            if len(lib_list) == 1 and lib_list[0] not in pl_list:
                temp_std_lib = lib_list[0]
                draft_3.write("\n")
                draft_3.write("%s\n" % lib_list[0])
            if len(lib_list) == 1 and lib_list[0] in pl_list:
                draft_3.write("%s\t\n" % lib_list[0])
            if len(lib_list) > 1:
                lib_list_copy = [lib_list[index] for index in range(1, len(lib_list))]
                normalized_lib_list = [normalize(lib) for lib in lib_list_copy]
                print temp_std_lib
                print lib_list
                index_list = uni_index(normalized_lib_list, temp_std_lib)
                index_list = [(item + 1) for item in index_list]
                if index_list:
                    lib_list = [lib_list[0]] + [lib_list[index] for index in index_list]
                    print lib_list
                new_str = " "
                draft_3.write("%s\n" % (lib_list[0] + "\t" + new_str.join(lib_list[1:])))



        print count

#with open("analogical_library_low_freq_40.txt", "r") as draft_3:
    #with open("analogical_library_low_freq_processed.txt", "w") as draft_4:
        #for line in draft_3:
            #line = re.sub(r'_[0-9.]*', ' ', line)
            #draft_4.write("%s" % line)