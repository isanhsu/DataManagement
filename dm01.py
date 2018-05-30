# -*- coding: utf-8 -*-

# import
import tkinter as tk
import tkinter.filedialog as filedialog
import os
import re
import ctypes                           # 對話框
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import *
from natsort import natsorted           # 檔名排序
from tkinter import Menu


win = tk.Tk()  # 2 Create instance
win.title("Pro-wave 資料整理 V2.0")     # 視窗抬頭文字
win.geometry("538x480+120+100")         # 設定視窗大小及起始位置
win.resizable(0, 0)                     # 關閉視窗長寬可變大小


# 下划线这种命名方式表明这是私有函数不是被客户端调用的
def _quit():
    win.quit()
    win.destroy()
    exit()


def message_box(title, text, style):    # 對話框
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def getdir(Extension):
    d = []
    try:
        options = {}
        options['title'] = "請選擇資料夾"
        filepath = filedialog.askdirectory(**options)
        if filepath:
            # 選擇的資料夾
            d.append(filepath)
        # 返回指定的文件夾包含的文件
        cf = os.listdir(filepath)
        for i in cf:
            if os.path.splitext(i)[-1].lower() == Extension:            # 篩選副檔名
                d.append(i)
        return d
    except BaseException:
        return 0


def open_spl_file(path):
    parameters = []
    d_freq = []
    d_db = []

    f = open(path, 'r')
    s = f.read().split('\n')
    # print(s)
    f.close()
    for i in range(20):
        # print(str(i) + ',' + s[i])
        if i < 6:
            a = s[i].split(',')
            parameters.append(float(a[1]))
        if i == 6:
            a = s[i].split(',')
            parameters.append(a[1].strip())
        if i == 10:
            a = s[i].split(',')
            parameters.append(a[-1].strip())
        if 12 < i < 18:
            a = s[i].split(',')
            parameters.append(float(a[1]))
            parameters.append(float(a[4]))
        if i == 18:
            a = s[i].split(',')
            parameters.append(float(a[1]))
            a = re.split(r"[(d]", a[0])
            parameters.append(float(a[1]))
        if i == 19:
            a = s[i].split(',')
            parameters.append(float(a[-1]))
    j = i + 1
    # print(len(s))
    for i in range(j, len(s)):
        # print(len(s[i]))
        if len(s[i]) != 0:
            a = s[i].split(',')
            d_freq.append(float(a[0]))
            d_db.append(float(a[1]))
    return parameters, d_freq, d_db


