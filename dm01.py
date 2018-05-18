# -*- coding: utf-8 -*-

# import
import tkinter as tk  # 1 imports

from tkinter import ttk

from tkinter import scrolledtext as st
from tkinter import Menu


win = tk.Tk()  # 2 Create instance
win.title("Python GUI")  # 3 Add a title
win.resizable(0, 0)           # 4 Disable resizing the GUI


menuBar = Menu(win)
win.config(menu=menuBar)


# 下划线这种命名方式表明这是私有函数不是被客户端调用的
def _quit():
    win.quit()
    win.destroy()
    exit()


fileMenu = Menu(menuBar)
fileMenu.add_command(label="New")
fileMenu.add_separator()                                            # 分隔線
fileMenu.add_command(label="Exit", command=_quit)
menuBar.add_cascade(label="File", menu=fileMenu)

helpMenu = Menu(menuBar)
helpMenu.add_command(label="About")
menuBar.add_cascade(label="Help", menu=helpMenu)

style = ttk.Style()
style.configure("BW.TLabel", font=("Helvetica", "16", 'normal'))
tabControl = ttk.Notebook(win)                                      # create tab control
tab1 = ttk.Frame(tabControl, style="BW.TLabel")                                        # create a tab
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='   SPL   ')                               # tab control add a tab & name
tabControl.add(tab2, text='   SEN   ')
tabControl.pack(expand=1, fill="both")                              # Pack to make visible


monty = ttk.LabelFrame(tab1, text='整理')                  # 在tab1加入一個frame
monty.grid(column=0, row=0, padx=8, pady=4)                        # frame的格式

monty2 = ttk.LabelFrame(tab2, text=' The Snake ')                   # 在tab2加入一個frame
monty2.grid(column=0, row=0, padx=8, pady=4)

var2 = tk.StringVar()
scr1 = tk.Scrollbar(win, orient="vertical")
lb = tk.Listbox(monty, width=20, listvariable=var2)                           # 将var2的值赋给Listbox
list_items = [1,2,3,4]                 # 创建一个list并将值循环添加到Listbox控件中
for item in list_items:
    lb.insert('end', item)                                          # 从最后一个位置开始加入值
# lb.insert(1, 'first')                                               # 在第一个位置加入'first'字符
# lb.insert(2, 'second')                                              # 在第二个位置加入'second'字符
# lb.delete(0, 'end')                                                 # 删除所有
# lb.delete(0)                                                        # 删除第0
# lb.pack()

scr1 = tk.Scrollbar(monty)
lb.config(yscrollcommand=scr1.set)
scr1.config(command=lb.yview)
lb.grid(column=0, row=0, rowspan=20)
scr1.grid(column=0, row=0, rowspan=20, sticky='NES')

aLabel = ttk.Label(monty, text="输入文本：")                        # add a label
aLabel.grid(column=2, row=0, sticky=tk.W)                           # label 位置+格式
aLabe2 = ttk.Label(monty, text="choose a number")                   # add a label
aLabe2.grid(column=3, row=0, sticky=tk.W)                           # label 位置+格式

number = tk.StringVar()
# 只能選擇我們已經編入Combobox的值：state ="readonly"
numberChosen = ttk.Combobox(monty, width=12, textvariable=number, state="readonly")
numberChosen.grid(column=3, row=1, sticky=tk.W)                     # combobox 位置+格式
numberChosen["values"] = (1, 2, 3, 4, 5, 6, 12)                     # 預設值
numberChosen.current(3)                                             # 顯示第幾個預設


def clickMe():
    action.configure(text="hello " + name.get() + "-" + number.get())
    # aLabel.configure(foreground="red")
    lb.insert('end', "++++")


action = ttk.Button(monty, text="開啟路徑", command=clickMe)            # 增加按鍵
action.grid(column=4, row=1)
# action.configure(state="disabled")                                # Disable the Button Widget

name = tk.StringVar()
nameEntered = ttk.Entry(monty, width=12, textvariable=name)         # 增加textbox
nameEntered.grid(column=2, row=1, sticky=tk.W)
nameEntered.focus()                                                 # Place cursor into name Entry


# Creating three checkbuttons    # 1
# 0 (unchecked) or 1 (checked) so the type of the variable is a tkinter integer.
chVarDis = tk.IntVar()  # 2
check1 = tk.Checkbutton(monty2, text="Disabled", variable=chVarDis, state='disabled')  # 3
check1.select()  # 4
check1.grid(column=0, row=4, sticky=tk.W)  # 5

chVarUn = tk.IntVar()  # 6
check2 = tk.Checkbutton(monty2, text="UnChecked", variable=chVarUn)
check2.deselect()  # 8
check2.grid(column=1, row=4, sticky=tk.W)  # 9

chVarEn = tk.IntVar()  # 10
check3 = tk.Checkbutton(monty2, text="Enabled", variable=chVarEn)
check3.select()  # 12
check3.grid(column=2, row=4, sticky=tk.W)  # 13

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
nameEntered.focus()

win.mainloop()  # 5 Start GUI
