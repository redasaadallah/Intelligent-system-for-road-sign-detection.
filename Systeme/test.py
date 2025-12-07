import numpy as np
import cv2
import pickle
import pyttsx3
import keyboard
import time
from threading import Thread
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen 
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
import pygame
import json
from socket import socket, AF_INET, SOCK_STREAM
folder_path = "C:/Users/Dell/Desktop/for me/SICOM/S4/projet PFA/yolo"
x=0
y="desactive"
a=1
clients = {}  # Map: nickname -> socket
PD=[]
print("nombre element est",len(PD))
sapp=0
last_execution = time.time()
z=0
#-----------------------------------------conexion----------------------------------------------
def conection():
    def handle_client(client_socket, nickname):
        global y
        global x
        global clients
        global PD
        clients[nickname] = client_socket
        print(f"[+] {nickname} connected.")
        if nickname=="client1":
                # Send 100 infinitely
            while True:
                d=str(x)
                try:
                    client_socket.send(d.encode())
                    
                    time.sleep(0.1)
                except:
                    break
        elif nickname=="client2":
            try:
                while True:
                    data = client_socket.recv(1024).decode("utf-8")
                    #response = input("Réponse au client >> ")
                    #client_socket.send(response.encode("utf-8"))
                    if data:
                        
                        if data=="off":
                            PD=[]
                            y=data
                            label1.text="Desactivé"
                            label2.text=""
                            pygame.mixer.init()
                            pygame.mixer.music.load("goodbye.mp3")
                            pygame.mixer.music.play()
                        nn=data
                        if nn=="1":
                            client_socket.sendall(json.dumps(PD).encode('utf-8'))
                            nn="0"
                        else:
                        
                            y=data
                            print(y)
                            if y=="auto":
                                label1.text="Le mode auto regulation"
                                pygame.mixer.init()
                                pygame.mixer.music.load("auto.mp3")
                                pygame.mixer.music.play()
                            if y=="alerte":
                                label1.text="Le mode alerte"
                                pygame.mixer.init()
                                pygame.mixer.music.load("alerte.mp3")
                                pygame.mixer.music.play()
                            if y=="wellcome":
                                y=1
                                print(y)
                                pygame.mixer.init()
                                pygame.mixer.music.load("wellcome.mp3")
                                pygame.mixer.music.play()
                                
            except:             
                pass
                
        client_socket.close()
        del clients[nickname]

    # Création du socket serveur
    HOST = '0.0.0.0'
    PORT = 12345

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)

    print(f"[STARTED] Server listening on {HOST}:{PORT}")

    '''s = socket(AF_INET, SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen(2)  # Autorise 2 connexions en attente
    print("Serveur en attente de connexions...")'''

    # Accepter plusieurs clients dans une boucle
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")

        # Get nickname
        client_socket.send("NICK".encode())
        nickname = client_socket.recv(1024).decode()
       
        
        
        # Démarrer un nouveau thread pour chaque client
        Thread(target=handle_client, args=(client_socket, nickname), daemon=True).start()

#-----------------------------------------------------------------------------------------------
def increment_x():
    global x
    if x==100:
        x=x
    else:   
        x += 1
        print(f"x = {x}")
        time.sleep(0.1)
def decrement_x():
    global x
    if x==0:
        x=x
    else:
        x -= 1
        print(f"x = {x}")
        time.sleep(0.1)
def work():

    # Assign up arrow key to increment and down arrow key to decrement
    keyboard.on_press_key("up", lambda _: increment_x())
    keyboard.on_press_key("down", lambda _: decrement_x())
    print("Press '↑' (up) to increase x, '↓' (down) to decrease x. Press 'esc' to stop.")
    keyboard.wait("esc")