def splclick():                         # Spl 整理按鍵
    if lb.size() != 0:                  # 判斷是否有要整理的檔案
        if chSpl_1.get() == 1 or chSpl_2.get() == 1 or chSpl_3.get(
        ) == 1 or chSpl_4.get() == 1 or chSpl_5.get() == 1 or chSpl_6.get() == 1:
            a1 = []
            for i in range(lb.size()):
                lb2.insert(0, "整理檔案: " + aLabel.cget("text") + "/" + lb.get(i))  # 顯示資訊
                d1, d2, d3 = open_spl_file(
                    aLabel.cget("text") + "/" + lb.get(i))  # 開啟檔案並整理資料
                if i == 0:
                    a2 = []
                    a2.append("檔名")
                    if chSpl_1.get() == 1:
                        a2.append("@" + vvalue.get() + " BW")
                    if chSpl_3.get() == 1:
                        a2.append("FrdB")
                        a2.append("FrFreq")
                    if chSpl_4.get() == 1:
                        a2.append("RateddB")
                        a2.append("RatedFreq")
                    if chSpl_5.get() == 1:
                        a2.append("Fc")
                        a2.append("Fh")
                        a2.append("Fl")
                    if chSpl_6.get() == 1:
                        a2.append("BW")
                    a1.append(a2)
                a2 = []
                a2.append(lb.get(i))                            # 加入檔名
                if chSpl_1.get() == 1:                          # 計算 @ 多少dB 的 BW
                    for j in range(                             # 計算@dB 的Fl
                        d3.index(
                            max(d3)), 0, -1):
                        if d3[j] < float(vvalue.get()):
                            break
                    fl = d2[j + 1] + (((d3[j + 1] - float(vvalue.get()))
                                       * (d2[j + 1] - d2[j])) / (d3[j + 1] - d3[j]))
                    for j in range(                                 # 計算@dB 的Fh
                            d3.index(max(d3)), len(d3)):
                        if d3[j] < float(vvalue.get()):
                            break
                    fh = d2[j - 1] + (((d3[j - 1] - float(vvalue.get()))
                                       * (d2[j] - d2[j - 1])) / (d3[j - 1] - d3[j]))
                    # 加入 @dB 的 BW
                    a2.append(round(fh - fl, 2))
                if chSpl_3.get() == 1:
                    a2.append(d1[8])        # FrdB
                    a2.append(d1[9])        # FrFreq
                if chSpl_4.get() == 1:
                    a2.append(d1[10])       # RateddB
                    a2.append(d1[11])       # RatedFreq
                if chSpl_5.get() == 1:
                    a2.append(d1[13])       # Fc
                    a2.append(d1[15])       # Fh
                    a2.append(d1[17])       # Fl
                if chSpl_6.get() == 1:
                    a2.append(d1[18])       # BW
                if chSpl_2.get() == 1:
                    if i == 0:
                        for k in range(len(d2)):
                            if k == 0:
                                a1index=len(a1[0])
                            a1[0].append(d2[k])     # 加入 Freq 標籤
                        print(a1[0][a1index])       # 標籤起始位置

                    for k in range(len(d3)):
                        a2.append(d3[k])    # dB

                a1.append(a2)           # 將 a2[] 加入 a1[] 變二維
            lb2.insert(0, "存檔中......")                   # 顯示資訊
            filepath = filedialog.asksaveasfilename(
                filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
            file, ext = os.path.splitext(filepath)
            if len(file) != 0 and len(ext) == 0:            # 自動加入附檔名
                filepath += ".csv"
            if len(filepath) != 0:                          # 檢查是否有輸入檔名
                lb2.insert(0, "檔案存檔: " + filepath)      # 顯示資訊
                fp = open(filepath, "w")                    # 開啟檔案

                print(len(a1),len(a1[0]))
                for j in range(len(a1[0])):
                    tp = ''
                    for i in range(len(a1)):
                        print(a1[i][j])
                        tp += str(a1[i][j]) + ','
                    fp.write(tp + '\n')                     # 寫入檔案
                fp.close()                                  # 關閉檔案
            lb2.insert(0, "!!!檔案整理完成!!!")             # 顯示資訊
        else:
            message_box('警告', '沒有勾選要整理項目', 0)  # 跳出對話方塊
    else:
        message_box('警告', '沒有選擇檔案', 0)  # 跳出對話方塊


def clickOpen():            # 開啟路徑
    # action.configure(text="hello " + name.get() + "-" + number.get())
    lb.delete(0, END)                                               # 清空Listbox
    aLabel.configure(text="", foreground="red")                     # 清空Label
    # 選擇資料夾並篩選附檔名
    dname = getdir('.spl')
    if dname != 0:
        aLabel.configure(text=dname[0], foreground="red")
        lb2.insert(0, "開啟路徑: " + dname[0])            # 顯示資訊:路徑
        lb2.insert(0, "檔案總數: " + str(len(dname)-1))   # 顯示資訊:檔案數
        del dname[0]
        lb.insert(END, *natsorted(dname))  # 排序後符合名稱的副檔名加入listbox
        # lb.see('end')  # 顯示最後一筆
    action_del.configure(state="enabled")


def clickDel():             # 刪除選取
    indexs = lb.curselection()                                      # 讀取有選擇的LISTBOX
    for i in sorted(
            indexs,
            reverse=True):                          # 對indexs做逆排序並循環for
        # 刪除所選擇的Listbox 選項
        lb.delete(i)
    print(lb.size(), chSpl_1.get())


style = ttk.Style()
style.configure("BW.TLabel", font=("Helvetica", "16", 'normal'))
# create tab control
tabControl = ttk.Notebook(win)
# create a tab
tab1 = ttk.Frame(tabControl, style="BW.TLabel")
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
# tab control add a tab & name
tabControl.add(tab1, text='   SPL   ')
tabControl.add(tab2, text='   EDB   ')
tabControl.add(tab3, text='   TEST   ')
# Pack to make visible
tabControl.pack(expand=1, fill="both")

# 在tab1加入一個frame
monty = ttk.LabelFrame(tab1, text=' SPL 整理 ')
monty.grid(column=0, row=0, padx=4, pady=0)                         # frame的格式

# 在tab2加入一個frame
monty2 = ttk.LabelFrame(tab3, text=' The Snake ')
monty2.grid(column=0, row=0, padx=8, pady=4)

# tab 1
var2 = tk.Variable()
scr1 = tk.Scrollbar(win, orient="vertical")
lb = tk.Listbox(monty, width=20, height=20, listvariable=var2,
                selectmode=EXTENDED)    # 將var2的值賦給Listbox,多選
# list_items = [1,2,3,4]                                              # 创建一个list并将值循环添加到Listbox控件中
# for item in list_items:
#     lb.insert('end', item)                                          # 从最后一个位置开始加入值
# lb.insert(1, 'first')                                               # 在第一个位置加入'first'字符
# lb.insert(2, 'second')                                              # 在第二个位置加入'second'字符
# lb.delete(0, 'end')                                                 # 删除所有
# lb.delete(0)                                                        # 删除第0
# lb.pack()
scr1 = tk.Scrollbar(monty)
lb.config(yscrollcommand=scr1.set)
scr1.config(command=lb.yview)
lb.grid(column=0, row=1, columnspan=2, rowspan=20, sticky='W')
scr1.grid(
    column=0,
    row=1,
    columnspan=2,
    rowspan=20,
    sticky='NES')                # 排上bar

var3 = tk.Variable()
splscr1 = tk.Scrollbar(win, orient="vertical")
lb2 = tk.Listbox(monty, height=5, listvariable=var3,  selectmode=EXTENDED)    # 將var2的值賦給Listbox,多選
splscr1 = tk.Scrollbar(monty)
lb2.config(yscrollcommand=splscr1.set)
splscr1.config(command=lb2.yview)
lb2.grid(column=0, row=21, columnspan=5, sticky='WE')
splscr1.grid(column=0, row=21, columnspan=5,  sticky='NES')                # 排上bar


action_del = ttk.Button(
    monty,
    width=8,
    text="刪除選取",
    command=clickDel)            # 增加按鍵
action_del.grid(column=0, row=0, columnspan=2, sticky='W')
action_del.configure(state="disabled")
action = ttk.Button(
    monty,
    width=8,
    text="開啟路徑",
    command=clickOpen)            # 增加按鍵
action.grid(column=1, row=0, columnspan=2, sticky='W')
# action.configure(state="disabled")                                #
# Disable the Button Widget

# add a label
aLabel = ttk.Label(monty, text="", width=53)
aLabel.grid(
    column=2,
    row=0,
    columnspan=3,
    sticky='W')                           # label 位置+格式

aLabe2 = ttk.Label(monty, text="整理項目:")                        # add a label
# label 位置+格式
aLabe2.grid(column=2, row=1, sticky='E')

chSpl_1 = tk.IntVar()
splcheck1 = tk.Checkbutton(
    monty,
    text="@                dB BandWidth",
    variable=chSpl_1)
# splcheck1.select()
splcheck1.grid(column=3, row=1, sticky='W')

vvalue = tk.StringVar()
vvalue.set(100)
nameEntered = ttk.Entry(
    monty,
    width=4,
    textvariable=vvalue)            # 增加textbox
nameEntered.grid(column=3, row=1, padx=40, sticky=tk.W)

chSpl_2 = tk.IntVar()
splcheck2 = tk.Checkbutton(
    monty,
    text="頻率 & dB 資料 ( Spl dB data )",
    variable=chSpl_2)
splcheck2.grid(column=3, row=2, sticky='W')

chSpl_3 = tk.IntVar()
splcheck3 = tk.Checkbutton(
    monty,
    text="諧振頻率 & dB ( Resonant Freq & dB )",
    variable=chSpl_3)
splcheck3.grid(column=3, row=3, sticky='W')

chSpl_4 = tk.IntVar()
splcheck4 = tk.Checkbutton(
    monty,
    text="額定頻率 & dB ( Rated Freq & dB )",
    variable=chSpl_4)
splcheck4.grid(column=3, row=4, sticky='W')

chSpl_5 = tk.IntVar()
splcheck5 = tk.Checkbutton(monty, text="@-6dB Fc Fh Fl", variable=chSpl_5)
splcheck5.grid(column=3, row=5, sticky='W')

chSpl_6 = tk.IntVar()
splcheck6 = tk.Checkbutton(monty, text="@-6dB BandWidth", variable=chSpl_6)
splcheck6.grid(column=3, row=6, sticky='W')

splaction = ttk.Button(monty, text="整理", command=splclick)            # 增加按鍵
splaction.grid(column=4, row=19, sticky='ENS')
# nameEntered.focus()                                                 # Place cursor into name Entry
#
# number = tk.StringVar()
# # 只能選擇我們已經編入Combobox的值：state ="readonly"
# numberChosen = ttk.Combobox(monty, width=12, textvariable=number, state="readonly")
# numberChosen.grid(column=1, row=4, sticky=tk.W)                     # combobox 位置+格式
# numberChosen["values"] = (1, 2, 3, 4, 5, 6, 12)                     # 預設值
# numberChosen.current(3)                                             # 顯示第幾個預設

# tab 2
# Creating three checkbuttons
# 0 (unchecked) or 1 (checked) so the type of the variable is a tkinter
# integer.
chVarDis = tk.IntVar()
check1 = tk.Checkbutton(
    monty2,
    text="Disabled",
    variable=chVarDis,
    state='disabled')
check1.select()
check1.grid(column=0, row=4, sticky=tk.W)

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(monty2, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(monty2, text="Enabled", variable=chVarEn)
check3.select()
check3.grid(column=2, row=4, sticky=tk.W)

tk.Scrollbar()


# 代码重构（refactor our code）
# First, we change our Radiobutton global variables into a list.
colors = ["Blue", "Gold", "Red"]
# create three Radiobuttons using one variable
radVar = tk.IntVar()
print(radVar)
# Next we are selecting a non-existing index value for radVar.
# (如果不设置为range范围外的值，初始化页面默认会选中第一个并且不会触发变更背景色的回调函数)
radVar.set(99)


# We have also changed the callback function to be zero-based, using the list instead of module-level global variables.
# Radiobutton callback function
def radCall():
    radSel = radVar.get()
    # if radSel == 0:
    #     win.configure(background=colors[0])
    # elif radSel == 1:
    #     win.configure(background=colors[1])
    # elif radSel == 2:
    #     win.configure(background=colors[2])

    if radSel == 0:
        monty2.configure(text='Blue')
    elif radSel == 1:
        monty2.configure(text='Gold')
    elif radSel == 2:
        monty2.configure(text='Red')


# Now we are creating all three Radiobutton widgets within one loop.
for col in range(3):
    curRad = 'rad' + str(col)
    curRad = tk.Radiobutton(
        monty2,
        text=colors[col],
        variable=radVar,
        value=col,
        command=radCall)
    curRad.grid(column=col, row=5, sticky=tk.W)

# Using a scrolled Text control
scrollW = 30
scrollH = 3
scroll = st.ScrolledText(monty2, width=scrollW, height=scrollH, wrap=tk.WORD)
# sticky='WE' 该属性左右对其，做下面的测试时可以注释查看效果
scroll.grid(column=0, columnspan=3, sticky='WE')
# scroll.grid(column=0, columnspan=3)


# Create a container to hold labels(label的长度取决于LabelFrame标题的长度，当添加的LabelFrame组件的长度大于硬编码的组件大小时，
# 我们会自动将这些组件移动到column 0 列的中心，并在组件左右两侧填充空白，具体可以参看下列两行的区别)
labelsFrame = ttk.LabelFrame(monty2, text=' Labels in a Frame ')
# labelsFrame = ttk.LabelFrame(win)
# labelsFrame.grid(column=0, row=7, padx=20, pady=40)
labelsFrame.grid(column=0, row=7)

# Place labels into the container element # 2
ttk.Label(labelsFrame, text='Label 1').grid(column=0, row=0)
ttk.Label(labelsFrame, text='Label 2').grid(column=0, row=1)
ttk.Label(labelsFrame, text='Label 3').grid(column=0, row=2)
# Place cursor into name Entry
# nameEntered.focus()

win.mainloop()  # 5 Start GUI
