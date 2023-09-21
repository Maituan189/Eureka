from statistics import mode
from chuan_convert import convert
from gtts import gTTS
from playsound import playsound
import os
from tkinter import *
import tkinter
from turtle import st
import time
import serial
from threading import Thread
import speech_recognition#.
from threading import Thread#.
from subprocess import call
ai_ear = speech_recognition.Recognizer()  # nghe người dùng nói

vva = Tk()
vva.title("voice virtual assistant- air condition system")
vva.geometry("800x480")  # có thể thay đổi chiều dài rộng
vva.resizable(width=False, height=False)
# thư viện ảnh
def image(tk_):
    global _giongoai_,_giotrong_,ac_on,ac_off,up,down,up1,down1,bi,chan,mat,guong_chan,guong,bi2,chan2,mat2,guong_chan2,guong2,guongon,guongoff,img,create_bt
    _giongoai_ = tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdngoai.png')
    _giotrong_ = tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdtrong.png')
    ac_on= tk_.PhotoImage(file='/home/pi/Desktop/code_project/ACON.PNG')
    ac_off= tk_.PhotoImage(file='/home/pi/Desktop/code_project/ACOFF.PNG')
    up =tk_.PhotoImage(file='/home/pi/Desktop/code_project/up.PNG')
    down =tk_.PhotoImage(file='/home/pi/Desktop/code_project/dow.PNG')
    up1 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/up1.PNG')
    down1 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/down1.PNG')

    bi =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cd_bi.png')
    chan =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdchan.png')
    mat =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdmat.png')
    guong_chan =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdguong_chan.png')
    guong =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdguong.png')

    bi2 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cd_bi2.png')
    chan2 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdchan2.png')
    mat2 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdmat2.png')
    guong_chan2 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdguong_chan2.png')
    guong2 =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdguong2.png')

    guongon =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdguongs2.png')
    guongoff =tk_.PhotoImage(file='/home/pi/Desktop/code_project/cdguongs.png')

    img = tk_.PhotoImage(file='/home/pi/Desktop/code_project/car.png')
    create_bt = tk_.PhotoImage(file='/home/pi/Desktop/code_project/create.png')

def guide(): #1 NỀN GUIDE
    global label,label_signal,label_text
    label = Label(vva, image = img )
    label.place(x=-10, y=-10)
    label_signal = Label(vva, text = "---" )
    label_signal.place(x=150, y=340)
    label_text = Label(vva, text = "---" )
    label_text.place(x=10, y=380)


def serial_c():    
    global label_signal,door,flag_door, engine,temperature_evir,IG, resutl,value_wind,value_temperature,wind_in,value_mode,var_kinsau
    label_signal.config(text="2")
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=1)
    value_wind,value_temperature,wind_in,value_mode,var_kinsau,resutl,x,IG,door=0,25,0,3,0,0,0,0,0
    flag_door=0
    time_door_open=0
    while True:
        elements= [int(value_wind),int(value_temperature),int(wind_in),int(value_mode),int(resutl),int(var_kinsau)]
        data2=bytearray(elements)
        ser.write(data2)
        ser.flush()
        while ser.in_waiting<4:
            pass
        print("input")
        engine=int(ser.readline().decode("utf-8", "ignore"))
        engine=1
        temperature_evir=int(ser.readline().decode("utf-8", "ignore"))
        IG=int(ser.readline().decode("utf-8", "ignore"))
        door=int(ser.readline().decode("utf-8", "ignore"))
        door=1
        label_signal.config(text=str(engine)+"-"+str(temperature_evir)+"-"+str(IG)+"-"+str(door))
        ser.flush()
        condition()
        
            


def config_song_guong(): #6 ADJUSTING CHẾ ĐỘ SƯỞI KÍNH SAU
    global var_kinsau
    if var_kinsau ==0:
        var_kinsau=1
        guongs_.config(image=guongon)
    elif var_kinsau ==1:
        var_kinsau=0
        guongs_.config(image=guongoff)
def suoi_guong(): #6 CHẾ ĐỘ SƯỞI KÍNH SAU
    global var_kinsau,guongs_
    var_kinsau=0 # GƯƠNG OFF
    guongs_=tkinter.Button(vva, image=guongoff,bd=4, command=config_song_guong)
    guongs_.place(x=150+95*5, y=365)
    
