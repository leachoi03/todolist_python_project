import tkinter as tk
from tkinter import *
from tkinter.ttk import *   # Notebook 모듈
import tkinter.messagebox
import customtkinter
import time
import datetime
import calendar
import csv
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
from tkcalendar import *
from curses import window
from datetime import timedelta #오늘 날짜 이전 날짜 구할때 사용
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import platform
try:
        import winsound
        type='windows'
except:
        import os
        type='other'


window = tk.Tk()
window.title("Well-To-Do List")
window.geometry('500x720')

df_task = pd.read_csv("todolist.csv",encoding='cp949')
df_done = pd.read_csv("todolist_done.csv",encoding='cp949')
now = datetime.datetime.now()
today = now.date()

task_list= []
done_list = []


#시계
def clock():        # 현재 시간 표시 / 반복
   live_T = time.strftime("%H:%M:%S")                   # Real Time
   clock_width.config(text=live_T)
   clock_width.after(200, clock)                        # .after(지연시간{ms}, 실행함수)


#스톱워치
def startTimer():   #타이머 시작
    if running:
        global timer                                    # timer = 시간
        timer+=1                                        # 시간이 1씩 증가
        sec=timer//100%60                               #   초
        minu=timer//100//60                             #   분
        dec=timer%100                                   #   시
        time=str(minu).zfill(2)+":"+str(sec).zfill(2) 
                                                        # 시간의 빈칸을 0으로 채움 => 초기 세팅
        timeText.configure(text=time)                   # 시간 출력
    window.after(10, startTimer)                        # 특정 시간마다 startTimer 함수 호출 (재귀)

def start():        # 시작
    global running
    running=True

def stop():         # 중지
    global running
    running=False

def initial():      # 초기화
    global running
    running = False
    global timer
    timer = 0
    timeText.configure(text= "00:00")
    

#할 일 추가        
def addTask():
    task = task_entry.get()
    task_entry.delete(0, END)

    if task:
        df_task.loc[len(df_task)]=[task,today.strftime("%Y-%m-%d")]
        df_task.to_csv("todolist.csv", mode='w',encoding='euc-kr',index=False)       
        task_list.append(task)
        listbox1.insert( END, task)
        get_chart()
       

#할 일 완료        
def doneTask():
    global task_list
    task =str(listbox1.get(ANCHOR))
    if task in task_list:
        task_list.remove(task)
                
        df_done.loc[len(df_done)]=[task,today.strftime("%Y-%m-%d")]
        df_done.to_csv("todolist_done.csv", mode='w',encoding='euc-kr',index=False)  
        done_list.append(task)
        
        idx = df_task[(df_task["날짜"]==today.strftime("%Y-%m-%d"))&(df_task['일정']==task)].index
        df_task.drop(idx, axis=0,inplace=True)
        df_task.to_csv("todolist.csv", mode='w',encoding='euc-kr',index=False)
        listbox1.delete(ANCHOR)
        doneTaskFile()
        get_chart()



#할 일 저장 파일 
def openTaskFile():
    global task_list
    f = open('todolist.csv','r')
    reader = csv.reader(f)
    next(reader)

    for line in reader :
        if(line[1] == today.strftime("%Y-%m-%d")) :
                task_list.append(line[0])
                listbox1.insert(END, line[0])
                
#완료한 일 저장 파일
def doneTaskFile():
    listbox2.delete(0,END)
    global done_list
    f = open('todolist_done.csv','r')
    reader = csv.reader(f)
    next(reader)

    for line in reader :
        if(line[1] == today.strftime("%Y-%m-%d")) :
                done_list.append(line[0])
                listbox2.insert(END, line[0])


