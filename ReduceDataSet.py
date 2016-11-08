import csv
import datetime

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


def distribution(file, type_dict, lines=0):

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\x01')

        keys = []
        csvwriter = []

        for key in type_dict:
            temp_file = open('first_second\\'+key[0]+'_'+key[1], 'w', newline='\n')
            keys.append(key)
            csvwriter.append(csv.writer(temp_file, delimiter='\x01'))

        writer_dict = dict(zip(keys, csvwriter))

        if lines != 0:
            testline = lines
            for row in spamreader:

                for key in type_dict:
                    if row[18] in type_dict[key]:
                        writer_dict[key].writerow(row)
                        break

                testline -= 1
                if testline == 0:
                    break
        else:
            for row in spamreader:
                print(row)


start_time = datetime.datetime.now()

category_dict_g, first_type_dict_g, first_second_dict_g = deal_with_media_info()
print(category_dict_g)
print(first_type_dict_g)
print(first_second_dict_g)

distribution(train_dataset_file, first_second_dict_g, 10000000)


# reduce_dataset(train_dataset_file, categoryfiles[0], 10000)

end_time = datetime.datetime.now()
print("运行时间：%ds" % (end_time-start_time).seconds)
