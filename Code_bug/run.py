import os
import shutil
import time


def main_process(root, n, top_num, max_len):
    project_list = traversal_dir(root)
    output = 0
    counter = 0
    for project_ in project_list:
        for i in range(10):
            start = time.time()
            result = evaluation(test_data, top_num, n, max_len)
            print("Results: ", result)
            output = output + result
            counter += 1
            print("Time used: ", time.time() - start)
            print(output)
            print(counter)
    return output/counter


code_root = ""
n = 3
top_num = 5
max_len = 12
result = main_process(code_root, n, top_num, max_len)