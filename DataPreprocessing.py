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
    symbolList = ['=', '*', '{', '}', '[', ']', '&', '$']
    pattern = re.sub("<code>(.*?)</code>",
                     lambda m: "" if any(symbol in m.group(1) for symbol in symbolList) else m.group(), data,
                     flags=re.S)

    pattern = re.sub("</?[a-z][^>]*>", "", pattern)
    pattern = re.sub("&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;", "", pattern)
    pattern = re.sub("\*|~|`", "", pattern)

    pattern = re.sub("http.+?&#xA", "&#xA", pattern)
    pattern = re.sub("http.+? ", " ", pattern)
    pattern = re.sub("http.+?$", "", pattern)
    pattern = pattern.lower()
    return pattern

def separateSentAndWord(processedData):
    wordList = []
    sentence_list = re.split("&#xa;|!|\?|;|\. ", processedData)

    for sentence in sentence_list:
        if (not sentence.isspace()) and sentence:
            sentence = re.sub("\.$", "", sentence)
            wordList.append(re.sub("[^\w|+|.|#|-]", " ", sentence).split())

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
