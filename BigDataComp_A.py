import csv
import datetime
import os
from user_agents import parse


train_dataset_file = 'F:\\AdMaster_competition_dataset\\AdMaster_train_dataset'
test_dataset_file = 'F:\\AdMaster_competition_dataset\\final_ccf_test_0919'
media_info_file = 'F:\\AdMaster_competition_dataset\\ccf_media_info.csv'


def dict_add_item(item, dict_m):

    if item in dict_m.keys():
        dict_m[item] += 1
    else:
        dict_m[item] = 1

    return dict_m


def print_num_vector(flag_m, spamreader, writefile, ip_dict, campid_dict, mobile_dict, mobile_count_in_appkey_dict, line_count):

    for row in spamreader:

        rank = row[0]
        ip = row[3]
        campid = row[10]
        mobile_type = row[13]
        app_key = row[14]
        user_agent = parse(row[17])

        if flag_m:
            print('%s, ' % row[21], file=writefile, end='')
        else:
            print('%8s, ' % rank, file=writefile, end='')

        if user_agent.is_mobile:
            print("1.000000", file=writefile, end='')
        else:
            print("0.000000", file=writefile, end='')
        print(', ', file=writefile, end='')

        if app_key != '' and mobile_type != '':
            print('%f' % (mobile_dict[app_key][mobile_type] / mobile_count_in_appkey_dict[app_key]), file=writefile,
                  end='')
        else:
            print("0.000000", file=writefile, end='')
        print(', ', file=writefile, end='')

        print("%f" % (ip_dict[ip] / line_count), file=writefile, end='')
        print(', ', file=writefile, end='')
        print("%f" % (campid_dict[campid] / line_count), file=writefile, end='\n')


def csv_to_vectors(parent_m, filename_m):

    file = os.path.join(parent_m, filename_m)

    test_filename = file
    train_filename = file.replace('_test', '')
    result_file = os.path.abspath('.')+'\\result_A\\'+filename_m

    with open(train_filename, 'r', encoding='utf-8') as csvfile_train:
        spamreader_train = csv.reader(csvfile_train, delimiter='\x01')

        with open(test_filename, 'r', encoding='utf-8') as csvfile_test:
            spamreader_test = csv.reader(csvfile_test, delimiter='\x01')

            ip_dict = {}
            campid_dict = {}
            mobile_dict = {}

            line_count = 0
            for row in spamreader_train:
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

            for row in spamreader_test:
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

    with open(train_filename, 'r', encoding='utf-8') as csvfile_train:
        spamreader_train = csv.reader(csvfile_train, delimiter='\x01')

        with open(test_filename, 'r', encoding='utf-8') as csvfile_test:
            spamreader_test = csv.reader(csvfile_test, delimiter='\x01')

            writefile_train = open(result_file+'_num_train.txt', 'w', newline='\n')
            writefile_test = open(result_file+'_num_test.txt', 'w', newline='\n')

            print_num_vector(True, spamreader_train, writefile_train, ip_dict, campid_dict, mobile_dict, mobile_count_in_appkey_dict, line_count)
            print_num_vector(False, spamreader_test, writefile_test, ip_dict, campid_dict, mobile_dict, mobile_count_in_appkey_dict, line_count)

last_time = datetime.datetime.now()

first_second_dir = os.path.abspath('.')+'\\first_second_test'

for parent, dirnames, filenames in os.walk(first_second_dir):

    for filename in filenames:
        csv_to_vectors(parent, filename)
        now_time = datetime.datetime.now()
        print('%s is finish, takes %d second' % (filename, (now_time - last_time).seconds))
        last_time = now_time
