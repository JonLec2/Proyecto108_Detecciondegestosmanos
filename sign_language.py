import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    results = hands.process(img)


    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            # Acceder a los puntos de referencia por su posición
           # for id ,lm in enumerate(hand_landmark.landmark):
           #     lm_list.append(lm)

            
             #Dibujar puntos de un color en las puntas de los dedos
            for index in finger_tips:
                lendmarks=results.multi_hand_landmarks[0].landmark
                finger_y=lendmarks[index].y
                finger_x=lendmarks[index].x
    
                x,y=int(finger_x*w), int(finger_y*h)
                cv2.circle(img, (x,y), 15, (255,0,0), cv2.FILLED)

                finger_fold_status=[]

                if finger_x<lendmarks[index-3].x:
                    cv2.circle(img, (x,y), 15, (255,255,0), cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

                #print(finger_fold_status)

                if all(finger_fold_status):
                    if lendmarks[thumb_tip].y<lendmarks[thumb_tip-1].y<lendmarks[thumb_tip-2].y:
                        cv2.putText(img, "Me gusta", (150,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

                    if lendmarks[thumb_tip].y>lendmarks[thumb_tip-1].y>lendmarks[thumb_tip-2].y:
                        cv2.putText(img, "No me gusta", (150,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,69,0), 3)
           
           #Dibujar lineas y puntos
            mp_draw.draw_landmarks(img, hand_landmark,
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),
            mp_draw.DrawingSpec((0,255,0),4,2))

    key = cv2.waitKey(25)
    if key == 32:
     print("Detenido")
     break
    

    cv2.imshow("Rastreo de manos", img)
    cv2.waitKey(1)