def read_temperature(val):#3 READ VALUE THANH ĐIỀU CHỈNH NHIỆT- value ok---value_temperature----
    global value_temperature
    value_temperature=int(val)
    #show_temperature() # tạm
def _scale(vva):#3SCALE THANH ĐIỀU CHỈNH NHIỆT
    global value_temperature,temperature_s
    value_temperature=25
    temperature_s=Scale(vva, activebackground="green",fg="black",highlightbackground= "green",sliderlength= 50,troughcolor="black",width=30, from_=35, to=22, length=400, resolution=1,showvalue=0, orient= VERTICAL , command=read_temperature) #orient = HORIZONTAL
    temperature_s.set(value_temperature)
    temperature_s.pack(side=RIGHT, padx=10,pady=0)
def button_tem(vva):
    global temperature_evir,show_temperature_my,status_tem
    temperature_evir=25
    status_tem=0
    show_temperature_my =tkinter.Button(vva, text=str(temperature_evir)+"E", fg ="red", font =("Arial", 25,'bold'),bd=5,bg='white',command=restart_tem)
    show_temperature_my.place(x=660, y=200)
def restart_tem():
    global status_tem,engine
    if engine==1:
        if status_tem==0:
            status_tem=1
        else:
            status_tem=0
    else:
        response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
def show_temperature():#3 SHOW THANH ĐIỀU CHỈNH NHIỆT
    global value_temperature,temperature_s
    temperature_s.set(int(value_temperature))
    show_temperature_my.config(text=str(value_temperature), fg ="red")
def show_temperature_evi():#3 SHOW THANH ĐIỀU CHỈNH NHIỆT
    global temperature_evir,temperature_s,value_temperature
    temperature_s.set(int(temperature_evir))
    value_temperature=temperature_evir
    show_temperature_my.config(text=str(temperature_evir)+"R", fg ="green")
    
def condition():
    global resutl, status_tem,engine,flag_door,time_door_open,IG
    if IG==0:
        call("sudo shutdown -h now",shell=True)
        #pass
    if engine==1 and status_tem==1:
        resutl=1
        show_temperature()
        fan.pack_forget()
    else:
        resutl=0
        status_tem=0
        show_temperature_evi()
        fan.pack(side=LEFT, padx=35,pady=100)
    if door!= 1 and resutl==1:
        if flag_door==0: # 
            time_door_open=time.time()
            flag_door=1
            print("flag_door=0")
        elif flag_door==1:
            if time.time()-time_door_open>5 & door == 60:
                response_customer("cảnh báo cửa ô tô mở khi điều hòa đang hoạt động")
                time.sleep(0.25)
                response_customer("cửa trước bên trái mở")
                flag_door=0
                time_door_open=time.time()
            elif time.time()-time_door_open>5 & door == 50:
                response_customer("cảnh báo cửa ô tô mở khi điều hòa đang hoạt động")
                time.sleep(0.25)
                response_customer("cửa trước bên trái mở")
                flag_door=0
                time_door_open=time.time()
            elif time.time()-time_door_open>5 & door == 70:
                response_customer("cảnh báo cửa ô tô mở khi điều hòa đang hoạt động")
                time.sleep(0.25)
                response_customer("cả hai cửa trước đều mở")
                flag_door=0
                time_door_open=time.time()
            elif time.time()-time_door_open>5 & door == 76: # HEX=4C -> 76
                response_customer("cảnh báo cửa ô tô mở khi điều hòa đang hoạt động")
                time.sleep(0.25)
                response_customer("cả hai cửa trước đều mở")
                flag_door=0
                time_door_open=time.time()
            elif time.time()-time_door_open>5 & (door == 124 | door == 92) : # HEX=7C,5C -> 124,92
                response_customer("cảnh báo cửa ô tô mở khi điều hòa đang hoạt động")
                time.sleep(0.25)
                response_customer("nhiều cửa đang mở")
                flag_door=0
                time_door_open=time.time()
            else:
                print("flag_door=1")
    else:
        flag_door=0
def config_wind():#4 CONFIG CHỈNH CHẾ ĐỘ GIÓ TRONG GIÓ NGOÀI value ok ---wind_in---
    global wind_in
    if wind_in==0:
        gio_ngoai_ngoai.config(image=_giongoai_)
        wind_in=1
    else:
        gio_ngoai_ngoai.config(image=_giotrong_)
        wind_in=0
