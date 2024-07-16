#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import time
import math
import sys
import ctypes

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("IEEE 754 Conventer")          
        self.init_window_name.geometry('1280x720+100+50')          #+10+10定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "pink"                                    
        #self.init_window_name.attributes("-alpha", 0.95)          #虚化，值越小虚化程度越高
        self.init_window_name.iconbitmap("D:\\Code\\Python\\Tkinter Coding\\IEEE754\\conventer.ico")
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")  

        self.init_data_label = Label(self.init_window_name, text="待处理数据", width=10, height=2, font=('楷体', 15, 'bold'))
        self.init_data_label.grid(row=0, column=0, padx=(40, 10), pady=15)
        self.result_data_label = Label(self.init_window_name, text="输出结果", width=10, height=2, font=('楷体', 15, 'bold'))
        self.result_data_label.grid(row=0, column=12, padx=(10, 0), pady=15)
        self.log_label = Label(self.init_window_name, text="日志", width=10, height=2, font=('楷体', 15, 'bold'))
        self.log_label.grid(row=12, column=0, padx=(40, 10), pady=10)

        #文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=30)    #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10, padx=(40, 10))
        self.result_data_Text = Text(self.init_window_name, width=67, height=45)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10, padx=(10, 0))
        self.log_data_Text = Text(self.init_window_name, width=67, height=10)     # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10, padx=(40, 10))

        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="转换", bg="lightblue", width=10, font=('楷体', 15, 'bold'), command=self.IEEE_Convert)
        self.str_trans_to_md5_button.grid(row=1, column=11, padx=20)

    #功能函数
    def IEEE_Convert(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n","").encode()
        #print("src = ", src)

        i_zheng = 0
        i_xiao = 0.0
        _sign, _exp, _frac, _whole = 0, [0] * 80, [0] * 230, [0] * 320
        wholepos = 0
        zheng_bin, xiao_bin = [0] * 320, [0] * 320

        if src:
            try:
                i = float(src)
                if i > 1e10 or i < -1e10:
                    self.write_log_to_Text("ERROR: Number is too big / small")
                    self.result_data_Text.delete(1.0, END)
                    self.result_data_Text.insert(1.0, "您提供的数字不在表示范围内")  
                    return
                
                if i >= 0:
                    i_zheng = math.floor(i)
                    i_xiao = i - math.floor(i)
                    _sign = 0

                else:
                    i_zheng = math.ceil(i) * (-1)
                    i_xiao = (i - math.ceil(i)) * (-1)
                    _sign = 1

                cnt1, cnt2, cnt2_first, flag = 0, 0, 0, 0
                while i_zheng:
                    zheng_bin[cnt1] = i_zheng % 2
                    i_zheng //= 2
                    cnt1 += 1

                while True:
                    i_xiao *= 2
                    if i_xiao < 1 and i_xiao != 0:
                        xiao_bin[cnt2] = 0
                        cnt2 += 1

                    elif i_xiao > 1:
                        xiao_bin[cnt2] = 1
                        cnt2 += 1
                        i_xiao -= 1
                        if flag == 0:
                            cnt2_first = cnt2
                            flag = 1

                    elif i_xiao == 0:
                        break

                    else:
                        xiao_bin[cnt2] = 1
                        cnt2 += 1
                        if flag == 0:
                            cnt2_first = cnt2
                            flag = 1
                            break
                        if cnt2 > 31:
                            break
                
                #print(i)
                if abs(i) >= 1:
                    exp_shi = 127 + (cnt1 - 1)
                elif abs(i) > 0 and abs(i) < 1:
                    exp_shi = 127 - cnt2_first
                else:
                    exp_shi = 0

                for j in range(7, -1, -1):
                    _exp[j] = exp_shi % 2
                    exp_shi //= 2

                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.delete(2.0, END)
                self.result_data_Text.insert(1.0, "Sign: ")
                self.result_data_Text.insert(2.0, str(_sign))
                _whole[wholepos] = _sign
                wholepos += 1

                self.result_data_Text.delete(3.0, END)
                self.result_data_Text.delete(4.0, END)
                self.result_data_Text.insert(3.0, "\n")
                self.result_data_Text.insert(3.1, "Exponent: ")
                for j in range(8):
                    self.result_data_Text.insert(4.0, str(_exp[j]))
                    _whole[wholepos] = _exp[j]
                    wholepos += 1
                    if j == 3:
                        self.result_data_Text.insert(4.0, " ")

                self.result_data_Text.delete(5.0, END)
                self.result_data_Text.delete(6.0, END)
                self.result_data_Text.insert(5.0, "\n")
                self.result_data_Text.insert(5.1, "Mantissa: ")
                #print(i)
                if abs(i) >= 1:
                    pos = 0
                    for j in range(cnt1 - 2, -1, -1):
                        _frac[pos] = zheng_bin[j]
                        pos += 1
                    for j in range(0, cnt2 + 1):
                        _frac[pos] = xiao_bin[j]
                        pos += 1
                    for j in range(pos, 23):
                         _frac[j] = 0
                else:
                    pos = 0
                    for j in range(cnt2_first, 50):
                        _frac[pos] = xiao_bin[cnt2_first]
                        cnt2_first += 1
                        pos += 1
                        if(pos >= 23):
                            break

                for j in range(23):
                    self.result_data_Text.insert(6.0, str(_frac[j]))
                    _whole[wholepos] = _frac[j]
                    wholepos += 1
                    if (j + 1) % 4 == 0:
                        self.result_data_Text.insert(6.0, " ")

                self.result_data_Text.delete(7.0, END)
                self.result_data_Text.delete(8.0, END)
                self.result_data_Text.insert(7.0, "\n")
                self.result_data_Text.insert(7.1, "Binary Representation: ")
                for j in range(32):
                    self.result_data_Text.insert(8.0, str(_whole[j]))
                    if (j + 1) % 4 == 0:
                        self.result_data_Text.insert(8.0, " ")

                self.result_data_Text.delete(9.0, END)
                self.result_data_Text.delete(10.0, END)
                self.result_data_Text.insert(9.0, "\n")
                self.result_data_Text.insert(9.1, "Hexadecimal Representation: ")
                hexnumber = 0
                for j in range(0, 32, 4):
                    if _whole[j] == 1:
                        hexnumber += 8
                    if _whole[j + 1] == 1:
                        hexnumber += 4
                    if _whole[j + 2] == 1:
                        hexnumber += 2
                    if _whole[j + 3] == 1:
                        hexnumber += 1

                    if hexnumber >= 10:
                        self.result_data_Text.insert(10.0, str(chr(hexnumber + 55)))
                    else:
                        self.result_data_Text.insert(10.0, str(hexnumber))

                    if i == 12:
                        self.result_data_Text.insert(10.0, " ")

                    hexnumber = 0

                self.write_log_to_Text("INFO: Success!") 

            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "输入的不是数字")
                self.write_log_to_Text("ERROR: Not a number")
        else:
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, "坏了！无法转换")
            self.write_log_to_Text("ERROR: Failed to convert") 

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #日志打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"
        if LOG_LINE_NUM <= 8:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)

def gui_start():
    init_window = Tk()                # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)  # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()            # 父窗口进入事件循环，保持窗口运行，否则界面不展示


gui_start()