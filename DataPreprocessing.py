import re
import MySQLdb

def getDataFromDB():
    host = raw_input("host: ")
    user = raw_input("user: ")
    password = raw_input("password: ")
    database = raw_input("database: ")
    db = MySQLdb.connect(host, user, password, database)
    cursor = db.cursor()
    cursor.execute("select Body from posts limit 1000")
    rows = [item[0] for item in cursor.fetchall()]
    db.close()
    return rows

def processDataRegex(data):
    symbolList = ['=', '*', '{', '}', '[', ']', '&', '$'] #This line and the next line mean that if any of those symbols appear in the code block, it will be considered as code, which will be removed.
    pattern = re.sub("<code>(.*?)</code>",
                     lambda m: "" if any(symbol in m.group(1) for symbol in symbolList) else m.group(), data,
                     flags=re.S)

    pattern = re.sub("</?[a-z][^>]*>", "", pattern)
    pattern = re.sub("&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;", "", pattern) #remove some html entities
    pattern = re.sub("\*|~|`", "", pattern) #remove some symbols

    pattern = re.sub("http.+?&#xA", "&#xA", pattern)
    pattern = re.sub("http.+? ", " ", pattern)
    pattern = re.sub("http.+?$", "", pattern)
    #Those three lines above are for handling url

    pattern = pattern.lower()
    return pattern

def separateSentAndWord(processedData): #This function is for separating sentences based on punctuations and separating words.
    wordList = []
    sentence_list = re.split("&#xa;|!|\?|;|\. ", processedData)

    for sentence in sentence_list:
        if (not sentence.isspace()) and sentence:
            sentence = re.sub("\.$", "", sentence)
            wordList.append(re.sub("[^\w|+|.|#|-]", " ", sentence).split()) #Keep letters, numbers, +, ., # and -. Otherwise, replace them with space. The reason for keeping +, ., # is because they may be part of some software terms. C++, C#, angular.js and so on.

    return wordList


def main():
    rows = getDataFromDB()
    fileName = raw_input("The name of the file storing processed data: ")
    file = open(fileName, "w")
    for row in rows:
        processedData = processDataRegex(str(row))
        wordList = separateSentAndWord(processedData)

        for words in wordList:
            newStr = " "
            file.write("%s\n" % newStr.join(words))

    file.close()

if __name__ == "__main__": main()
