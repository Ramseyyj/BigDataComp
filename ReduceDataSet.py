import csv
import datetime
import os
from user_agents import parse


train_dataset_file = 'F:\\AdMaster_competition_dataset\\ccf_data_train'
test_dataset_file = 'F:\\AdMaster_competition_dataset\\ccf_data_test'
media_info_file = 'F:\\AdMaster_competition_dataset\\ccf_media_info.csv'

small_train_dataset_file = 'small_train_dataset'


def deal_with_media_info():

    category_set = set()
    first_type_set = set()
    first_second__set = set()

    with open(media_info_file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        flag = False
        for row in spamreader:
            if flag:
                category_set.add(row[1])
                first_type_set.add(row[2])
                first_second__set.add((row[2], row[3]))
            else:
                flag = True

    category_list = list(category_set)
    first_type_list = list(first_type_set)
    first_second_list = list(first_second__set)

    category_id_list = []
    first_type_id_list = []
    first_second_id_list = []

    for i in range(len(category_list)):
        category_id_list.append(set())

    for i in range(len(first_type_list)):
        first_type_id_list.append(set())

    for i in range(len(first_second_list)):
        first_second_id_list.append(set())

    with open(media_info_file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        flag = False
        for row in spamreader:

            if flag:
                category_id_list[category_list.index(row[1])].add(row[0])
                first_type_id_list[first_type_list.index(row[2])].add(row[0])
                first_second_id_list[first_second_list.index((row[2], row[3]))].add(row[0])

            else:
                flag = True

    category_dict = dict(zip(category_list, category_id_list))
    first_type_dict = dict(zip(first_type_list, first_type_id_list))
    first_second_dict = dict(zip(first_second_list, first_second_id_list))

    return category_dict, first_type_dict, first_second_dict


def print_csv_in_lines(file, lines=0):

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        if lines != 0:
            testline = lines
            for row in spamreader:
                print(row[19])
                testline -= 1
                if testline == 0:
                    break
        else:
            for row in spamreader:
                print(row)


def reduce_dataset(origin_file, reduce_file, reduce_lines):

    with open(origin_file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        with open(reduce_file, 'w', newline='\n') as csvwritefile:
            csvwriter = csv.writer(csvwritefile, delimiter=',')
            testline = reduce_lines
            for row in spamreader:
                csvwriter.writerow(row)
                testline -= 1
                if testline == 0:
                    break


def distribution(file, floder, type_dict, media_id_index, lines=0):

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        keys = []
        csvwriter = []

        for key in type_dict:
            temp_file = open(floder + '\\' + key[0] + '_' + key[1], 'w', newline='\n')
            keys.append(key)
            csvwriter.append(csv.writer(temp_file, delimiter=','))

        # if floder == 'first_second_test':
        #     for key in type_dict:
        #         temp_file = open(floder+'\\'+key[0]+'_'+key[1], 'w', newline='\n')
        #         keys.append(key)
        #         csvwriter.append(csv.writer(temp_file, delimiter=','))
        #
        # else:
        #     for key in type_dict:
        #         temp_file = open(floder+'\\'+key+'_', 'w', newline='\n')
        #         keys.append(key)
        #         csvwriter.append(csv.writer(temp_file, delimiter=','))

        writer_dict = dict(zip(keys, csvwriter))

        now_line = 0
        count = 0
        if lines != 0:
            testline = lines
            for row in spamreader:
                now_line += 1
                if now_line == 100000:
                    count += 1
                    print(count)
                    now_line = 0

                for key in type_dict:
                    if row[media_id_index] in type_dict[key]:
                        writer_dict[key].writerow(row)
                        break

                testline -= 1
                if testline == 0:
                    break
        else:
            for row in spamreader:
                now_line += 1
                if now_line == 100000:
                    count += 1
                    print(count)
                    now_line = 0

                for key in type_dict:
                    if row[media_id_index] in type_dict[key]:
                        writer_dict[key].writerow(row)
                        break


def dict_add_item(item, dict_m):

    if item in dict_m.keys():
        dict_m[item] += 1
    else:
        dict_m[item] = 1

    return dict_m


def csv_to_vectors(file):

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\x01')

        ip_dict = {}
        campid_dict = {}
        mobile_dict = {}

        line_count = 0
        for row in spamreader:
            line_count += 1

            ip = row[3]
            campid = row[10]
            mobile_type = row[13]
            app_key = row[14]
            # user_agent = parse(row[17])

            if app_key != '':
                if app_key in mobile_dict.keys():
                    mobile_dict[app_key] = dict_add_item(mobile_type, mobile_dict[app_key])
                else:
                    mobile_dict[app_key] = {}
                    mobile_dict[app_key][mobile_type] = 1

            ip_dict = dict_add_item(ip, ip_dict)
            campid_dict = dict_add_item(campid, campid_dict)

        mobile_count_in_appkey_dict = {}
        for key in mobile_dict.keys():
            temp_sum = 0
            for mobile in mobile_dict[key].keys():
                temp_sum += mobile_dict[key][mobile]
            mobile_count_in_appkey_dict[key] = temp_sum

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\x01')

        with open(file+'_num.txt', 'w', newline='\n') as writefile:

            for row in spamreader:

                rank = row[0]
                ip = row[3]
                campid = row[10]
                mobile_type = row[13]
                app_key = row[14]
                user_agent = parse(row[17])
                # flag = row[21]

                print('%8s, ' % rank, file=writefile, end='')
                # print('%s, ' % flag, file=writefile, end='')

                if user_agent.is_mobile:
                    print("1.000000", file=writefile, end='')
                else:
                    print("0.000000", file=writefile, end='')
                print(', ', file=writefile, end='')

                if app_key != '' and mobile_type != '':
                    print('%f' % (mobile_dict[app_key][mobile_type] / mobile_count_in_appkey_dict[app_key]), file=writefile, end='')
                else:
                    print("0.000000", file=writefile, end='')
                print(', ', file=writefile, end='')

                print("%f" % (ip_dict[ip] / line_count), file=writefile, end='')
                print(', ', file=writefile, end='')
                print("%f" % (campid_dict[campid] / line_count), file=writefile, end='\n')


def add_label(file):

    if '_num.txt' not in file:
        with open(file, 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\x01')

            file1 = open(file+'_num.txt', 'r', encoding='utf-8')
            file2 = open(file+'_num_1.txt', 'w')

            for row in spamreader:
                line = file1.readline().strip('\n')
                print('%s, %s' % (row[21], line), file=file2)


start_time = datetime.datetime.now()

# print_csv_in_lines(train_dataset_file, 10)


category_dict_g, first_type_dict_g, first_second_dict_g = deal_with_media_info()
# print(category_dict_g)
# print(first_type_dict_g)
# print(first_second_dict_g)

# distribution(train_dataset_file, 'category', category_dict_g)
# distribution(train_dataset_file, 'first_type', first_type_dict_g)
distribution(train_dataset_file, 'first_second', first_second_dict_g, 19)
distribution(test_dataset_file, 'first_second_test', first_second_dict_g, 20)

# reduce_dataset(train_dataset_file, small_train_dataset_file, 10000000)

# reduce_dataset(train_dataset_file, 'small_test', 100)
# print_csv_in_lines('small_test', 10)

# category_dir = os.path.abspath('.')+'\\category'
# first_type_dir = os.path.abspath('.')+'\\first_type'
# first_second_dir = os.path.abspath('.')+'\\first_second_test'
#
# for parent, dirnames, filenames in os.walk(category_dir):
#     for filename in filenames:
#         csv_to_vectors(os.path.join(parent, filename))
#         print('%s is finish' % filename)
#
# for parent, dirnames, filenames in os.walk(first_type_dir):
#     for filename in filenames:
#         csv_to_vectors(os.path.join(parent, filename))
#         print('%s is finish' % filename)

# for parent, dirnames, filenames in os.walk(first_second_dir):
#     for filename in filenames:
#         csv_to_vectors(os.path.join(parent, filename))
#         print('%s is finish' % filename)

# csv_to_vectors('small_test')
# add_label('small_test')

end_time = datetime.datetime.now()
print("运行时间：%ds" % (end_time-start_time).seconds)