def _gio_ngoai_trong(vva):#4 GUIDE CHỈNH CHẾ ĐỘ GIÓ TRONG GIÓ NGOÀI
    global gio_ngoai_ngoai,wind_in
    wind_in=0
    gio_ngoai_ngoai = tkinter.Button(vva,image=_giotrong_,fg ="red", font =("Arial", 18,'bold'),bd=4,bg='aqua',command=config_wind)
    gio_ngoai_ngoai.place(x=10, y=400)
def gio_ngoai():
    global wind_in
    wind_in=1
    gio_ngoai_ngoai.config(image=_giongoai_)
def gio_trong():
    global wind_in
    wind_in=0
    gio_ngoai_ngoai.config(image=_giotrong_)


def mode_():#5 CÁC CHẾ ĐỘ HƯỚNG GIÓ value ok ---value_mode---
    global bi_2,chan_,mat_,guong_chan_,guong_,value_mode
    value_mode=3
    bi_2 = tkinter.Button(vva, image=bi,bd=4, command=lambda:config_mode_("1"))
    chan_=tkinter.Button(vva, image=chan,bd=4, command=lambda:config_mode_("2"))
    mat_=tkinter.Button(vva, image=mat2,bd=4, command=lambda:config_mode_("3"))
    guong_chan_=tkinter.Button(vva, image=guong_chan,bd=4, command=lambda:config_mode_("4"))
    guong_=tkinter.Button(vva, image=guong,bd=4, command=lambda:config_mode_("5"))
    bi_2.place(x=150, y=365)
    chan_.place(x=150+95, y=365)
    mat_.place(x=150+95*2, y=365)
    guong_chan_.place(x=150+95*3, y=365)
    guong_.place(x=150+95*4, y=365)
def config_mode_(signal):#5 ADJUST CÁC CHẾ ĐỘ HƯỚNG GIÓ
    global var_bi, var_guong, var_mat, var_changuong, var_chan,bi_2,chan_,mat_, guong_chan_,guong_,value_mode
    if signal=="1":
        value_mode=1
        var_bi,var_chan,var_mat,var_changuong,var_guong, = 1,0,0,0,0
        bi_2.config(image=bi2)
        chan_.config(image=chan)
        mat_.config( image=mat)
        guong_chan_.config(image=guong_chan)
        guong_.config( image=guong)
    elif signal=="2": # 
        value_mode=2
        var_bi,var_chan,var_mat,var_changuong,var_guong = 0,1,0,0,0
        bi_2.config(image=bi)
        chan_.config(image=chan2)
        mat_.config(image=mat)
        guong_chan_.config(image=guong_chan)
        guong_.config(image=guong)
    elif signal=="3": # 
        value_mode=3
        var_bi,var_chan,var_mat,var_changuong,var_guong = 0,0,1,0,0
        bi_2.config(image=bi)
        chan_.config(image=chan)
        mat_.config(image=mat2)
        guong_chan_.config( image=guong_chan)
        guong_.config(image=guong)
    elif signal=="4": # 
        value_mode=4
        var_bi,var_chan,var_mat,var_changuong,var_guong, = 0,0,0,1,0
        bi_2.config(image=bi)
        chan_.config(image=chan)
        mat_.config(image=mat)
        guong_chan_.config(image=guong_chan2)
        guong_.config(image=guong)
    elif signal=="5": # 
        value_mode=5
        var_bi,var_chan,var_mat,var_changuong,var_guong = 0,0,0,0,1
        if wind_in==0:
            gio_ngoai()
        bi_2.config(image=bi)
        chan_.config(image=chan,bd=4)
        mat_.config(image=mat,bd=4)
        guong_chan_.config(image=guong_chan)
        guong_.config(image=guong2)
    elif value_mode==1: # 
        value_mode=1
        var_bi,var_chan,var_mat,var_changuong,var_guong, = 1,0,0,0,0
        bi_2.config(image=bi2)
        chan_.config(image=chan)
        mat_.config( image=mat)
        guong_chan_.config(image=guong_chan)
        guong_.config( image=guong)
    elif value_mode==2: # 
        value_mode=2
        var_bi,var_chan,var_mat,var_changuong,var_guong = 0,1,0,0,0
        bi_2.config(image=bi)
        chan_.config(image=chan2)
        mat_.config(image=mat)
        guong_chan_.config(image=guong_chan)
        guong_.config(image=guong)
    elif  value_mode==3: # 
        value_mode=3
        var_bi,var_chan,var_mat,var_changuong,var_guong = 0,0,1,0,0
        bi_2.config(image=bi)
        chan_.config(image=chan)
        mat_.config(image=mat2)
        guong_chan_.config( image=guong_chan)
        guong_.config(image=guong)
    elif value_mode==4: # 
        value_mode=4
        var_bi,var_chan,var_mat,var_changuong,var_guong, = 0,0,0,1,0
        bi_2.config(image=bi)
        chan_.config(image=chan)
        mat_.config(image=mat)
        guong_chan_.config(image=guong_chan2)
        guong_.config(image=guong)
    elif value_mode==5: # 
        value_mode=5
        var_bi,var_chan,var_mat,var_changuong,var_guong = 0,0,0,0,1
        bi_2.config(image=bi)
        chan_.config(image=chan,bd=4)
        mat_.config(image=mat,bd=4)
        guong_chan_.config(image=guong_chan)
        guong_.config(image=guong2)
    else:
        print("error config_mode_")


