from utils import grayscale,preprocessing,equalize,getCalssName
import numpy as np
import cv2
import keras



def main() :
    frameWidth= 640         # CAMERA RESOLUTION
    frameHeight = 480
    brightness = 180
    threshold = 0.75         # PROBABLITY THRESHOLD
    font = cv2.FONT_HERSHEY_SIMPLEX
    ##############################################
    print('===================')
    # SETUP THE VIDEO CAMERA
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)
    # IMPORT THE TRANNIED MODEL
    model=keras.models.load_model("model.keras")
    
    
    while True:

        # READ IMAGE
        success, imgOrignal = cap.read()
        
        # PROCESS IMAGE
        img = np.asarray(imgOrignal)
        img = cv2.resize(img, (32, 32))
        img = preprocessing(img)
        cv2.imshow("Processed Image", img)
        img = img.reshape(1, 32, 32, 1)
        cv2.putText(imgOrignal, "CLASS: " , (20, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(imgOrignal, "PROBABILITY: ", (20, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        # PREDICT IMAGE
        predictions = model.predict(img)
        classIndex = model.predict_classes(img)
        probabilityValue =np.amax(predictions)
        if probabilityValue > threshold:
            #print(getCalssName(classIndex))
            cv2.putText(imgOrignal,str(classIndex)+" "+str(getCalssName(classIndex)), (120, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(imgOrignal, str(round(probabilityValue*100,2) )+"%", (180, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Result", imgOrignal)
            
            if cv2.waitKey(1) and 0xFF == ord('q'):
                break
            



if __name__=="__main__":
    main()