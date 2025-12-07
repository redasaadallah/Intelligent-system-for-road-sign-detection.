from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from splash import*
from first import*
from home import*
from login import*
from mode import*
from respect import*
from info import*
from contact import*
from why import*
from resume import*
from kivy.clock import Clock
from kivy.core.window import Window
from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
import random
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
Window.size=(350,600);Window.resizable = False
s=socket(AF_INET,SOCK_STREAM)
class MainApp(MDApp):
    def build(self):
        
        self.screen_manager = ScreenManager()
        # Load the kv file
        Builder.load_file('splash.kv')
        Builder.load_file('first.kv')
        Builder.load_file('home.kv')
        Builder.load_file('login.kv')
        Builder.load_file('mode.kv')
        Builder.load_file('respect.kv')
        Builder.load_file('info.kv')
        Builder.load_file('contact.kv')
        Builder.load_file('why.kv')
        Builder.load_file('resume.kv')
        # Add the SplashScreen to the screen manager
        self.screen_manager.add_widget(Splash(name='splash'))
        self.screen_manager.add_widget(First(name='first'))
        self.screen_manager.add_widget(Home(name='home'))
        self.screen_manager.add_widget(Login(name='login'))
        self.screen_manager.add_widget(Mode(name='mode'))
        self.screen_manager.add_widget(Respect(name='respect'))
        self.screen_manager.add_widget(Info(name='info'))
        self.screen_manager.add_widget(Contact(name='contact'))
        self.screen_manager.add_widget(Why(name='why'))
        self.screen_manager.add_widget(Resume(name='resume'))
        Thread(target=self.connect_to_server, daemon=True).start()
        return self.screen_manager
    def connect_to_server(self):
        s.connect(("127.0.0.1",12345))#le IP de server here localhost
        if s.recv(1024).decode() == "NICK":
            s.send("client2".encode())
    def on_start(self):
        Clock.schedule_once(self.change_screen,6)
        
    def change_screen(self,dt):
        self.screen_manager.current="first"
    def auto(self):
        sind_data="auto"
        sind_data=sind_data.encode("utf-8")
        s.send(sind_data)
    def alerte(self):
        sind_data="alerte"
        sind_data=sind_data.encode("utf-8")
        s.send(sind_data)
    
    def connecter(self):
        self.screen_manager.current="home"
        sind_data="wellcome"
        sind_data=sind_data.encode("utf-8")
        s.send(sind_data)
        

    def misejour(self):
        
        d=[[0,0],[1,20],[2,30],[3,50],[4,60],[5,70],[6,80],[7,50],[8,40],[9,30],[10,30],[11,40],[12,45],[13,50]]
        dd={"Stop":0,"Limitation de vitesse 20 km/h":1,"Limitation de vitesse 30 km/h":2,"Limitation de vitesse 50 km/h":3,"Limitation de vitesse 60 km/h":4,"Limitation de vitesse 70 km/h":5,"Limitation de vitesse 80 km/h":6,"Traversée d'animaux":7,"Attention verglas/neige":8,"Traversée de vélos":9,"Traversée d'enfants":10,"Travaux sur la route":11,"Double virage":12,"Virage dangereux à droite":13}
        sind_data="1"
        sind_data=sind_data.encode("utf-8")
        s.send(sind_data)
        PD =json.loads(s.recv(1024).decode())
        print(PD)
        global m
        m=0
        global n
        n=0
        global gr
        gr=MDGridLayout(cols=1,
            pos_hint={'center_x':0.15,'center_y':3.3},
            size_hint=[None,None],
            spacing=5)
        if len(PD)==0:
            pass
        else:
            res=self.screen_manager.get_screen("respect")
            con=res.ids.con
            #np=res.ids.NP
            #con.remove_widget(np)
            pad=res.ids.pad
            pr=res.ids.PR
            pnr=res.ids.PNR
            con.add_widget(gr)
            l1=res.ids.l1
            l2=res.ids.l2
            x=-1000
            y=0.5
            a=3
            b=2.87
            print(PD)
            for i in range(0,len(PD)):
                for j in range(0,len(d)):
                    if d[j][0]==PD[i][0]:
                        mem=d[j]
                if PD[i][1]>mem[1]:
                    resp="roadsign/yet2.png"
                    n+=1
                else:
                    m+=1
                    resp="roadsign/done3.png"
                pnr.text="Panneaux non respectés : "+str(n)
                pr.text="Panneaux respectés : "+str(m)
                scr=MDScreen(name=f"screen{i}")
                scr.add_widget(Image(source='roadsign/'+str(PD[i][0])+'.png',
                                    size_hint_y=0.7,
                                    pos_hint={'center_x':0.2,'center_y':0.5}))
                scr.add_widget(MDLabel(text="Vitesse détectée : "+str(PD[i][1])+" km/h",
                                    theme_text_color='Custom',
                                    text_color=[1,1,1,1],
                                    pos_hint={'center_x':0.9,'center_y':0.8},
                                    bold=True,
                                    font_style='Label'))
                scr.add_widget(MDLabel(text="Vitesse limitée : "+str(mem[1])+" km/h",
                                    theme_text_color='Custom',
                                    text_color=[1,1,1,1],
                                    pos_hint={'center_x':0.9,'center_y':0.55},
                                    bold=True,
                                    font_style='Label'))
                scr.add_widget(MDLabel(text="Respect :",
                                    theme_text_color='Custom',
                                    text_color=[1,1,1,1],
                                    pos_hint={'center_x':1.1,'center_y':0.25},
                                    bold=True,
                                    font_style='Title',
                                    role="medium"))
                scr.add_widget(Image(source=resp,
                                    size_hint_y=0.3,
                                    pos_hint={'center_x':0.9,'center_y':0.25}))
                x+=200
                if len(PD)==1:
                    a-=0.15
                    b-=0.15
                else:
                    a-=0.5
                    b-=0.5
                l1.pos_hint={'center_x':0.5,'center_y':a}
                l2.pos_hint={'center_x':0.5,'center_y':b}
                box=MDBoxLayout(id="reda",md_bg_color=[255,153/255,51/255],
                            size_hint=[None,None],radius=20,height=150,width=400)
                box.add_widget(scr)
                gr.add_widget(box)
                pad.padding=[0,1300,0,x]
    def deconnecter(self):
        global m
        global n
        gr.clear_widgets()
        sind_data="off"
        sind_data=sind_data.encode("utf-8")
        s.send(sind_data)
        self.screen_manager.current = 'login'
        self.screen_manager.transition.direction = 'left'
        sender_email = "redasaadallah77@gmail.com"
        receiver_email = "reda.saadallah@usmba.ac.ma"
        subject = "Statistiques sur le respect des panneaux de signalisation"
        if m<6 and n<6:
            msg="aucun resultat."
        else:
            if m>n:
                msg="Bravo ! Votre respect des panneaux fait de vous un exemple sur la route. Continuez comme ça, vous inspirez les autres !\n\nLe saviez-vous ? En respectant les limitations, vous économisez jusqu’à 20% de carburant et réduisez l’usure de votre véhicule. Bonne conduite = économies !\n\n\n\nNombre de panneaux respectés : "+str(m)+"\n\nNombre de panneaux non respectés : "+str(n)+"\n\nLe taux de respect est donc : "+str(round(m/(m+n)*100))+"%."
            else:
                msg="Attention ! Vous venez de franchir un feu rouge. Voici pourquoi c’est dangereux :\n\nRisque de collision latérale (75% des accidents graves en ville).\n\nAmende de 800 MAD + retrait de points.\n\n\n\nNombre de panneaux respectés : "+str(m)+"\n\nNombre de panneaux non respectés : "+str(n)+"\n\nLe taux de respect est donc : "+str(round(m/(m+n)*100))+"%."
        # Create a multipart message object
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(msg, "plain"))  # Fixed: Use attach() for body content
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        username = "redasaadallah77@gmail.com"
        password = "dcum ptii xbsp pfyt"

        # Create an SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start a secure TLS connection
            server.starttls()
            
            # Login to the email account
            server.login(username, password)
            
            # Convert the message to a string and send the email
            server.send_message(message)
    def static(self):

        global m
        global n
        print(m,n)
        self.screen_manager.current = 'resume'
        self.screen_manager.transition.direction = 'left'
        res=self.screen_manager.get_screen("resume")
        con=res.ids.cn
        npn=res.ids.npn
        msg=res.ids.msg
        if m<6 and n<6:
            msg.text="aucun resultat."
            npn.text=""
        else:
            if m>n:
                msg.text="Bravo ! Votre respect des panneaux fait de vous un exemple sur la route. Continuez comme ça, vous inspirez les autres !\n\nLe saviez-vous ? En respectant les limitations, vous économisez jusqu’à 20% de carburant et réduisez l’usure de votre véhicule. Bonne conduite = économies !"
                npn.text="Nombre de panneaux respectés : "+str(m)+"\n\nNombre de panneaux non respectés : "+str(n)+"\n\nLe taux de respect est donc : "+str(round(m/(m+n)*100))+"%."
            else:
                msg.text="Attention ! Vous venez de franchir un feu rouge. Voici pourquoi c’est dangereux :\n\nRisque de collision latérale (75% des accidents graves en ville).\n\nAmende de 800 MAD + retrait de points."
                npn.text="Nombre de panneaux respectés : "+str(m)+"\n\nNombre de panneaux non respectés : "+str(n)+"\n\nLe taux de respect est donc : "+str(round(m/(m+n)*100))+"%."
if __name__ == "__main__":
    MainApp().run()
