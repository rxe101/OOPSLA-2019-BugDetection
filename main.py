from __future__ import absolute_import

import os
os.environ["CUDA_VISIBLE_DEVICES"]="1"

import tensorflow as tf
import numpy as np
import math


def get_data_input(label_file):
    print("Getting input data...")
    label_f = open(label_file)
    input_set =[]
    while 1:
        path = label_f.readline()
        if not path:
            break
        temp = label_f.readline()
        path = path.strip()
        codes_list = path.split()
        input_list_line = []
        for count in range(len(codes_list)):
            input_list_line.append(codes_list[count])
        input_set.append(input_list_line)
    label_f.close()
    return input_set


def get_data_output(label_file):
    print("Getting output data...")
    output_set = []
    label_f = open(label_file)
    while 1:
        path = label_f.readline()
        if not path:
            break
        bug = label_f.readline()
        bug = bug.strip()
        codes_list = bug.split()
        output_list_line = []
        for count in range(len(codes_list)):
            output_list_line.append(codes_list[count])
        output_set.append(output_list_line)
    label_f.close()
    return output_set


def build_data_set(data_set, types_file, vectors_file, data_length):
    types = open(types_file)
    codes_list = types.readlines()
    vectors = open(vectors_file)
    vectors_list = vectors.readlines()
    vector_list = []
    for vector in vectors_list:
        vector_info = vector.split()
        vector_list.append(vector_info)
    len_x = len(data_set)
    data_set_new = np.zeros((len_x, data_length, vector_length))
    for list_num in range(len(data_set)):
        for code_pos in range(len(data_set[list_num])):
            for check_code_pos in range(len(codes_list)):
                if codes_list[check_code_pos].strip() == data_set[list_num][code_pos].strip():
                    for vector_num_pos in range(len(vector_list[check_code_pos])):
                        data_set_new[list_num, code_pos, vector_num_pos] = vector_list[check_code_pos][vector_num_pos]
    return data_set_new


def modelConstruction:
    session = tf.Session()
    gru = GRU(input_dimensions, hidden_size)
    W_output = tf.Variable(tf.truncated_normal(dtype=tf.float64, shape=(hidden_size, 1), mean=0, stddev=0.01))
    b_output = tf.Variable(tf.truncated_normal(dtype=tf.float64, shape=(1,), mean=0, stddev=0.01))
    output = tf.map_fn(lambda h_t: tf.matmul(h_t, W_output) + b_output, gru.h_t)
    expected_output = tf.placeholder(dtype=tf.float64, shape=(batch_size, time_size, 1), name='expected_output')
    loss = tf.reduce_sum(0.5 * tf.pow(output - expected_output, 2)) / float(batch_size)
    train_step = tf.train.AdamOptimizer().minimize(loss)
    init_variables = tf.global_variables_initializer()
    session.run(init_variables)