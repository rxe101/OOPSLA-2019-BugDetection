def counter_data(input, n):
    counter = {}
    k = 1
    for line in input:
        tokens = line.split(" ")
        length = len(tokens) - n + 1
        if n > length:
            continue
        for i in range(length):
            new_token = []
            for j in range(n):
                new_token.append(tokens[i + j])
            key_ = (" ").join(new_token)
            if key_ in counter.keys():
                counter[key_] += 1
            else:
                counter[key_] = 1
        k += 1
    return counter


def get_data(input, n, top_num):
    list_1 = counter_ngram(input, n-1)
    list_2 = counter_ngram(input, n)
    output_list = {}
    for gram_2 in list_2:
        gram_2f = gram_2.strip().split(" ")[0:-1]
        gram_2f = (" ").join(gram_2f)
        if gram_2f in list_1.keys():
            if gram_2f in output_list.keys():
                if len(output_list[gram_2f]) > top_num:
                    for gram_check in output_list[gram_2f]:
                        if output_list[gram_2f][gram_check] < list_2[gram_2] / list_1[gram_2f]:
                            output_list[gram_2f].pop(gram_check)
                            output_list[gram_2f][gram_2] = list_2[gram_2] / list_1[gram_2f]
                            break
                else:
                    output_list[gram_2f][gram_2] = list_2[gram_2] / list_1[gram_2f]
            else:
                new_list = {}
                new_list[gram_2] = list_2[gram_2] / list_1[gram_2f]
                output_list[gram_2f] = new_list
    return output_list


