import re
import MySQLdb

db = MySQLdb.connect("localhost", "root", "cjx209114319", "stack_overflow")
cursor = db.cursor()
cursor.execute("select Tags from posts")
rows = [item[0] for item in cursor.fetchall()]
db.close()
tag_list = []
with open("tag_sentences.txt", "w") as tags_file:
    for row in rows:
        tag_sentence = str(row)
        tag_sentence = re.sub("<|>", " ", tag_sentence)
        if tag_sentence != "None":
            temp_tag_list = tag_sentence.split()
            new_str = ' '
            tags_file.write("%s\n" % new_str.join(temp_tag_list))
    #         for tag in temp_tag_list:
    #             tag = re.sub("-\d.*$", "", tag)
    #             if not (tag in tag_list):
    #                 tag_list.append(tag)
    # for tag in tag_list:
    #     tags_file.write("%s\n" % tag)

