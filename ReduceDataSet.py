import csv
import datetime
import os
from user_agents import parse


train_dataset_file = 'F:\\AdMaster_competition_dataset\\AdMaster_train_dataset'
test_dataset_file = 'F:\\AdMaster_competition_dataset\\final_ccf_test_0919'
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
        spamreader = csv.reader(csvfile, delimiter='\x01')
        if lines != 0:
            testline = lines
            for row in spamreader:
                print(row)
                testline -= 1
                if testline == 0:
                    break
        else:
            for row in spamreader:
                print(row)


def reduce_dataset(origin_file, reduce_file, reduce_lines):

    with open(origin_file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\x01')

        with open(reduce_file, 'w', newline='\n') as csvwritefile:
            csvwriter = csv.writer(csvwritefile, delimiter='\x01')
            testline = reduce_lines
            for row in spamreader:
                csvwriter.writerow(row)
                testline -= 1
                if testline == 0:
                    break


def distribution(file, floder, type_dict, lines=0):

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\x01')

        keys = []
        csvwriter = []

        if floder == 'first_second':
            for key in type_dict:
                temp_file = open(floder+'\\'+key[0]+'_'+key[1], 'w', newline='\n')
                keys.append(key)
                csvwriter.append(csv.writer(temp_file, delimiter='\x01'))

        else:
            for key in type_dict:
                temp_file = open(floder+'\\'+key+'_', 'w', newline='\n')
                keys.append(key)
                csvwriter.append(csv.writer(temp_file, delimiter='\x01'))

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
                    if row[18] in type_dict[key]:
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
                    if row[18] in type_dict[key]:
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
                ip = row[3]
                campid = row[10]
                mobile_type = row[13]
                app_key = row[14]
                user_agent = parse(row[17])

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


start_time = datetime.datetime.now()

category_dict_g, first_type_dict_g, first_second_dict_g = deal_with_media_info()
# print(category_dict_g)
# print(first_type_dict_g)
# print(first_second_dict_g)

# distribution(train_dataset_file, 'category', category_dict_g)
# distribution(train_dataset_file, 'first_type', first_type_dict_g)
# distribution(train_dataset_file, 'first_second', first_second_dict_g)

# reduce_dataset(train_dataset_file, small_train_dataset_file, 10000000)

# reduce_dataset(train_dataset_file, 'small_test', 10000)
# print_csv_in_lines('small_test', 10)

first_second_dir = os.path.abspath('.')+'\\first_second'

for parent, dirnames, filenames in os.walk(first_second_dir):

    for filename in filenames:
        csv_to_vectors(os.path.join(parent, filename))

# csv_to_vectors('small_test')

end_time = datetime.datetime.now()
print("运行时间：%ds" % (end_time-start_time).seconds)