def traversal_dir(root):
    list = []
    if (os.path.exists(root)):
        files = os.listdir(root)
        for file in files:
            m = os.path.join(root, file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                list.append(h[1])
        return list


def format_fix(file_name):
    input_file = open(file_name, "r", encoding='utf8')
    lines = input_file.readlines()
    new_lines = []
    for line in lines:
        new_line = line.strip()
        line_ = line.strip()
        word_before = 0
        counter = 0
        for i in range(len(line_)):
            if i == 0:
                if line_[i].isalpha() == 1 or line_[i].isdigit() == 1:
                    word_before = 1
                else:
                    word_before = 0
            elif word_before == 1:
                if line_[i].isalpha() == 1 or line_[i].isdigit() == 1:
                    continue
                else:
                    word_before = 0
                    if line_[i] != " ":
                        str_1 = new_line[0:i+counter]
                        str_2 = new_line[i+counter:]
                        new_line = str_1 + " " + str_2
                        counter += 1
            elif word_before == 0:
                if line_[i].isalpha() == 1 or line_[i].isdigit() == 1:
                    word_before = 1
                else:
                    word_before = 0
                if line[i] != " ":
                    str_1 = new_line[0:i+counter]
                    str_2 = new_line[i+counter:]
                    new_line = str_1 + " " + str_2
                    counter += 1
        if new_line.strip() != "" and new_line.strip()[len(new_line)-1] == ";":
            new_lines.append(new_line)
    output_file = open(file_name, "w", encoding='utf8')
    for line in new_lines:
        print(line, file=output_file)


def prepare_data(root):
    project_list = traversal_dir(root)
    for project in project_list:
        path = root + "\\" + project
        counter = 0
        check = os.path.exists(root + "\\prepare_data\\" + project)
        if not check:
            os.makedirs(root + "\\prepare_data\\" + project)
        for project_path, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.java'):
                    check = os.path.exists(root + "\\prepare_data\\" + project)
                    if not check:
                        os.makedirs(root + "\\prepare_data\\" + project)
                    shutil.copyfile(os.path.join(project_path, filename), os.path.join(root + "\\prepare_data\\" + project, filename))
                    counter += 1
        counter_2 = 0
        folder = 1
        for project_path, dirnames, filenames in os.walk(root + "\\prepare_data\\" + project):
            for filename in filenames:
                counter_2 += 1
                if counter_2 > counter/10 and folder != 10:
                    counter_2 = 1
                    folder += 1
                check = os.path.exists(root + "\\prepared_data\\" + project + "\\" + str(folder))
                if not check:
                    os.makedirs(root + "\\prepared_data\\" + project + "\\" + str(folder))
                shutil.copyfile(os.path.join(project_path, filename), os.path.join(root + "\\prepared_data\\" + project + "\\" + str(folder), filename))


def rm_comment(file_name):
    input_file = open(file_name, "r", encoding='utf8')
    lines = input_file.readlines()
    new_lines = []
    start_point = 0
    for line in lines:
        new_line = line.strip()
        if start_point == 0:
            if new_line.find("//") != -1:
                new_line = new_line[0: new_line.find("//")]
            elif new_line.find("/*") != -1:
                new_line = ""
                start_point = 1
        elif new_line.find("*/") != -1:
            new_line = ""
            start_point = 0
        else:
            new_line = ""
        if new_line != "":
            new_lines.append(new_line)
    output_file = open(file_name, "w", encoding='utf8')
    for line in new_lines:
        print(line, file=output_file)


def get_method(file_name):
    input_file = open(file_name, "r", encoding='utf8')
    lines = input_file.readlines()
    mark = 0
    new_lines = []
    file_num = 0
    start_mark = 0
    for line in lines:
        line_ = line.strip()
        new_line = ""
        for i in range(len(line_)):
            if mark == 2 and line_[i] != "}":
                new_line += line_[i]
            if i == 0:
                if line_[i] == "{":
                    mark += 1
                if line_[i] == "}":
                    mark -= 1
            elif line_[i] == "{" and line_[i-1] != "\\":
                mark += 1
            elif line_[i] == "}" and line_[i-1] != "\\":
                mark -= 1
        if mark == 2:
            if start_mark == 0:
                start_mark = 1
                new_lines.append(new_line)
            else:
                new_lines.append(new_line)
        if mark < 2:
            if start_mark == 0:
                continue
            else:
                start_mark = 0
                if new_line:
                    new_lines.append(new_line)
                file_token = file_name.split("\\")
                temp = file_token[-1].split(".")
                file_token[-1] = temp[0] + "_" + str(file_num) + "." + temp[1]
                #print(file_token)
                file_token = ("\\").join(file_token)
                output_file = open(file_token, "w", encoding='utf8')
                for line_n in new_lines:
                    print(line_n, file=output_file)
                file_num += 1
                new_lines = []


def replace_string(file_name):
    input_file = open(file_name, "r", encoding='utf8')
    lines = input_file.readlines()
    new_lines = []
    for line in lines:
        line_ = line.strip()
        tokens = line_.split(" ")
        for i in range(len(tokens)):
            if tokens[i].isdigit():
                tokens.pop(i)
                tokens.insert(i, "HOLDER_INT")
        start = -1
        mark = 0
        i = 0
        total_len = len(tokens)
        while 1:
            if start == -1:
                if tokens[i] == "\"":
                    start = i
                    mark = 1
                elif tokens[i] =="\'":
                    start = i
                    mark = 2
            else:
                if tokens[i] == "\"" and mark == 1:
                    for j in range(i-start+1):
                        tokens.pop(start)
                    tokens.insert(start, "HOLDER_STRING")
                    total_len = total_len - i + start
                    i = start
                    start = -1
                if tokens[i] == "\'" and mark == 2:
                    for j in range(i-start+1):
                        tokens.pop(start)
                    tokens.insert(start, "HOLDER_STRING")
                    total_len = total_len - i + start
                    i = start
                    start = -1
            i += 1
            if i >= total_len:
                break
        new_line = (" ").join(tokens)
        new_line = new_line.lower()
        new_lines.append(new_line)
    output_file = open(file_name, "w", encoding='utf8')
    for line in new_lines:
        print(line, file=output_file)


def process_code(root):
    path = root + "\\prepared_data\\"
    for project_path, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.java'):
                rm_comment(os.path.join(project_path, filename))
                get_method(os.path.join(project_path, filename))
                os.remove(os.path.join(project_path, filename))
    #for project_path, dirnames, filenames in os.walk(path):
        #for filename in filenames:
            #if filename.endswith('.java'):
                #format_fix(os.path.join(project_path, filename))
                #replace_string(os.path.join(project_path, filename))


def get_input(root, project_list, project, folder):
    path = root + "\\prepared_data\\"
    input_list = []
    for project_ in project_list:
        for i in range(10):
            if project_ == project and i == folder - 1:
                continue
            else:
                path_ = path + project_ + "\\" + str(i+1)
                for project_path, dirnames, filenames in os.walk(path_):
                    for filename in filenames:
                        if filename.endswith('.java'):
                            #print("Reading..." + os.path.join(project_path, filename))
                            input_file = open(os.path.join(project_path, filename), "r", encoding='utf8')
                            line = ""
                            while 1:
                                line_ = input_file.readline().strip()
                                line = line + line_.strip() + " "
                                if not line_:
                                    break
                            input_list.append(line.strip())
    return input_list


def get_test(root, project_list, project, folder):
    path = root + "\\prepared_data\\"
    test_list = []
    for project_ in project_list:
        for i in range(10):
            if project_ == project and i == folder -1:
                path_ = path + project_ + "\\" + str(i + 1)
                for project_path, dirnames, filenames in os.walk(path_):
                    for filename in filenames:
                        if filename.endswith('.java'):
                            input_file = open(os.path.join(project_path, filename), "r", encoding='utf8')
                            line = ""
                            while 1:
                                line_ = input_file.readline().strip()
                                line = line + line_ + " "
                                if not line_:
                                    break
                            test_list.append(line.strip())
            else:
                continue
    return test_list