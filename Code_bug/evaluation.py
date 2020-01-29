import os
import shutil
import time


def evaluation(input_data, gram_list, n, max_len):
    true_false = 0
    counter = 0
    file_num = 0
    for line in input_data:
        file_num += 1
        print("Calculating...", file_num, "/", len(input_data))
        tokens = line.split(" ")
        start_pos = 0
        for i in range(len(tokens)):
            if i > n - 1 and tokens[i] == ";":
                statement = tokens[start_pos:i + 1]
                if len(statement) > max_len:
                    counter += 1
                elif len(statement) > 0:
                    if start_pos == 0:
                        check_list = tokens[0:n-1]
                        value_mark = n
                        known = n - 1
                    else:
                        check_list = tokens[start_pos-n+1:start_pos]
                        known = 0
                        value_mark = start_pos
                    check_str = (" ").join(check_list).strip()
                    recommend_list = {}
                    recommend_list[check_str] = 1
                    break_mark = 0
                    value_checker = 1
                    for j in range(len(statement) - known):
                        new_recommend = {}
                        for recommend in recommend_list:
                            possible = {}
                            for gram in gram_list:
                                if gram.find(recommend) != -1:
                                    possible = gram_list[gram]
                                    break
                            if len(possible) == 0:
                                break_mark = 1
                                break
                            for poss_ in possible:
                                name_str = poss_.split(" ")
                                name_str.pop(0)
                                name_str = (" ").join(name_str)
                                new_recommend[name_str] = recommend_list[recommend] * possible[poss_]
                        temp_mark = 0
                        for check_re in new_recommend:
                            try:
                                if check_re.strip().split(" ")[-1] == tokens[value_mark + j]:
                                    value_checker = value_checker * new_recommend[check_re]
                                    temp_mark = 1
                                    break
                                else:
                                    continue
                            except:
                                continue
                        if temp_mark == 0:
                            break_mark = 1
                        if break_mark == 1:
                            break
                        recommend_list = new_recommend
                    if break_mark == 1:
                        counter += 1
                    else:
                        top_five = []
                        for re_ in recommend_list:
                            if len(top_five) < 5:
                                top_five.append(recommend_list[re_])
                            else:
                                for num_ in range(len(top_five)):
                                    if top_five[num_] < recommend_list[re_]:
                                        top_five.pop(num_)
                                        top_five.append(recommend_list[re_])
                                        break
                        for top_ in top_five:
                            if value_checker > top_:
                                true_false += 1
                                break
                        counter += 1
                start_pos = i + 1
    return true_false / counter