def value_wind_(val):  #2 READ THANH ĐIỀU CHỈNH GIÓ- ok biến--- value_wind---
    global value_wind,status_tem
    value_wind = int(val)
    config_fan(int(val))
def wind_adj(vva):#2 GUIDE THANH ĐIỀU CHỈNH GIÓ
    global level_wind_7,value_wind, fan
    value_wind=0
    fan=Scale(vva, activebackground="green",fg="black",highlightbackground= "magenta",sliderlength= 50,troughcolor="black",width=30, from_=10, to=0, length=250, resolution=1,showvalue=0, orient= VERTICAL , command=value_wind_) #orient = HORIZONTAL
    fan.place(x=35,y=135)
    fan.set(0)
    level_wind_7 =tkinter.Label(vva, text=str(value_wind), fg ="red", font =("Arial", 30,'bold'),bd=10,background='#180A0A')
    level_wind_7.place(x=30, y=65)
    
def config_fan(signal_fan):#2 CONFIG THANH ĐIỀU CHỈNH GIÓ
    fan.set(int(signal_fan))
    level_wind_7.config(text=str(signal_fan))

def create_setup():
    global tem1_mode,tem1_temperature, tem1_wind,tem2_mode,tem2_temperature, tem2_wind,tem3_mode,tem3_temperature, tem3_wind
    if value_remember !=0 and value_wind!=0 and value_mode!=5:
        if value_remember==1:
            tem1_mode=value_mode
            tem1_temperature=value_temperature
            tem1_wind=value_wind
        elif value_remember==2:
            tem2_mode=value_mode
            tem2_temperature=value_temperature
            tem2_wind=value_wind
        elif value_remember==3:
            tem3_mode=value_mode
            tem3_temperature=value_temperature
            tem3_wind=value_wind
        else:
            print("error create_setup(0)")
        write_file_remember()
    else:
        print("error create_setup(1)")
def create_setup_virtual(value):
    global tem1_mode,tem1_temperature, tem1_wind,tem2_mode,tem2_temperature, tem2_wind,tem3_mode,tem3_temperature, tem3_wind
    if value_mode!=5:
        if value==1:
            tem1_mode=value_mode
            tem1_temperature=value_temperature
            tem1_wind=value_wind
        elif value==2:
            tem2_mode=value_mode
            tem2_temperature=value_temperature
            tem2_wind=value_wind
        elif value==3:
            tem3_mode=value_mode
            tem3_temperature=value_temperature
            tem3_wind=value_wind
        else:
            print("error create_setup_virtual(1)")
        write_file_remember()
    else:
        print("error create_setup_virtual(2)")
def read_remember(val): # trước khi lưu thì phải đảm bảo điều kiện đủ để sử dụng điều hòa
    global value_remember
    value_remember=int(val)
    consider_remember(value_remember)
