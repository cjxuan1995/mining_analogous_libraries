import re

def is_variant(str1, str2):
    suffix_list = ['s','es','ing','ed','er','or']
    for suffix in suffix_list:
        if (str1 + suffix == str2) or (str2 + suffix == str1):
            return True;
    return False

def is_substring(str1,str2):
    str1 = re.sub(r"[^a-zA-Z0-9+#]","",str1)
    str2 = re.sub(r"[^a-zA-Z0-9+#]","",str2)
    if str1 != str2 and not is_variant(str1, str2):
        if (str1.find(str2) != -1) or (str2.find(str1) != -1):
            return True
    return False


with open("library_synonym.txt","r") as lib_syn_file:
    with open("library_synonym_processed.txt", "w") as lib_syn_pro_file:
        for line in lib_syn_file:
            line = re.sub(r"\n","",line)
            temp_term_list = line.split()
            standard_term = temp_term_list[0]
            new_term_list = [standard_term]
            for index in range(1, len(temp_term_list)):
                if not is_substring(standard_term, temp_term_list[index]):
                    new_term_list.append(temp_term_list[index])
            new_str = " "
            if len(new_term_list) > 1:
                lib_syn_pro_file.write("%s\n" % new_str.join(new_term_list))
