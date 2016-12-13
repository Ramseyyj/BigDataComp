import csv
import datetime
import os

# train_dataset_file = 'F:\\AdMaster_competition_dataset\\AdMaster_train_dataset'
# test_dataset_file = 'F:\\AdMaster_competition_dataset\\final_ccf_test_0919'
train_dataset_file1 = 'F:\\AdMaster_competition_dataset\\ccf_data_1'
train_dataset_file2 = 'F:\\AdMaster_competition_dataset\\ccf_data_2'
train_dataset_file3 = 'F:\\AdMaster_competition_dataset\\ccf_data_3'
test_dataset_file1 = 'F:\\AdMaster_competition_dataset\\test_data_1_1118'
test_dataset_file2 = 'F:\\AdMaster_competition_dataset\\test_data_2_1118'
media_info_file = 'F:\\AdMaster_competition_dataset\\ccf_media_info.csv'

output_train_file = 'F:\\AdMaster_competition_dataset\\ccf_data_train'
output_test_file = 'F:\\AdMaster_competition_dataset\\ccf_data_test'


def print_csv_in_lines(file, lines=0):

    with open(file, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
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
        spamreader = csv.reader(csvfile, delimiter=',')

        with open(reduce_file, 'w', newline='\n') as csvwritefile:
            csvwriter = csv.writer(csvwritefile, delimiter=',')
            testline = reduce_lines
            for row in spamreader:
                csvwriter.writerow(row)
                testline -= 1
                if testline == 0:
                    break


def combine_train_csv_files(file1, file2, file3, outputfile):

    with open(file1, 'r', encoding='utf-8') as csvfile1:
        with open(file2, 'r', encoding='utf-8') as csvfile2:
            with open(file3, 'r', encoding='utf-8') as csvfile3:
                spamreader1 = csv.reader(csvfile1, delimiter=',')
                spamreader2 = csv.reader(csvfile2, delimiter=',')
                spamreader3 = csv.reader(csvfile3, delimiter=',')

                temp_file = open(outputfile, 'w', newline='\n')
                csvwriter = csv.writer(temp_file, delimiter=',')

                first_line_flag = True

                now_line = 0
                count = 0
                for row in spamreader1:
                    now_line += 1
                    if now_line == 100000:
                        count += 1
                        print(count)
                        now_line = 0

                    if first_line_flag:
                        first_line_flag = False
                    else:
                        csvwriter.writerow(row)

                for row in spamreader2:
                    now_line += 1
                    if now_line == 100000:
                        count += 1
                        print(count)
                        now_line = 0

                    csvwriter.writerow(row)

                for row in spamreader3:
                    now_line += 1
                    if now_line == 100000:
                        count += 1
                        print(count)
                        now_line = 0

                    csvwriter.writerow(row)

                temp_file.close()


def combine_test_csv_files(file1, file2, outputfile):

    with open(file1, 'r', encoding='utf-8') as csvfile1:
        with open(file2, 'r', encoding='utf-8') as csvfile2:
            spamreader1 = csv.reader(csvfile1, delimiter=',')
            spamreader2 = csv.reader(csvfile2, delimiter=',')

            temp_file = open(outputfile, 'w', newline='\n')
            csvwriter = csv.writer(temp_file, delimiter=',')

            first_line_flag = True

            now_line = 0
            count = 0
            for row in spamreader1:
                now_line += 1
                if now_line == 100000:
                    count += 1
                    print(count)
                    now_line = 0

                if first_line_flag:
                    first_line_flag = False
                else:
                    csvwriter.writerow(row)

            for row in spamreader2:
                now_line += 1
                if now_line == 100000:
                    count += 1
                    print(count)
                    now_line = 0

                csvwriter.writerow(row)

            temp_file.close()


reduce_dataset(test_dataset_file1, 'small_test', 100)
print_csv_in_lines('small_test', 10)

# combine_train_csv_files(train_dataset_file1, train_dataset_file2, train_dataset_file3, output_train_file)
# combine_test_csv_files(test_dataset_file1, test_dataset_file2, output_test_file)