def consider_remember(value_re_):
    global status_tem,engine,value_remember,show_remember,tem1_mode,tem1_temperature, tem1_wind,tem2_mode,tem2_temperature, tem2_wind,tem3_mode,tem3_temperature, tem3_wind,value_mode,value_temperature,value_wind, engine,remember_
    
    if engine==1:
        show_remember.config(text='VỊ TRÍ ĐIỀU HÒA '+str(value_re_))
        remember_.set(value_re_)
        if value_re_==1:
            value_mode=tem1_mode
            value_temperature=tem1_temperature
            value_wind=tem1_wind
            status_tem=1
            config_mode_(value_mode)
            config_fan(value_wind)
            show_temperature()
            
        elif value_re_==2:
            value_mode=tem2_mode
            value_temperature=tem2_temperature
            value_wind=tem2_wind
            status_tem=1
            config_mode_(value_mode)
            config_fan(value_wind)
            show_temperature()
            
        elif value_re_==3:
            value_mode=tem3_mode
            value_temperature=tem3_temperature
            value_wind=tem3_wind
            status_tem=1
            config_mode_(value_mode)
            config_fan(value_wind)
            show_temperature()
    else:
        show_remember.config(text='VỊ TRÍ ĐIỀU HÒA'+str(0))
        remember_.set(0)
    
    print("consider_remember():"+str(value_mode)+str(value_temperature)+str(value_wind))
def remember():
    global remember_, value_remember,show_remember, tem1_mode,tem1_temperature, tem1_wind,tem2_mode,tem2_temperature, tem2_wind,tem3_mode,tem3_temperature, tem3_wind
    value_remember=0
    remember_=25
    remember_=Scale(vva, activebackground="green",fg="black",highlightbackground= "green",sliderlength= 50,troughcolor="black",width=30, from_=0, to=3, length=200, resolution=1,showvalue=0, orient= HORIZONTAL , command=read_remember) #orient = HORIZONTAL
    remember_.set(0)
    remember_.place(x=350, y=300)
    show_remember=tkinter.Label(vva, text='VỊ TRÍ ĐIỀU HÒA '+str(value_remember), fg ="black", font =("Times New Roman ", 24,'bold'),bd=5,bg='white')
    show_remember.place(x=250, y=240)
    create_ = tkinter.Button(vva,image=create_bt,fg ="black",bd=4,bg='red',command=create_setup)
    create_.place(x=250, y=285)
def write_file_remember():
    global tem1_mode,tem1_temperature, tem1_wind,tem2_mode,tem2_temperature, tem2_wind,tem3_mode,tem3_temperature, tem3_wind
    add=[str(tem1_mode),str(tem1_wind),str(tem1_temperature)]
    add2=[str(tem2_mode),str(tem2_wind),str(tem2_temperature)]
    add3=[str(tem3_mode),str(tem3_wind),str(tem3_temperature)]
    open_file=open("/home/pi/Desktop/project/file.txt",mode= 'w')
    data_=open_file.writelines(add)
    data_=open_file.write("\n")
    data_=open_file.writelines(add2)
    data_=open_file.write("\n")
    data_=open_file.writelines(add3)
    open_file.close()
    open_file=open("/home/pi/Desktop/project/file.txt",mode= 'r')
    data_=open_file.readline()
    data_=open_file.readline()
    data_=open_file.readline()
    open_file.close()
def read_file_remember():
    global tem1_mode,tem1_temperature, tem1_wind,tem2_mode,tem2_temperature, tem2_wind,tem3_mode,tem3_temperature, tem3_wind
    open_file=open("/home/pi/Desktop/project/file.txt",mode= 'r')
    data_=open_file.readline()
    tem1_mode=data_[0]
    tem1_wind=data_[1]
    tem1_temperature=data_[2:4]
    data_=open_file.readline()
    tem2_mode=data_[0]
    tem2_wind=data_[1]
    tem2_temperature=data_[2:4]
    data_=open_file.readline()
    tem3_mode=data_[0]
    tem3_wind=data_[1]
    tem3_temperature=data_[2:4]
    open_file.close()
    
def response_customer(x):
    convert.play_audio(x)
