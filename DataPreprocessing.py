import re
import MySQLdb


class Processor(object):
    """The Processor class process the raw stack_overflow post data to more readable form.

    It contains five methods. Basically, only three methods should be accessed externally, which are get_data_from_db, write_data_to_file and write_raw_and_processed_data_to_file.
    """

    def get_data_from_db(self, host, user, password, database, command):
        """Retrieve data from a table in a MySQL database

        :param host: host name of your database
        :param user: user of your database
        :param password: password for your database
        :param database: name of the specific database storing the data
        :param command: MySQL command for getting the data
        :return: rows as a result of your MySQL query
        """
        db = MySQLdb.connect(host, user, password, database)
        cursor = db.cursor()
        cursor.execute(command)
        rows = [item[0] for item in cursor.fetchall()]
        db.close()
        return rows

    def __process_data_regex(self, data):
        """Use regular expression to clean the raw data to get more readable data

        :param data: strings, which are converted from rows retrieved from the database
        :return: strings, which are the processed data
        """
        symbol_list = ['=', '*', '{', '}', '[', ']', '&', '$']  #This line and the next line mean that if any of those symbols appear in the code block, it will be considered as code, which will be removed.
        pattern = re.sub("<code>(.*?)</code>",
                         lambda m: "" if any(symbol in m.group(1) for symbol in symbol_list) else m.group(), data,
                         flags=re.S)

        pattern = re.sub(r"</?[a-z][^>]*>", " ", pattern)
        pattern = re.sub(r"&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;|e\.g\.|i\.e\.", " ", pattern)  #remove some html entities and special expressions
        pattern = re.sub(r"\*|~|`", " ", pattern)
        pattern = re.sub(r"&#xA", ". ", pattern)

        # pattern = re.sub(r"https?://.+?&#xA", "&#xA", pattern)
        pattern = re.sub(r"https?://\S+", " ", pattern)
        # pattern = re.sub(r"https?://.+?$", "", pattern)
        pattern = pattern.lower()
        return pattern

    def __separate_sentence_and_word(self, processed_data):
        """Separate sentences and words in the processed data

        :param processed_data: strings, which are the output of __process_data_regrex
        :return: a two-dimensional list which contains all the words in the processed data.
                 For example, [[i, like, football][this, python, module, is, very, confusing]]
        """
        word_list = []
        sentence_list = re.split(r"&#xa;|&#xd;|!|\?|;|\. ", processed_data)

        for sentence in sentence_list:
            if (not sentence.isspace()) and sentence:
                sentence = re.sub(r"\.$", "", sentence)
                word_list.append(re.sub(r"[^\w|\+|\.|#|-]", " ", sentence).split())  #Keep letters, numbers, +, ., # and -. Otherwise, replace them with space. The reason for keeping +, ., # is because they may be part of some software terms. C++, C#, angular.js and so on.

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


        return word_list

    def write_data_to_file(self, file_name, rows):
        """write processed data into a file

        :param file_name: name of the file you want to store the processed data
        :param rows: output of get_data_from_db, which are rows obtains from database
        :return:
        """
        with open(file_name, 'w') as data_file:
            for row in rows:
                processed_data = self.__process_data_regex(str(row))
                word_list = self.__separate_sentence_and_word(processed_data)

                for words in word_list:
                    new_str = " "
                    if not new_str.join(words).isspace():
                        data_file.write("%s\n" % new_str.join(words))

    def write_raw_and_processed_data_to_file(self, file_name, rows):
        """write both raw data and processed data into a file

        :param file_name: name of the file you want to store the processed data
        :param rows: output of get_data_from_db, which are rows obtains from database
        :return:
        """
        with open(file_name, 'w') as data_file:
            for row in rows:
                processed_data = self.__process_data_regex(str(row))
                word_list = self.__separate_sentence_and_word(processed_data)
                data_file.write("%s\n\n" % str(row))
                data_file.write("%s\n\n" % processed_data)

                for words in word_list:
                    new_str = " "
                    data_file.write("%s\n" % new_str.join(words))

                data_file.write("\n\n\n")