def create():
    class ExApp(MDApp):
        def build(self):
            global box1
            global label2
            global label
            global prog
            global label1
            screen= MDScreen()
            label=MDLabel(markup=True,text=str(x)+"Km/h",halign="center",pos_hint={'center_x': .35, 'center_y': .5},font_style="Display",role="large",bold=True,text_color=(1, 1, 1, 1))
            image=Image(source="board.jpg",size_hint=[0.8,0.8],pos_hint={'center_x':0.35,'center_y':0.6})
            logo=Image(source="6.png",size_hint=[0.2,0.5],pos_hint={'center_x':0.83,'center_y':0.8})
            logo1=Image(source="6.png",size_hint=[0.5,0.5],pos_hint={'center_x':0.83,'center_y':0.3},opacity=0.1)
            prog=ProgressBar(size_hint=[0.25,1],value=x,pos_hint={'center_x': .35, 'center_y': .45})
            box1=MDBoxLayout(size_hint=[0.08,0.1],pos_hint={'center_x': .05, 'center_y': .25},radius=[50,50,50,50],md_bg_color=[0,255,0,1])
            label1=MDLabel(markup=True,pos_hint={'center_x': .82, 'center_y': .5},text="Desactivé",halign="center",font_style="Title",role="large",bold=True,text_color=(0, 0, 0, 1))
            label2=MDLabel(markup=True,pos_hint={'center_x': .5, 'center_y': .1},text="",halign="center",font_style="Title",role="large",bold=True,text_color=(0, 0, 0, 1))
            keyboard.on_press_key("up", lambda _: self.change(label,prog))
            keyboard.on_press_key("down", lambda _: self.change(label,prog))
            screen.add_widget(image)
            screen.add_widget(label)
            screen.add_widget(prog)
            screen.add_widget(box1)
            screen.add_widget(logo1)
            screen.add_widget(label1)
            screen.add_widget(label2)
            screen.add_widget(logo)
            screen.md_bg_color=[0.97,0.97,0.97]
            return screen
        def modeauto(self,instance):
            global y
            y="auto"
            print(y)
            self.label1.text="Le mode auto regulation"
            pygame.mixer.init()
            pygame.mixer.music.load("auto.mp3")
            pygame.mixer.music.play()
        def modealer(self,instance):
            global y
            y="alerte"
            self.label1.text="Le mode alerte"
            pygame.mixer.init()
            pygame.mixer.music.load("alerte.mp3")
            pygame.mixer.music.play()
        def change(self,label,prog):
            label.text=str(x)+"Km/h"
            if x<70:
                label.color=[1,1,1]
            if x>=70 and x<80:
                label.color=[1,1,0]
            if x>=80 and x<90:
                label.color=[1,165/255,0]
            if x>=90 and x<=100:
                label.color=[1,0,0]
            prog.value=x
    return ExApp()  
    #ExApp().run()
    
# Start server in background
t1=Thread(target=work, daemon=True)
t1.start()

#t2=Thread(target=create, daemon=True).start()
#############################################
 