def process(code):
    global engine,value_temperature,status_tem,value_wind,value_remember,value_mode,wind_in
    code_last = code.split()
    p = [int(n) for n in code.split() if n.isdigit()]
    if len(p) > 0:  # //////////////////////////////////////////////xử lý res có số X
        set_point = int(p[0])
        print(code_last[0] )
        if code_last[0] == "it": # UP TEMPERATURE TO LEVEL
            if set_point > value_temperature and set_point < 36: # condition sub
                if engine == 1:# value_temperature condition main
                    if status_tem==0: # tức resutl=0 và quạt đang hoạt động
                        restart_tem()
                    value_temperature=set_point
                    response_customer("nhiệt độ sẽ tăng lên "+str(value_temperature)) # đủ điều khiện tăng nhiệt độ lên mong muốn
                else:
                    response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa") # động cơ chưa nổ
            elif set_point > 35 or set_point < 22:
                response_customer("ngoài phạm vi điều chỉnh nhiệt độ từ 22 đến 35 độ")
            elif set_point < value_temperature:
                response_customer("nhiệt độ hiện tại là "+ str(value_temperature) + " đang cao hơn yêu cầu là "+str(set_point))
            else:
                print("error it")
        elif code_last[0] == "dt":
            if set_point < value_temperature and set_point > 21:
                if engine == 1:
                    if status_tem == 0: # quạt đang hoạt động
                        restart_tem()
                    value_temperature = set_point
                    response_customer("nhiệt độ sẽ giảm xuống "+str(value_temperature)) # đủ điều khiện tăng nhiệt độ lên mong muốn
                else:
                    response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa") # động cơ chưa nổ
            elif set_point > 35 or set_point <22:
                response_customer("ngoài phạm vi điều chỉnh nhiệt độ từ 22 đến 35")
            elif set_point > value_temperature:
                response_customer("nhiệt độ hiện tại là "+ str(value_temperature) + " đã thấp hơn yêu cầu là "+str(set_point) )
            else:
                print("error dt")
        elif code_last[0]=="dtx" or  code_last[0]=="ont":
            if set_point > 21 and set_point < 36:
                if engine == 1:
                    if status_tem == 0: # or resutl
                        restart_tem()
                    value_temperature = set_point
                    response_customer("nhiệt độ sẽ điều chỉnh nhiệt độ đến "+str(value_temperature)) # đủ điều khiện tăng nhiệt độ lên mong muốn
                else:
                    response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
            else:
                response_customer("ngoài phạm vi điều chỉnh nhiệt độ từ 22 đến 35")
        elif code_last[0]=="iw":#/////////////////////////////////////////////////////////////////// CONSIDER FAN
            if set_point>value_wind and set_point<11: # setpoint lớn hơn gió hiện tại và nhỏ hơn max
                if resutl == 1: # đang chỉnh nhiệt(engine=1; status_tem=1)
                    restart_tem()
                value_wind = set_point # change value fan
                config_fan(value_wind) # config show  fan
                response_customer("quạt gió sẽ tăng lên "+str(value_wind))
            elif set_point>10 or set_point<0:
                response_customer("ngoài phạm vi điều chỉnh quạt từ 1 đến 10")
            elif set_point < value_wind:
                response_customer("quạt hiện tại là "+str(value_wind)+" đang cao hơn quạt yêu cầu là "+str(set_point))
            else:
                print("error iw")
        elif code_last[0]=="dw":#/////////////////////////////////////////////////////////////////// CONSIDER FAN
            if set_point<value_wind and set_point>=0: # setpoint lớn hơn gió hiện tại và nhỏ hơn max
                if resutl==1: # đang chỉnh nhiệt
                    restart_tem()
                value_wind=set_point # change value level fan
                config_fan(value_wind) # change show fan
                response_customer("quạt gió sẽ giảm xuống "+str(value_wind))
            elif set_point>10 or set_point<0:
                response_customer("ngoài phạm vi điều chỉnh quạt từ 1 đến 10")
            elif set_point > value_wind:
                response_customer("quạt hiện tại là "+str(value_wind)+" đang thấp hơn quạt yêu cầu là "+str(set_point))
            else:
                print(" error dw")
        elif code_last[0]=="dwxx":#/////////////////////////////////////////////////////////////////// CONSIDER FAN
            if set_point < 11 and set_point > 0: # setpoint lớn hơn gió hiện tại và nhỏ hơn max
                if resutl==1: # đang chỉnh nhiệt
                    restart_tem()
                value_wind=set_point # change value fan
                config_fan(value_wind) # change show fan
                response_customer(" quạt gió sẽ điều chỉnh về "+str(value_wind))
            elif set_point>10 or set_point<0:
                response_customer("ngoài phạm vi điều chỉnh quạt từ 1 đến 10")
            else:
                print("error dwxx")
        elif code_last[0]=="rr":
            if engine==0:
                response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
            elif set_point == value_remember:
                response_customer("vị trí điều hòa hiện tại đã ở "+str(set_point))
            elif set_point>3 or set_point<0:
                response_customer("vị trí điều hòa yêu cầu nằm ngoài phạm vi từ 1 đến 3")
            else:
                response_customer("hệ thống điều hòa sẽ đưa đến vị trí "+str(set_point))
                value_remember=set_point
                consider_remember(set_point)
        elif code_last[0]=="wr":
            if set_point>0 and set_point < 4:
                response_customer("trạng thái điều hòa sẽ lưu vào vị trí "+str(set_point))
                create_setup_virtual(set_point)
            else:
                response_customer("vị trí nhớ yêu cầu nằm ngoài phạm vi, phạm vi chỉ có thể từ 1 đến 3")
        elif code_last[0]=="c":
            for i in range(6):
                if set_point == i:
                    response_customer("vị trí hướng gió sẽ được điều chỉnh")
                    value_mode=set_point
                    config_mode_(str(set_point))
        else:
            print("error have number response")

    else: #//////////////////////////////////////////////////////////////KHÔNG SỐ
        if code_last[0] == "it":
            if engine==1:
                if status_tem == 0:
                        restart_tem()
                if value_temperature < 34:
                    value_temperature = value_temperature+2
                    response_customer("nhiệt độ sẽ tăng lên "+str(value_temperature)) 
                elif value_temperature == 34:
                    value_temperature = 35
                    response_customer("nhiệt độ sẽ tăng lên "+str(35))
                elif value_temperature == 35:
                    response_customer("nhiệt độ hiện tại đã lớn nhất")
                else:
                    print("error it response")
            else:
                response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
        elif code_last[0] == "dt":
            if engine == 1:
                if status_tem == 0:
                        restart_tem()
                if value_temperature > 23:
                    value_temperature = value_temperature-2
                    response_customer("nhiệt độ sẽ giảm xuống "+str(value_temperature))
                elif value_temperature == 23:
                    value_temperature = 22
                    response_customer("nhiệt độ sẽ giảm xuống "+str(22))
                elif value_temperature == 22:
                    response_customer("nhiệt độ hiện tại đã thấp nhất")
                else:
                    print("error dt response")
            else:
                response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
        elif code_last[0] == "dt1":
            if engine == 1:
                if status_tem==0:
                    restart_tem()
                value_temperature = 25
                response_customer("nhiệt độ sẽ đưa về 25 độ")
            else:
                response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
        elif code_last[0] == "it1":
            if engine == 1:
                if status_tem==0:
                    restart_tem()
                value_temperature = 35
                response_customer("nhiệt độ sẽ đưa lên 35 độ")
            else:
                response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
        elif code_last[0] == "ont":
            if engine==1:
                if resutl==0:
                    restart_tem()
                    value_temperature = 25
                    response_customer("điều hòa sẽ mở và đưa nhiệt độ đến 25 độ")
                else:
                    response_customer("điều hòa đang mở")
            else:
                response_customer("động cơ chưa được khởi động nên không thể sử dụng các chế độ điều hòa")
        elif code_last[0] == "dtx":
            response_customer("tôi cần biết bạn yêu cầu bao nhiêu độ")
        elif code_last[0] == "oft":
            if resutl == 0:
                response_customer("điều hòa đã tắt")
            else:
                response_customer("điều hòa sẽ được tắt ")
                restart_tem()
                show_remember.config(text='VỊ TRÍ NHỚ '+str(0))
                remember_.set(0)
        elif code_last[0]=="iw" or code_last[0]=="iwx":#/////////////////////////////////////////////////////////////////// CONSIDER FAN
            if resutl==1: # đang chỉnh nhiệt
                restart_tem()
            if value_wind<9:
                value_wind=value_wind+2
                config_fan(value_wind) # config show
                response_customer("gió sẽ được tăng gió lên "+str(value_wind))
            elif value_wind==9:
                value_wind=10
                config_fan(value_wind) # config show
                response_customer("gió sẽ được tăng gió lên cấp 10 ")
            else:
                response_customer("gió đã tối đa không thể tăng")
        elif code_last[0]=="dw"or code_last[0]=="dwx":#/////////////////////////////////////////////////////////////////// CONSIDER FAN
            if resutl==1: # đang chỉnh nhiệt
                restart_tem() 
            if value_wind>2:
                value_wind=value_wind-2
                config_fan(value_wind) # config show
                response_customer("gió sẽ được giảm xuống "+str(value_wind))
            elif value_wind==2:
                value_wind=1
                config_fan(value_wind) # config show
                response_customer("gió sẽ được giảm xuống cấp 1")
            else:
                response_customer("gió đã nhỏ nhất không thể giảm")
        elif code_last[0]=="ofw": #////////////////KHI TẮT QUẠT ĐỒNG THỜI TẮT CHỈNH NHIỆT
            if resutl==1:
                restart_tem() # off the air conditioner
                value_wind=0 # set value fan comeback 0
                config_fan(value_wind) # config show fan
                response_customer("điều hòa đang được bật và tôi sẽ tắt quạt lẫn điều hòa")
            elif value_wind==0:
                response_customer("quạt đã tắt")
            else:
                value_wind=0
                config_fan(value_wind)
                response_customer("quạt sẽ được tắt")
        elif code_last[0]=="onw":# 
            if resutl ==1:
                response_customer("điều hòa đang hoạt động và quạt đã hoạt động")
            elif value_wind!=0: # NẾU QUẠT ĐÃ ON THÌ BÁO
                response_customer("quạt đã được bật")
            else: # NẾU QUẠT CHƯA ON THÌ NGHĨA ĐIỀU HÒA CHƯA HĐ
                response_customer("quạt sẽ được mở ở cấp 2")
                value_wind=2
                config_fan(value_wind)
        elif code_last[0]=="wr":
            if value_remember==0:
                response_customer("vui lòng chuyển đến vị trí mà bạn muốn lưu vào")
            else:
                response_customer("trạng thái này sẽ lưu vào vị trí "+str(value_remember))
                create_setup()
        elif code_last[0]=="windi":
            if wind_in==0:
                response_customer("hệ thống hiện tại đang sử dụng gió tuần hoàn")
            else:
                response_customer("hệ thống sẽ sử dụng gió tuần hoàn")
                config_wind()
        elif code_last[0]=="windo":
            if wind_in==1:
                response_customer("hệ thống hiện tại đang sử dụng gió môi trường")
            else:
                response_customer("hệ thống sẽ sử dụng gió môi trường")
                config_wind()
        elif code_last[0]=="rr":
            response_customer("tôi chưa hiểu bạn muốn mở vị trí đã nhớ là bao nhiêu")
        else:
            print("error haven't none P[0]")
