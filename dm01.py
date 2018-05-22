# -*- coding: utf-8 -*-

# import
import tkinter as tk
import tkinter.filedialog as filedialog
import os
import re
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import *
from tkinter import Menu


win = tk.Tk()  # 2 Create instance
win.title("Pro-wave 資料整理 V2.0")     # 視窗抬頭文字
win.geometry("538x380+120+100")         # 設定視窗大小及起始位置
win.resizable(0, 0)                     # 關閉視窗長寬可變大小


# 下划线这种命名方式表明这是私有函数不是被客户端调用的
def _quit():
    win.quit()
    win.destroy()
    exit()


style = ttk.Style()
style.configure("BW.TLabel", font=("Helvetica", "16", 'normal'))
tabControl = ttk.Notebook(win)                                      # create tab control
tab1 = ttk.Frame(tabControl, style="BW.TLabel")                     # create a tab
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='   SPL   ')                              # tab control add a tab & name
tabControl.add(tab2, text='   TEST   ')
tabControl.pack(expand=1, fill="both")                              # Pack to make visible

monty = ttk.LabelFrame(tab1, text='整理')                           # 在tab1加入一個frame
monty.grid(column=0, row=0, padx=8, pady=4)                         # frame的格式

monty2 = ttk.LabelFrame(tab2, text=' The Snake ')                   # 在tab2加入一個frame
monty2.grid(column=0, row=0, padx=8, pady=4)

# tab 1
var2 = tk.Variable()
scr1 = tk.Scrollbar(win, orient="vertical")
lb = tk.Listbox(monty, width=20, height=20, listvariable=var2)                 # 将var2的值赋给Listbox
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
lb.grid(column=0, row=0, rowspan=20)
scr1.grid(column=0, row=0, rowspan=20, sticky='NES')                # 排上bar


def getdir(Extension):
    d = []
    try:
        filepath = filedialog.askdirectory()
        if filepath:
            d.append(filepath)                                          # 選擇的資料夾
        cf = os.listdir(filepath)                                       # 返回指定的文件夾包含的文件
        for i in cf:
            if os.path.splitext(i)[-1].lower() == Extension:            # 篩選副檔名
                d.append(i)
        return d
    except:
        return 0


def clickMe():
    # action.configure(text="hello " + name.get() + "-" + number.get())
    lb.delete(0, END)                                               # 清空Listbox
    aLabel.configure(text="", foreground="red")                     # 清空Label
    dname = getdir('.spl')                                          # 選擇資料夾裡的檔案

    if dname != 0:
        a = 0
        for i in dname:
            if a == 0:
                aLabel.configure(text=i, foreground="red")
            else:
                lb.insert(END, i)   # 符合名稱的副檔名加入listbox
            a += 1
        lb.see('end')  # 顯示最後一筆


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
    j = i+1
    # print(len(s))
    for i in range(j, len(s)):
        # print(len(s[i]))
        if len(s[i]) != 0:
            a = s[i].split(',')
            d_freq.append(float(a[0]))
            d_db.append(float(a[1]))
    return parameters, d_freq, d_db


def splclick():
    # print(lb.curselection())
    # print(lb.get(ACTIVE))
    # print(lb.size())
    a1 = []                             # 檔名
    a2 = []                             # @dB,Fl
    a3 = []                             # @dB,Fh
    if chSpl_1.get() == 1:
        for i in range(lb.size()):
            a1.append(lb.get(i))                                                # 加入檔名
            d1, d2, d3 = open_spl_file(aLabel.cget("text") + "/" + lb.get(i))   # 開啟檔案並整理資料
            for j in range(d3.index(max(d3)), 0, -1):                           # 計算@dB 的Fl
                if d3[j] < float(vvalue.get()):
                    break
            fl = d2[j+1]+(((d3[j+1] - float(vvalue.get())) * (d2[j+1] - d2[j])) / (d3[j+1] - d3[j]))
            a2.append(round(fl, 1))
            for j in range(d3.index(max(d3)), len(d3)):                         # 計算@dB 的Fh
                if d3[j] < float(vvalue.get()):
                    break
            fh = d2[j - 1] + (((d3[j - 1] - float(vvalue.get())) * (d2[j] - d2[j-1])) / (d3[j - 1] - d3[j]))
            a3.append(round(fh, 2))
        filepath = filedialog.asksaveasfilename(filetypes=(("csv files", "*.csv"), ("all files",  "*.*")))
        file, ext = os.path.splitext(filepath)
        if len(ext) == 0:
            filepath += ".csv"
        print(filepath, file, ext, len(ext))
        fp = open(filepath, "a")                    # 開啟檔案
        j = "檔名"
        for i in a1:
            j += "," + str(i)
        fp.write(j + '\n')                          # 寫入檔案
        j = vvalue.get() + "dB Bandwidth"
        for i in a2:
            j += "," + str(i)
        fp.write(j + '\n')                          # 寫入檔案
        print(j)
        fp.close()                                  # 關閉檔案


action = ttk.Button(monty, text="開啟路徑", command=clickMe)            # 增加按鍵
action.grid(column=1, row=0, sticky='W')
# action.configure(state="disabled")                                # Disable the Button Widget

aLabel = ttk.Label(monty, text="", width=40)                        # add a label
aLabel.grid(column=2, row=0, sticky='W')                           # label 位置+格式
aLabe2 = ttk.Label(monty, text="整理項目:")                        # add a label
aLabe2.grid(column=1, row=1, sticky='E')                           # label 位置+格式

chSpl_1 = tk.IntVar()
splcheck1 = tk.Checkbutton(monty, text="@                dB BandWidth", variable=chSpl_1)
splcheck1.select()
splcheck1.grid(column=2, row=1, padx=0, sticky=tk.W)
# aLabe2 = ttk.Label(monty, text="choose a number")                   # add a label
# aLabe2.grid(column=2, row=1, sticky=tk.W)                           # label 位置+格式

vvalue = tk.StringVar()
vvalue.set(100)
nameEntered = ttk.Entry(monty, width=4, textvariable=vvalue)         # 增加textbox
nameEntered.grid(column=2, row=1, padx=40, sticky=tk.W)

splaction = ttk.Button(monty, text="整理", command=splclick)            # 增加按鍵
splaction.grid(column=2, row=19, sticky='ENS')
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
# 0 (unchecked) or 1 (checked) so the type of the variable is a tkinter integer.
chVarDis = tk.IntVar()
check1 = tk.Checkbutton(monty2, text="Disabled", variable=chVarDis, state='disabled')
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
    curRad = tk.Radiobutton(monty2, text=colors[col], variable=radVar, value=col, command=radCall)
    curRad.grid(column=col, row=5, sticky=tk.W)

# Using a scrolled Text control
scrollW = 30
scrollH = 3
scroll = st.ScrolledText(monty2, width=scrollW, height=scrollH, wrap=tk.WORD)
scroll.grid(column=0, columnspan=3, sticky='WE') # sticky='WE' 该属性左右对其，做下面的测试时可以注释查看效果
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