frameWidth=640        # CAMERA RESOLUTION
frameHeight =480
brightness = 180
threshold = 0.75         # PROBABLITY THRESHOLD
font = cv2.FONT_HERSHEY_SIMPLEX
##############################################
def detection():
    global z
    global x
    global PD
    global sapp
    global last_execution
    # SETUP THE VIDEO CAMERA
    #phone_ip = "192.168."  # Change this to your phone's IP
    #port = "8080"
    #url = f"http://{phone_ip}:{port}/video"  # For IP Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)
    # IMPORT THE TRANNIED MODEL
    pickle_in=open("C:/Users/Dell/Desktop/for me/SICOM/S4/projet PFA/yolo/model_trained_colab.p","rb")  ## rb = READ BYTE
    model=pickle.load(pickle_in)
    
    def grayscale(img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return img
    def equalize(img):
        img =cv2.equalizeHist(img)
        return img
    def preprocessing(img):
        img = grayscale(img)
        img = equalize(img)
        img = img/255
        return img
    def getCalssName(classNo):
        if   classNo == 0: return 'Limitation de vitesse 20 km/h'#'Speed Limit 20 km/h'
        elif classNo == 1: return 'Limitation de vitesse 30 km/h'#'Speed Limit 30 km/h'
        elif classNo == 2: return 'Limitation de vitesse 50 km/h'#'Speed Limit 50 km/h'
        elif classNo == 3: return 'Limitation de vitesse 60 km/h'#'Speed Limit 60 km/h'
        elif classNo == 4: return 'Limitation de vitesse 70 km/h'#'Speed Limit 70 km/h'
        elif classNo == 5: return 'Limitation de vitesse 80 km/h'#'Speed Limit 80 km/h'
        elif classNo == 6: return 'Limitation de vitesse 80 km/h'#'End of Speed Limit 80 km/h'
        #elif classNo == 7: return 'Speed Limit 100 km/h'
        #elif classNo == 8: return 'Speed Limit 120 km/h'
        #elif classNo == 9: return 'No passing'
        #elif classNo == 10: return 'No passing for vechiles over 3.5 metric tons'
        #elif classNo == 11: return 'Right-of-way at the next intersection'
        #elif classNo == 12: return 'Priority road'
        #elif classNo == 13: return 'Yield'
        elif classNo == 14: return 'Stop'
        #elif classNo == 15: return 'No vechiles'
        #elif classNo == 16: return 'Vechiles over 3.5 metric tons prohibited'
        #elif classNo == 17: return 'No entry'
        #elif classNo == 18: return 'General caution'
        #elif classNo == 19: return 'Dangerous curve to the left'
        elif classNo == 20: return 'Virage dangereux à droite'#'Dangerous curve to the right'
        elif classNo == 21: return 'Double virage'#'Double curve'
        #elif classNo == 22: return 'Bumpy road'
        #elif classNo == 23: return 'Slippery road'
        #elif classNo == 24: return 'Road narrows on the right'
        #elif classNo == 25: return 'Travaux sur la route'#'Road work'
        #elif classNo == 26: return 'Traffic signals'
        #elif classNo == 27: return 'Pedestrians'
        elif classNo == 28: return "Traversée d'enfants"#'Children crossing'
        elif classNo == 29: return 'Traversée de vélos'#'Bicycles crossing'
        elif classNo == 30: return 'Attention verglas/neige'#'Beware of ice/snow'
        elif classNo == 31: return "Traversée d'animaux"#'Wild animals crossing'
        #elif classNo == 32: return 'End of all speed and passing limits'
        #elif classNo == 33: return 'Turn right ahead'
        #elif classNo == 34: return 'Turn left ahead'
        #elif classNo == 35: return 'Ahead only'
        #elif classNo == 36: return 'Go straight or right'
        #elif classNo == 37: return 'Go straight or left'
        #elif classNo == 38: return 'Keep right'
        #elif classNo == 39: return 'Keep left'
        #elif classNo == 40: return 'Roundabout mandatory'
        #elif classNo == 41: return 'End of no passing'
        #elif classNo == 42: return 'End of no passing by vechiles over 3.5 metric tons'
    
    while True:
        current_time = time.time()
        # READ IMAGE
        success, imgOrignal = cap.read()
        # PROCESS IMAGE
        img = np.asarray(imgOrignal)
        img = cv2.resize(img,(32,32))
        img = preprocessing(img)
        cv2.imshow("Processed Image", img)
        img = img.reshape(1, 32, 32, 1)
        cv2.putText(imgOrignal, "CLASS: " , (20, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(imgOrignal, "PROBABILITY: ", (20, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        # PREDICT IMAGE
        '''predictions = model.predict(img)
        classIndex = model.predict_classes(img)
        probabilityValue =np.amax(predictions)'''
        predictions = model.predict(img, verbose=0)
        classIndex = np.argmax(predictions)  # Gets the class index with highest probability
        probabilityValue = np.max(predictions)
        #d={"Stop":0,"Speed Limit 20 km/h":20,"Speed Limit 30 km/h":30,"Speed Limit 50 km/h":50,"Speed Limit 60 km/h":60,"Speed Limit 70 km/h":70,"Speed Limit 80 km/h":80,"Wild animals crossing":50,"Beware of ice/snow":40,"Bicycles crossing":30,"Children crossing":30,"Road work":40,"Double curve":45,"Dangerous curve to the right":50}
        d={"Stop":0,"Limitation de vitesse 20 km/h":20,"Limitation de vitesse 30 km/h":30,"Limitation de vitesse 50 km/h":50,"Limitation de vitesse 60 km/h":60,"Limitation de vitesse 70 km/h":70,"Limitation de vitesse 80 km/h":80,"Traversée d'animaux":50,"Attention verglas/neige":40,"Traversée de vélos":30,"Traversée d'enfants":30,"Travaux sur la route":40,"Double virage":45,"Virage dangereux à droite":50}
        dd={"Stop":0,"Limitation de vitesse 20 km/h":1,"Limitation de vitesse 30 km/h":2,"Limitation de vitesse 50 km/h":3,"Limitation de vitesse 60 km/h":4,"Limitation de vitesse 70 km/h":5,"Limitation de vitesse 80 km/h":6,"Traversée d'animaux":7,"Attention verglas/neige":8,"Traversée de vélos":9,"Traversée d'enfants":10,"Travaux sur la route":11,"Double virage":12,"Virage dangereux à droite":13}
        
        if probabilityValue > threshold:
            
            for i in d:
                
                if getCalssName(classIndex)==i:
                    if y=="alerte" or y=="auto":
                        if current_time - last_execution >= 2:
                            if x>d[i]:
                                z+=1
                                
                            else:
                                z-=1
                                if z<0:
                                    z=0
                            if z>=3 and z<6:
                                    box1.md_bg_color=[255,128/255,0/255,1]
                            if z>6:
                                box1.md_bg_color=[255,0,0]
                            if z<3:
                                box1.md_bg_color=[0,255,0]
                            last_execution = current_time  # Reset timer
                            PD.append([dd[i],x])
                        label2.text="Attention, le panneau de signalisation " + i + " est détecté."
                    if y=="alerte":
                        if x>d[i]:
                            print("alerte")
                            engine = pyttsx3.init()
                            # Get available voices
                            voices = engine.getProperty('voices')
                            # Set speech rate (speed)
                            engine.setProperty('rate', 170)  # Default is around 200 (words per minute)
                            # Set volume (0.0 to 1.0)
                            engine.setProperty('volume', 1.0)  # Default is usually 1.0
                            engine.setProperty('voice', voices[4].id)  # Try different indices
                            #engine.say("Attention, le panneau "+i+" est détecté.")
                            engine.say("Attention, le panneau de signalisation " + i + " est détecté.")
                            #engine.runAndWait()  # Blocks until speech is complete
                            
                            pygame.mixer.init()
                            pygame.mixer.music.load(str(dd[i])+".mp3")
                            pygame.mixer.music.play()
                            time.sleep(2)
                            
                    elif y=="auto":

                        if x>d[i]:
                            pygame.mixer.init()
                            pygame.mixer.music.load("warn.mp3")
                            pygame.mixer.music.play()
                            while x>d[i]:
                                
                                x-=1
                                label.text=str(x)+"Km/h"
                                prog.value=x
                                if x<70:
                                    label.color=[1,1,1]
                                if x>=70 and x<80:
                                    label.color=[1,1,0]
                                if x>=80 and x<90:
                                    label.color=[1,165/255,0]
                                if x>=90 and x<=100:
                                    label.color=[1,0,0]
                                time.sleep(0.1)
                            time.sleep(2)
            #print(getCalssName(classIndex))
            cv2.putText(imgOrignal,str(classIndex)+" "+str(getCalssName(classIndex)), (120, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(imgOrignal, str(round(probabilityValue*100,2) )+"%", (180, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Result", imgOrignal)

        else:
            cv2.putText(imgOrignal,"unknown", (120, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(imgOrignal, "0%", (180, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Result", imgOrignal)  
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
# Start server in background
t1=Thread(target=work, daemon=True).start()
t2=Thread(target=detection, daemon=True).start()
t3=Thread(target=conection, daemon=True).start()
app=create()
app.run()
input("..................")


