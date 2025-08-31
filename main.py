# import mediapipe as mp
# import nummpy as np
import pandas, cv2, os, time

# hands = mp.solutions.hands.Hands()
# pose = mp.solutions.pose.Pose()
pose_take = [0,11,12,13,14,15,16]
cpose = ""
nframes = 0
perpose = 0

cap = cv2.VideoCapture(0)

def print_start_banner():
    print(r"""
==============================         
  _____ _             _   
 / ____| |           | |  
| (___ | |_ __ _ _ __| |_ 
 \___ \| __/ _` | '__| __|
 ____) | || (_| | |  | |_ 
|_____/ \__\__,_|_|   \__|
          
==============================
""")

def start():
    print_start_banner()
    global nframes, cpose, perpose
    while nframes<300:
        nframes += 1
        ret, img = cap.read()
        cv2.putText(img, f"Rec-{nframes}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        frame = cv2.resize(img, (224, 224))


        cv2.imshow("Recoarding..", img)
        if cv2.waitKey(1) == 13:
            break
    cv2.destroyAllWindows()

def cancel():
    pass

while True:
    print("")
    print("")
    order = input("Type 'cs' to cancel, 'exc' to exit and '' to continue:")
    if order == "cs":
        cancel()
    elif order == "exc":
        break
    elif order == "ad":
        pass
    else:
        nframes = 0
        start()
cap.release()
cv2.destroyAllWindows() 