import csv
import random


train_dataset_file = 'F:\\AdMaster_competition_dataset\\AdMaster_train_dataset'
test_dataset_file = 'F:\\AdMaster_competition_dataset\\final_ccf_test_0919'
media_info_file = 'F:\\AdMaster_competition_dataset\\ccf_media_info.csv'

small_train_dataset_file = 'small_train_dataset'


def coin_algorithom(file):

    with open(file, 'r', encoding='utf-8') as csvreadfile:
        spamreader = csv.reader(csvreadfile, delimiter='\x01')

        with open(file+'_result_1.csv', 'w', encoding='utf-8', newline='\n') as csvwritefile:
            csvwriter = csv.writer(csvwritefile, delimiter='\x01')

            rank = 0
            now_line = 0
            count = 0
            for row in spamreader:

                now_line += 1
                if now_line == 100000:
                    count += 1
                    print(count)
                    now_line = 0

                if random.randint(0, 1) > 0.5:
                    line = []
                    line.append(rank)
                    csvwriter.writerow(line)

                rank += 1


def removeBom(file):
    '''移除UTF-8文件的BOM字节'''
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s == BOM else False

    f = open(file, 'rb')
    if existBom(f.read(3)):
        fbody = f.read()
        # f.close()
        with open(file, 'wb') as f:
            f.write(fbody)

coin_algorithom(test_dataset_file)
removeBom(test_dataset_file+'_result_1.csv')