def voice():
    global label_text
    
    while True:
        with speech_recognition.Microphone() as mic:
            label_text.config(text="listen")
            audio= ai_ear.adjust_for_ambient_noise(mic,duration=1)
            audio = ai_ear.record(mic, duration=3)
            #audio = ai_ear.listen(mic,None)
            label_text.config(text="process")
        try:
            you = ai_ear.recognize_google(audio, language='vi-VN')
            print(you)
            you1=you.lower().split()
            x="trợ lý"
            xx="trợ lí"
            if set(x.split()).issubset(you1) or set(xx.split()).issubset(you1):
                with speech_recognition.Microphone() as mic:
                    label_text.config(text="listen--")
                    audio= ai_ear.adjust_for_ambient_noise(mic,duration=0.5)
                    convert.play_audio_available("/home/pi/Desktop/project/say_yes.mp3")
                    audio = ai_ear.record(mic, duration=4)  # sau 5s tự đóng mic
                     #audio = ai_ear.listen(mic,None)
                    label_text.config(text="process--")
                try:
                    you = ai_ear.recognize_google(audio, language='vi-VN')
                    print(you)
                    process(convert.convert_(you))
                except:
                    pass
            else:
                convert.play_audio_available("/home/pi/Desktop/project/say_no.mp3")
        except:
            convert.play_audio_available("/home/pi/Desktop/project/say_no.mp3")
            

image(tkinter)
guide()
_scale(vva)
button_tem(vva)
show_temperature()
show_temperature_evi()
suoi_guong()
_gio_ngoai_trong(vva)
mode_()
wind_adj(vva)
remember()
read_file_remember()
label_signal.config(text="1")
thread1 = Thread(target=serial_c)
thread2 = Thread(target=voice)
thread1.start()
thread2.start()
vva.mainloop()

