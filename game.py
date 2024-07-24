from tkinter import *
from tkinter import messagebox  # 修复messagebox的bug
import time
import math
import sys
import ctypes
from datetime import datetime
import json
import os
import pygame

'''
—————————————————————————————————————————————————————————————————
| Options                                             Name      |
|                                                     Coins     |
| Angel1 Lv.1                                         Lv.1      |
| Angel2 Lv.1                                                   |
| Angel3 Lv.1               CG                                  |
| Angel4 Lv.1                                                   |
| Angel5 Lv.1                                                   |
|                                                               |
|                                                               |
—————————————————————————————————————————————————————————————————
'''

game = Tk()
game.geometry('1280x720+120+50') 
game.title('小游戏')
game.resizable(0,0)

pygame.mixer.init() #初始化混音器模块, 用于加载和播放声音

current_file = os.path.abspath(__file__) #当前代码文件
current_path = os.path.dirname(current_file) + '\\' #当前代码文件所在文件夹路径
#print(current_path)
#background = PhotoImage(file=current_path + 'bg.png')  #设置背景图
#pygame.mixer.music.load(current_path + 'bgm.mp3')      #设置bgm
#pygame.mixer.music.set_volume(0.1)                   #设置bgm音量 (值为0-1)
#pygame.mixer.music.play()

