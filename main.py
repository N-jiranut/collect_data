import mediapipe as mp
import numpy as np
import pandas, cv2, os, time, math

hands = mp.solutions.hands.Hands()
pose = mp.solutions.pose.Pose()
pose_take = [0,11,12,13,14,15,16]
client=[]
main=[]
cpose = ""
npose = 0
nframes = 0

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

def save():
    global npose, client, main
    main=[]
    npose+=1
    max=len(client)
    if max<30:
        con=1
    else:
        con = math.floor(max/15)
    for id, ob in enumerate(client):
        if id%con and len(main)<1470:
            main.extend(ob)
    df = pandas.DataFrame([main])
    df.to_csv("main.csv", mode='w', index=False, header=False)
    print("added to main.csv")

def start():
    print_start_banner()
    global nframes, cpose, npose, client
    client=[]
    while nframes<300:
        nframes += 1
        row=[]
        LH=[]
        RH=[]
        BO=[]
        
        ret, img = cap.read()
        cv2.putText(img, f"Rec-{nframes}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img, f"{cpose}: {npose}", (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        frame = cv2.resize(img, (224, 224))
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        
        hand_result = hands.process(frame)
        pose_results = pose.process(frame)
        if hand_result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_result.multi_hand_landmarks):
                mp.solutions.drawing_utils.draw_landmarks(frame,hand_landmarks,mp.solutions.hands.HAND_CONNECTIONS)
                handedness = hand_result.multi_handedness[idx].classification[0].label
                for lm in hand_landmarks.landmark: 
                    x, y= lm.x, lm.y    
                    if handedness == "Left" and len(LH)<42:
                        LH.extend([x,y])
                    if handedness == "Right" and len(RH)<42:
                        RH.extend([x,y])
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            for id,lm in enumerate(landmarks):
                x, y = lm.x, lm.y
                if id in pose_take:
                    cv2.circle(frame ,(round(x*720),round(y*480)), 1, (0,0,255), 7)
                    BO.extend([x, y])    
        
        if len(LH) <= 0:
            LH = [0 for _ in range(42)]
        row.extend(LH)
        if len(RH) <= 0:
            RH = [0 for _ in range(42)]
        row.extend(RH)  
        if len(BO) <= 0:
            BO = [0 for _ in range(14)]      
        row.extend(BO)        
        row.append(cpose)
        client.append(row)
        cv2.imshow("Recoarding..", img)
        if cv2.waitKey(1) == 13:
            break
    cv2.destroyAllWindows()

def cancel():
    global client
    client=[] 
    print("data cleared!")   

def change_pose():
    global cpose, npose
    npose=0
    print("")
    print("")
    
    cpose=input("Enter pose>:")
    
    print("")
    print("")


change_pose()
while True:
    print("")
    print("")
    order = input("Type 'cs' to cancel, ad to change pose, 'exc' to exit and '' to continue:")
    if order == "cs":
        cancel()
    elif order == "exc":
        break
    elif order == "ad":
        change_pose()
    else:
        save()
        nframes = 0
        start()
cap.release()
cv2.destroyAllWindows() 