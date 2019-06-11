import pickle
import os
import configparser
import json


def get_buglist(file_list, bug_list, bug_fix_path):
    buggy_lines=[]
    for bug in bug_list:
        bug_id = bug[3]
        bug_path = bug[4].strip()
        bug_path = bug_path.split("/")
        bug_path.pop(0)
        bug_path.pop(0)
        bug_path = ("/").join(bug_path)
        for project_path, dirnames, filenames in os.walk(bug_fix_path):
            for filename in filenames:
                if filename.find(bug_id) != -1:
                    file_ = open(os.path.join(project_path, filename), "r")
                    lines_ = file_.readlines()
                    for line_ in lines_:
                        tokens_ = line_.split()
                        if len(tokens_) > 1:
                            if tokens_[0] == "-":
                                tokens_.pop(0)
                                tokens_ = (" ").join(tokens_)
                                for i in range(len(file_list)):
                                    if file_list[i][0] == bug_path and file_list[i][1].find(tokens_) != -1:
                                        new_buggy_line = []
                                        new_buggy_line.append(bug_path)
                                        new_buggy_line.append(tokens_)
                                        if not new_buggy_line in buggy_lines:
                                            buggy_lines.append(new_buggy_line)
    return buggy_lines


def code_rollback(input_path, output_path, bug_summary, project_name, version_output, bug_fix_path):
    with open(bug_summary, 'rb') as f:
        bugs = pickle.load(f)
    file_set = []
    for project_path, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            if filename.endswith('.java'):
                file_name = os.path.join(project_path, filename)
                file_ = open(file_name, "r")
                file_infor = file_.read()
                file_name = file_name[len(input_path):]
                new_file = []
                new_file.append(file_name.strip())
                new_file.append(file_infor)
                new_file.append(99999)
                file_set.append(new_file)
    for bug in bugs:
        bug_infor = bug[2].strip()
        bug_id = bug[3].strip().split("-")
        bug_id = int(bug_id[1])
        bug_path = bug[4].strip()
        bug_path = bug_path.split("/")
        bug_path.pop(0)
        bug_path.pop(0)
        bug_path = ("/").join(bug_path)
        for i in range(len(file_set)):
            if file_set[i][0] == bug_path and file_set[i][2] < bug_id:
                file_set[i][1] = bug_infor
                file_set[i][2] = bug_id
    buggy_line_list = get_buglist(file_set, bugs, bug_fix_path)
    for file_check in file_set:
        path_full = output_path + project_name + "/" + version_output + "/" + file_check[0]
        folder_path_full = path_full.split("/")
        folder_path_full.pop(-1)
        folder_path_full = ("/").join(folder_path_full)
        check = os.path.exists(folder_path_full)
        if not check:
            os.makedirs(folder_path_full)
        file_ = open(path_full, "w")
        print(file_check[1], file=file_)
    file_ = open(output_path + project_name + "_" + version_output + "_buggy_list.txt", "a")
    print(project_name)
    print(version_output)
    for bug_line in buggy_line_list:
        print(bug_line[0], file=file_)
        print(bug_line[1], file=file_)


ver_intput = open("versions.json","r")
versions = json.load(ver_intput)
config = configparser.ConfigParser()
input_root = config.get('baseconf', 'data_path')
output_path = config.get('baseconf', 'processed_data_path')
buggy_root = input_root
bug_fix_path_ = config.get('baseconf', 'patch_file_path')
for project_ in versions:
    project_name = project_
    for version_ in versions[project_]:
        input_path = input_root + project_name + "/" + version_ + "/"
        bug_path = buggy_root + project_name + "/" + version_ + ".pickle"
        bug_fix_path = bug_fix_path_ + project_name + "/patch_files/"
        code_rollback(input_path, output_path, bug_path, project_name, version_, bug_fix_path)