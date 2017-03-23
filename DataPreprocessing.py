import re
import MySQLdb

db = MySQLdb.connect(host = '', user = '', passwd='', db = '') #Fill in details about your MySQL database
file1 = open("raw_data.txt","w")
file2 = open("processed_data.txt","w")
i = 0
cursor = db.cursor()
cursor.execute("") #This is where you execute your MySQL query
rows = [item[0] for item in cursor.fetchall()]


for row in rows:
    sentence_list = []
    wordList = []
    data = str(row)

    #This block below is for determining what is inside <code> and </code>. Only keep those pure text content.
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "=" in m.group(1) else m.group(), data, flags=re.S)
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "+" in m.group(1) else m.group(), pattern, flags=re.S)
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "*" in m.group(1) else m.group(), pattern, flags=re.S)
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "(" in m.group(1) else m.group(), pattern, flags=re.S)
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "{" in m.group(1) else m.group(), pattern, flags=re.S)
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "&" in m.group(1) else m.group(), pattern, flags=re.S)
    pattern = re.sub("<code>(.*?)</code>", lambda m: "" if "-" in m.group(1) else m.group(), pattern, flags=re.S)

    #The block below is for removing html code and other symbols in the data to get more readable data
    pattern = re.sub("</?[a-z][^>]*>", "", pattern)
    pattern = re.sub("</?blockquote>","",pattern)
    pattern = re.sub("&#xA;"," ", pattern)
    pattern = re.sub("&nbsp;","",pattern)
    pattern = re.sub("\*","",pattern)
    pattern = re.sub("&", "", pattern)
    pattern = re.sub("~", "", pattern)
    pattern = re.sub("`", "", pattern)
    pattern = re.sub("http.*? ", " ", pattern)
    pattern = re.sub("http.*?$", "", pattern)

    pattern = pattern.lower()#lowercase all the letters in the data
    sentence_list = re.split("&#xA;|!|\?|;|\. ", pattern)#split the data into sentences

    for sentence in sentence_list:
        if (not sentence.isspace()) and sentence:
            wordList.append(re.sub("[^\w]", " ", sentence).split()) #split each sentence to words

    for words in wordList:
        for i, word in enumerate(words):
            if (i + 1) == len(words):
                file2.write("%s\n" % word) #write the list of words into a file named "processed_data". Each row in the file contains words of a sentence, and those words are separated by space.
            else:
                file2.write("%s" % word + " ")


    file1.write(str(i) + ".%s\n" % data) #write raw data into a file named "raw_data"


file1.close()
file2.close()


db.close()