#알람
def alarm():
        main_time = datetime.datetime.now().strftime("%H:%M %p")
        alarm_time = get_alarm_time_entry.get()
        alarm_time1,alarm_time2 = alarm_time.split(' ')
        alarm_hour, alarm_minutes = alarm_time1.split(':')
        main_time1,main_time2 = main_time.split(' ')
        main_hour1, main_minutes = main_time1.split(':')
        if int(main_hour1) > 12 and int(main_hour1) < 24:
                main_hour = str(int(main_hour1) - 12)
        else:
                main_hour = main_hour1
        if int(alarm_hour) == int(main_hour) and int(alarm_minutes) == int(main_minutes) and main_time2 == alarm_time2:
                for i in range(3):
                        alarm_status_label.config(text='--알람 종료--')
                        if platform.system() == 'Windows':
                                winsound.Beep(5000,1000)
                        elif platform.system() == 'Darwin':
                                os.system('say Time is Up')
                        elif platform.system() == 'Linux':
                                os.system('beep -f 5000')
                get_alarm_time_entry.config(state='enabled')
                set_alarm_button.config(state='enabled')
                get_alarm_time_entry.delete(0,END)
                alarm_status_label.config(text = '')
        else:
                alarm_status_label.config(text='~알람 시작~')
                get_alarm_time_entry.config(state='disabled')
                set_alarm_button.config(state='disabled')
        alarm_status_label.after(1000, alarm)


#### Notebook 탭 메뉴 ####
tabs_control = Notebook(window)
todolist_tab = Frame(tabs_control)
clock_tab = Frame(tabs_control)
stopwatch_tab = Frame(tabs_control)
calender_tab = Frame(tabs_control)
chart_tab = Frame(tabs_control)
alarm_tab=Frame(tabs_control)

image1= PhotoImage(file="Images/win1.png")
image2= PhotoImage(file="Images/win2.png")
image3= PhotoImage(file="Images/win3.png")
image4= PhotoImage(file="Images/win4.png")
image5= PhotoImage(file="Images/win5.png")
image6= PhotoImage(file="Images/win6.png")
image_todo = PhotoImage(file="Images/todo.png")
image_done = PhotoImage(file="Images/done.png")
image_logo = PhotoImage(file="Images/logo.png")
image_time = PhotoImage(file="Images/time.png")

tabs_control.add(todolist_tab, image=image1)
tabs_control.add(chart_tab, image=image5)
tabs_control.add(calender_tab, image=image2)
tabs_control.add(stopwatch_tab, image=image3)
tabs_control.add(clock_tab, image=image4)
tabs_control.add(alarm_tab, image=image6 )

tabs_control.pack(expand = 1, fill ="both")


############## 스톱워치 기능 ##############
running=False       
timer=0 

timeText=tk.Label(stopwatch_tab, text="00:00", font=("Helvetica", 80))  
timeText.pack(fill=tk.BOTH)

startButton=customtkinter.CTkButton(stopwatch_tab, text="start", fg_color=None, border_width=1, command=start)
startButton.pack(fill=tk.BOTH,pady=10, padx=100)

stopButton=customtkinter.CTkButton(stopwatch_tab, text="stop", fg_color=None, border_width=1, command=stop)
stopButton.pack(fill=tk.BOTH,pady=10, padx=100)

initialButton = customtkinter.CTkButton(stopwatch_tab, text = 'reset', fg_color=None, border_width=1, command=initial)
initialButton.pack(fill=tk.BOTH,pady=10, padx=100)


############## 시계 기능 ##############
txt_frame = tk.Frame(clock_tab)
txt_frame.pack(fill=tk.BOTH)

txt_width = tk.Label(txt_frame, image=image_time)
txt_width.pack(fill=tk.BOTH,pady=20)

clock_frame = tk.Frame(clock_tab)
clock_frame.pack(fill=tk.BOTH)

clock_width = tk.Label(clock_frame, font=("Helvetica", 80), bg="white", bd=8)
clock_width.pack(fill=tk.BOTH)


############## 달력기능 ##############

cal = Calendar(calender_tab,selectmode='day')
cal.pack(fill=BOTH,expand=True)


############## 일정출력 ##############

l_logo = tk.Label(todolist_tab, image=image_logo)
l_logo.grid(row= 0, column = 0, columnspan=2, pady=20)
l_todo = tk.Label(todolist_tab,image=image_todo)
l_todo.grid(row= 1, column = 0)

l_done = tk.Label(todolist_tab,image=image_done)
l_done.grid(row= 1, column = 1)


listbox1 = Listbox(todolist_tab,font=('arial',14),width=20,height=10, borderwidth=0,
                        bg="white",fg="#32405b",cursor="hand2",selectbackground="#D35B58",
                        highlightthickness=2)
