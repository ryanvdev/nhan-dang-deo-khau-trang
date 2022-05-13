import sys
import os
import numpy as np
import cv2
import time

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../'
        )
    )
)

import conf

#import imutils
from modules.SaveImages import SaveImages
from modules.explodeImage import explodeImage
from modules.FaceDetector import FaceDetector
from modules.MaskPredictor import MaskPredictor
from modules.Fps import Fps
from modules.AudioPlayer import AudioPlayer
from modules import draw

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main():
    #Initialize
    fps = Fps()

    # ImageSave
    saveImages = SaveImages()
    saveImages.setDirSave(conf.DIR_SAVE_IMAGES)
    saveImages.setDelay(3)

    #Audio
    audioPlayer = AudioPlayer()
    audioPlayer.setAudioFilePath(conf.AUDIO_FILE_PATH)
    audioPlayer.tryImportLib()
    audioPlayer.setTimeSleepAfterPlayed(2)

    #FaceDetector
    faceDetector = FaceDetector()
    faceDetector.setMinAccuracy(0.4)
    faceDetector.loadFaceNetFromDir(conf.FACE_CAFFE_DNN_PATH)

    #MaskPredictor
    maskPredictor = MaskPredictor()
    maskPredictor.loadModelFromFile(conf.MODEL_IN_PATH)

    print('[i] Đang khởi tạo VideoCapture')
    videoCapture = cv2.VideoCapture()
    videoCapture.open(conf.VIDEO_ADDRESS)
    time.sleep(1)
    print('[=>] Khởi tạo VideoCapture thành công')


    def isWithoutMask(predict:list)->bool:
        return predict[0] < 0.5

    while True:
        success, img = videoCapture.read()
        if not success:
            break

        detectResult = faceDetector.detect(img)
        if len(detectResult) > 0:
            predictResult:list = maskPredictor.predict(img.copy(), detectResult)
            for predict, (accuracy, box) in zip(predictResult, detectResult):
                borderColor = (255,255,0) # Aqua

                if isWithoutMask(predict):
                    borderColor = (255,0,255) # Tím hồng
                    audioPlayer.play()

                    #region Lưu ảnh
                    if saveImages.ready():
                        saveImages.save(
                            imgs=explodeImage(img.copy(), detectResult, predictResult, isWithoutMask),
                            label='without-mask'
                        )
                    #if
                    #endregion Lưu ảnh
                #if
            #for

                #region draw
                img = cv2.rectangle(
                    img,
                    pt1=box[0:2], pt2=box[2:4],
                    color=borderColor,
                    thickness=1)

                img = draw.drawText( img,
                    f'+ Face:{round(accuracy*100, 2)}%',
                    [box[0] + 5, box[1] - 50],
                    borderColor)

                img = draw.drawText( img,
                    f'+ Mask:{round(predict[0]*100, 2)}%',
                    [box[0] + 5, box[1] - 30],
                    borderColor)
                #endregion draw
            #for
        #if

        img = draw.drawText(img, f'{fps.nextStr()} fps', (10,20))

        cv2.imshow(winname=conf.IMSHOW_WIN_NAME, mat=img)
        if (cv2.waitKey(1) in conf.KEY_STOP) or (cv2.getWindowProperty(conf.IMSHOW_WIN_NAME, cv2.WND_PROP_VISIBLE) < 1):
            break
    # while

    print('[i] Đang dọn dẹp bộ nhớ')
    videoCapture.release()
    cv2.destroyAllWindows()
# main

if __name__=='__main__':
    os.system('cls')
    main()

print('[i] EXITING')