class game_system:
    def __init__(self): #定义必要变量

        # ---------- ↓ 系统变量 ↓ ---------- #
        self.game1 = Frame(game)
        self.canvas = Canvas(self.game1)
        self.px = 1280
        self.py = 720
        self.Save_File_Global = 'global.json'
        self.Save_File_Game =''
        self.system_state = {            #定义游戏状态字典
            'savedata_count': 1
        }
        # ---------- ↑ 系统变量 ↑ ---------- #

        # ---------- ↓ 游戏变量 ↓ ---------- #
        self.game_state = {              #定义游戏数值字典
            'user_name'   : '',
            'user_lv'     : 0,
            'user_coins'  : 0,
            'user_angels' : 0,
            'angel_lv'    : [0, 0, 0, 0, 0]
        }
        #金币增加状态
        self.coins_running_state = 'title'

        self.User_Name = ''
        self.User_lv = 0
        self.Uplevel_User_Coins = [1000, 3000, 6000, 10000, 15000] #升级主人的所需金币 (默认LV0)
        #判断方式：round(User_lv / 5)
        #LV1  - 4  : 每级1000 币  每秒打工产出金币加成10% / 全属性战力值加成10%
        #LV5  - 9  : 每级3000 币  每秒打工产出金币加成20% / 全属性战力值加成20%
        #LV10 - 14 : 每级6000 币  每秒打工产出金币加成30% / 全属性战力值加成30%
        #LV15 - 19 : 每级10000币  每秒打工产出金币加成40% / 全属性战力值加成40%
        #LV20      : 每级15000币  每秒打工产出金币加成60% / 全属性战力值加成60%
        self.coin_round = 0 #int(self.User_lv / 5)
        self.add_coin_buff = 0 #每秒打工产出金币加成初始为0%
        self.POW_buff = 0 #全属性战力值加成初始为0%

        self.User_Coins = 0
        self.Coins_per_second = 10 #默认打工每秒产出金币10个 如果太慢可以修改试试
        self.User_Power = [100, 0, 0, 0, 0, 0] #基础, 水, 火, 木, 暗, 光, 共6种战力值
        #注意：打boss判定胜利条件为：综合战力值 > boss战力值
        # --> boss数值待定 <--
        # --> 综合战力值计算方式待定 <--

        self.User_Angels = 0    #持有的精灵数目
        self.Buy_Angel_Coins = [1000, 2000, 4000, 7000, 10000] #领悟精灵能力所需要的金币数 (领悟后默认lv.1)
        # Water 主人达到1 级可以领悟 需消耗1000 币 水战力初始值加100
        # Fire  主人达到5 级可以领悟 需消耗2000 币 火战力初始值加100
        # Wood  主人达到10级可以领悟 需消耗4000 币 木战力初始值加100
        # Dark  主人达到15级可以领悟 需消耗7000 币 暗战力初始值加100
        # Light 主人达到20级可以领悟 需消耗10000币 光战力初始值加100
        self.Angel_Upgrade_Coins = [100, 200, 400, 800, 1600] #升级精灵所需要的金币数
        # LV1  - 4  每级100币  该属性战力值加成10%
        # LV5  - 9  每级200币  该属性战力值加成20%
        # LV10 - 14 每级400币  该属性战力值加成30%
        # LV15 - 19 每级800币  该属性战力值加成40%
        # LV20      每级1600币 该属性战力值加成60%
        # 水属性所需金币不变，火属性每级+10%, 木属性每级+20%, 暗属性每级+30%, 光属性每级+50%
        self.Angel_lv = [0, 0, 0, 0, 0]
        self.User_Weapon = 'wip'
        #用户武器同上，先不写吧太复杂了感觉
        # ---------- ↑ 游戏变量 ↑ ---------- #

        self.load_global_system()
        self.load_data()
        #print(self.load_global_system())
        #print(self.load_data())
        self.game_start_gui() #启动游戏初始界面

    # ---------- ↓ 启动游戏初始界面 ↓ ---------- #
    def game_start_gui(self): 
        self.game1.place(width=1280, height=720)
        self.canvas.place(width=1280, height=720)
        #self.canvas.create_image(650, 650, image=background)

        self.New_Game1 = Frame(self.game1)  #设置new game外框的位置
        self.New_Game1.place(width=300, height=100, x=900, y=250)
        self.New_Game_Label1 = Label(self.New_Game1, bg='black')
        self.New_Game_Label1.place(width=300, height=100, x=0, y=0)
        self.New_Game_Label2 = Label(self.New_Game1, bg='grey')
        self.New_Game_Label2.place(width=296, height=96, x=2, y=2) #留了2x2的黑边
        self.New_Game_Button = Button(self.New_Game1, text='New Game', 
            font=('consolas', 20), bg='grey', fg='white', bd=0, command=self.new_game_gui)
        self.New_Game_Button.place(width=200, height=50, x=50, y=25)

        self.Load_Game1 = Frame(self.game1)  #设置load game外框的位置
        self.Load_Game1.place(width=300, height=100, x=750, y=400)
        self.Load_Game_Label1 = Label(self.Load_Game1, bg='black')
        self.Load_Game_Label1.place(width=300, height=100, x=0, y=0)
        self.Load_Game_Label2 = Label(self.Load_Game1, bg='grey')
        self.Load_Game_Label2.place(width=296, height=96, x=2, y=2) #留了2x2的黑边
        self.Load_Game_Button = Button(self.Load_Game1, text='Load Game', 
            font=('consolas', 20), bg='grey', fg='white', bd=0, command=self.load_data)
        self.Load_Game_Button.place(width=200, height=50, x=50, y=25)

        self.Options_Game1 = Frame(self.game1)  #设置options外框的位置
        self.Options_Game1.place(width=300, height=100, x=600, y=550)
        self.Options_Game_Label1 = Label(self.Options_Game1, bg='black')
        self.Options_Game_Label1.place(width=300, height=100, x=0, y=0)
        self.Options_Game_Label2 = Label(self.Options_Game1, bg='grey')
        self.Options_Game_Label2.place(width=296, height=96, x=2, y=2) #留了2x2的黑边
        self.Options_Game_Button = Button(self.Options_Game1, text='Options', 
            font=('consolas', 20), bg='grey', fg='white', bd=0, command=self.load_data) #options还没写
        self.Options_Game_Button.place(width=200, height=50, x=50, y=25)

        self.Exit_Game_Circle = self.canvas.create_oval(1050, 520, 1200, 670, fill="gray", width=2)
        self.Exit_Game_Button = Button(text='Exit', 
            font=('consolas', 20), bg='grey', fg='white', bd=0, command=self.game_exit)
        self.Exit_Game_Button.place(width=100, height=50, x=1075, y=570) 

        
    # ---------- ↑ 启动游戏初始界面 ↑ ---------- #

    def new_game_gui(self):
        self.New_Game1.destroy()
        self.Load_Game1.destroy()
        self.Options_Game1.destroy()
        self.canvas.delete(self.Exit_Game_Circle)
        self.Exit_Game_Button.destroy()

        # ---------- ↓ 新窗口读取用户名 ↓ ---------- #
        self.window_askname = Toplevel(game)
        self.window_askname.geometry('300x100+600+300')
        self.window_askname.title('这是一个窗口')
        self.new_name = StringVar()
        self.new_name.set('输入名字喵')
        Label(self.window_askname, text='你的名字是：').place(x=20, y=20)
        entry_new_name = Entry(self.window_askname, textvariable=self.new_name)
        entry_new_name.place(x=100, y=20)
        button_comfirm = Button(self.window_askname, text='确定', command=self.game_run)
        button_comfirm.place(x=130, y=60)
        # ---------- ↑ 新窗口读取用户名 ↑ ---------- #
    
    def game_run(self):
        self.User_Name = self.new_name.get()
        self.window_askname.destroy()

        self.Name_Frame = Frame(self.game1)  #设置name的位置
        self.Name_Frame.place(width=200, height=50, x=20, y=20)
        self.Name_Label = Label(self.Name_Frame, text=self.User_Name, font=('楷体', 18))
        self.Name_Label.place(width=150, height=30, x=0, y=20)
        self.Lv_Label = Label(self.Name_Frame, text='Lv.' + str(self.User_lv), font=('Consolas', 13))
        self.Lv_Label.place(width=50, height=20, x=130, y=0)
        #self.Coins_Label.config(anchor=W)  #左对齐W 右对齐E 居中默认或者CENTER

        self.Coins_Frame = Frame(self.game1)  #设置coins的位置
        self.Coins_Frame.place(width=160, height=50, x=20, y=70)
        self.Coins_Label = Label(self.Coins_Frame, text='金币：' + str(self.User_Coins), font=('Consolas', 15))
        self.Coins_Label.place(width=160, height=50, x=0, y=0)

        self.coins_running_state = 'running'
        self.coins_run()

    def game_exit(self):
        Game_Exit = messagebox.askyesno(title='再见', message='真的要离开嘛? o(TヘTo)')
        if Game_Exit:
            exit()

    # ---------- ↓ 游戏的储存和读取 ↓ ---------- #
    def save_global_system(self):   #保存游戏系统状态
        try:
            with open(self.Save_File_Global, 'w') as f:
                json.dump(self.system_state, f)
        except Exception as e:
            print(f"保存游戏时发生错误: {e}")

    def load_global_system(self):   #读取游戏系统状态
        try:
            with open(self.Save_File_Global, 'r') as f:
                state = json.load(f)
                return state
        except FileNotFoundError:
            self.save_global_system()
            return None
        except Exception as e:
            print(f"加载存档时发生错误: {e}")
            return None

    def save_data(self): #保存游戏存档
        self.Save_File_Game = 'savedata' + str(self.system_state['savedata_count']) + '.json'
        #self.system_state['savedata_count'] += 1  这里还不能写，不然每次save都要+1
        self.game_state['user_name']   = self.User_Name
        self.game_state['user_lv']     = self.User_lv
        self.game_state['user_coins']  = self.User_Coins
        self.game_state['user_angels'] = self.User_Angels
        self.game_state['angel_lv']    = self.Angel_lv
        try:
            with open(self.Save_File_Game, 'w') as f:
                json.dump(self.game_state, f)
        except Exception as e:
            print(f"保存游戏时发生错误: {e}")

    def load_data(self):   #读取游戏系统状态
        try:
            with open(self.Save_File_Game, 'r') as f:
                state = json.load(f)
                return state
        except FileNotFoundError:
            self.save_data()
            return None
        except Exception as e:
            print(f"加载存档时发生错误: {e}")
            return None
    # ---------- ↑ 游戏的储存和读取 ↑ ---------- #

    # ---------- ↓ 加载金币和更新 ↓ ---------- #
    def update_coins(self):
        self.User_Coins += int(self.Coins_per_second * (1.0 + self.add_coin_buff / 100))
        print(self.User_Coins)
        self.Coins_Label = Label(self.Coins_Frame, text='Coins: ' + str(self.User_Coins), font=('Consolas', 15))
        self.Coins_Label.place(width=160, height=50, x=0, y=0)
        #print('wip')
    # ---------- ↑ 加载金币和更新 ↑ ---------- #
    
    # ---------- ↓ 角色升级 ↓ ---------- #
    def User_lv_up(self):
        self.User_lv += 1
        self.coin_round = int(self.User_lv / 5)
        self.val_buff = [0,10,20,30,40,60] 
        self.add_coin_buff = self.val_buff[self.coin_round] 
        self.POW_buff = self.val_buff[self.coin_round] 
        print('升级成功！')

    # ---------- ↑ 角色升级 ↑ ---------- #
    
    # ---------- ↓ 游戏每帧的运行事件 ↓ ---------- #
    def coins_run(self):
        if self.coins_running_state != 'running': return
        self.update_coins()
        game.after(1000, Game.coins_run)
        #print(self.User_Coins)
    # ---------- ↑ 游戏每帧的运行事件 ↑ ---------- #
        
Game = game_system()
game.mainloop()