listbox1.grid(column=0, row=2, rowspan=6, sticky="nwe", padx=10, pady=15)

scrollbar= Scrollbar(todolist_tab)
scrollbar.grid(column=0, row=2, rowspan=6, sticky="nse", padx=10, pady=15)

listbox1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox1.yview)


listbox2 = Listbox(todolist_tab,font=('arial',14),width=20,height=10, borderwidth=0,
                        bg="white",fg="#32405b",cursor="hand2",selectbackground="#D35B58",
                        highlightthickness=2)
listbox2.grid(column=1, row=2, rowspan=6, sticky="nwe", pady=15, padx=5)

scrollbar= Scrollbar(todolist_tab)
scrollbar.grid(column=1, row=2, rowspan=6, sticky="nse", padx=5, pady=15)

listbox2.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox2.yview)


task=StringVar()
task_entry = customtkinter.CTkEntry(master=todolist_tab,
                                        width=120)
task_entry.grid(row=8, column=0, columnspan=2
                , pady=30, padx=20, sticky="ew")
task_entry.focus()

button_add = customtkinter.CTkButton(master=todolist_tab,
                                        text="ADD",
                                        border_width=1,  # <- custom border_width
                                        fg_color=None,  # <- no fg_color
                                        command=addTask)
button_add.grid(row=9, column=0, sticky="ew",padx=30)

button_delete = customtkinter.CTkButton(master=todolist_tab,
                                        text="DONE",
                                        border_width=1,  # <- custom border_width
                                        fg_color=None,  # <- no fg_color
                                        command=doneTask)
button_delete.grid(row=9, column=1, sticky="ew",padx=30)


#################### 일과 달성율보기 #################
def get_chart():
    date_arr = []
    done_arr = []

    for i in range(0,7):
        count_task = 0
        count_done = 0
        
        date = today - datetime.timedelta(days=i)
        date_str = date.strftime('%m/%d')
        date_arr.append(date_str)

        count_task = len(df_task.loc[df_task['날짜'] == date.strftime('%Y-%m-%d')]) + len(df_done.loc[df_done['날짜']== date.strftime('%Y-%m-%d')])
        count_done = len(df_done.loc[(df_done['날짜'] == date.strftime('%Y-%m-%d'))]) #특정날짜의 완료된 일정의 갯수 세기
        
        if ( count_task == 0) :
            done_perc = 0
        else :
            done_perc = (count_done/count_task) * 100 #일정 달성률
        done_arr.append(done_perc)

    for widgets in chart_tab.winfo_children():
        widgets.destroy()

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    axis = fig.add_subplot(111)
    xValues = date_arr
    yValues = done_arr
    t, = axis.plot(date_arr, done_arr, color='green', marker='o', linestyle='solid')
    canvas = FigureCanvasTkAgg(fig, chart_tab)
    canvas.get_tk_widget().pack()

    l_chart = tk.Label(chart_tab,text="지난 7일간의 달성율입니다. KEEP GOING!", font="arial 12")
    l_chart.pack()


######### 알람 기능 ##########
get_alarm_time_entry = tk.Entry(alarm_tab, bg = "#D4AC0D", font ='calibri 25 bold')
get_alarm_time_entry.pack(pady=15, anchor='center')

alarm_instructions_label = tk.Label(alarm_tab, font = 'calibri 20 bold', text = """Enter Alarm Time. Eg -> 01:30 PM, 
01 -> Hour, 30 -> Minutes""")
alarm_instructions_label.pack(anchor='s')

set_alarm_button = tk.Button(alarm_tab, text = "알람 설정", relief = "solid", fg="Black", bg="#D4AC0D", width = 20, 
                                        font=("Helevetica",20,"bold"), command=alarm)
set_alarm_button.pack(pady=15, anchor='s')

alarm_status_label = tk.Label(alarm_tab, font = 'calibri 15 bold')
alarm_status_label.pack(anchor='s')

###### 프레임당 디폴트 실행 #######
openTaskFile()
doneTaskFile()
startTimer()
clock()
get_chart()

window.mainloop()   # 윈도우를 이벤트 대기상태로 설정
                    # 원도우 창에서 마우스 클릭 같은 이벤트들이 발생하게끔 유지