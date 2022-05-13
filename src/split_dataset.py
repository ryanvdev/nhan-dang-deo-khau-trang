import os
import string
import sys
import imutils

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../'
        )
    )
)
import conf

import numpy as np
import cv2

def formatNumber(n:int)->string:
    strNumber = str(n)
    return (10 - len(strNumber))*'0' + strNumber

def main():
    print('[i] Load dataset từ file: ')
    print(f'     "{conf.DATASET_SHARE_FILE}" ')

    #Load data from share folder
    dataset = np.load(conf.DATASET_SHARE_FILE)
    data = dataset['data']
    labels = dataset['labels']
    names = dataset['names']

    for name in names:
        print(name)
        path = os.path.join(conf.DATASET_DIR, str(name))

        if(not os.path.exists(path)):
            print(f'Đang tạo thưc mục {name}')
            os.mkdir(path)

    oldIndex = 0
    oldLabel:str = str(labels[0])
    print(len(data))
    for i in range(0, len(data)):
        image = data[i]

        if oldLabel != str(labels[i]):
            oldIndex = 1

        fileName = f'{str(names[oldIndex])}_{formatNumber(i)}.png'
        imagePath = os.path.join(conf.DATASET_DIR, str(names[oldIndex]), fileName)
        print(imagePath)

        cv2.imwrite(imagePath, image*255)

if __name__=='__main__':
    main()