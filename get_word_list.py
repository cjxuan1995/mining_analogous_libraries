import DataPreprocessing as DP

data_processor = DP.Processor()
rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000")
data_processor.write_data_to_file("processed_data1.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 5000000")
data_processor.write_data_to_file("processed_data2.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 10000000")
data_processor.write_data_to_file("processed_data3.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 15000000")
data_processor.write_data_to_file("processed_data4.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 20000000")
data_processor.write_data_to_file("processed_data5.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 25000000")
data_processor.write_data_to_file("processed_data6.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 30000000")
data_processor.write_data_to_file("processed_data7.txt", rows)

rows = data_processor.get_data_from_db("localhost", "root", "cjx209114319", "stack_overflow", "select body from posts limit 5000000 offset 35000000")
data_processor.write_data_to_file("processed_data8.txt", rows)





