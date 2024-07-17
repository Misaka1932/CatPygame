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

game = Tk()
game.geometry('1280x720+120+50') 
game.title('小游戏')
game.resizable(0,0)


pygame.mixer.init() #初始化混音器模块, 用于加载和播放声音
background = PhotoImage(file='bg.png') #设置背景图
#pygame.mixer.music.load('bgm.mp3')     #设置bgm
#pygame.mixer.music.set_volume(0.1)     #设置bgm音量


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

        self.User_Name = ''
        self.User_lv = 0
        self.Uplevel_User_Coins = [1000, 3000, 6000, 10000, 15000] #升级主人的所需金币 (默认LV0)
        #判断方式：round(User_lv / 5)
        #LV1  - 4  : 每级1000 币  每秒打工产出金币加成10% / 全属性战力值加成10%
        #LV5  - 9  : 每级3000 币  每秒打工产出金币加成20% / 全属性战力值加成20%
        #LV10 - 14 : 每级6000 币  每秒打工产出金币加成30% / 全属性战力值加成30%
        #LV15 - 19 : 每级10000币  每秒打工产出金币加成40% / 全属性战力值加成40%
        #LV20      : 每级15000币  每秒打工产出金币加成60% / 全属性战力值加成60%

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
        self.canvas.create_image(650, 330, image=background)

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
        self.Load_Game1.place(width=300, height=100, x=900, y=400)
        self.Load_Game_Label1 = Label(self.Load_Game1, bg='black')
        self.Load_Game_Label1.place(width=300, height=100, x=0, y=0)
        self.Load_Game_Label2 = Label(self.Load_Game1, bg='grey')
        self.Load_Game_Label2.place(width=296, height=96, x=2, y=2) #留了2x2的黑边
        self.Load_Game_Button = Button(self.Load_Game1, text='Load Game', 
            font=('consolas', 20), bg='grey', fg='white', bd=0, command=self.load_data)
        self.Load_Game_Button.place(width=200, height=50, x=50, y=25)

        self.Exit_Game1 = Frame(self.game1)  #设置exit外框的位置
        self.Exit_Game1.place(width=300, height=100, x=900, y=550)
        self.Exit_Game_Label1 = Label(self.Exit_Game1, bg='black')
        self.Exit_Game_Label1.place(width=300, height=100, x=0, y=0)
        self.Exit_Game_Label2 = Label(self.Exit_Game1, bg='grey')
        self.Exit_Game_Label2.place(width=296, height=96, x=2, y=2) #留了2x2的黑边
        self.Exit_Game_Button = Button(self.Exit_Game1, text='Exit', 
            font=('consolas', 20), bg='grey', fg='white', bd=0, command=self.game_exit)
        self.Exit_Game_Button.place(width=200, height=50, x=50, y=25)
        
    # ---------- ↑ 启动游戏初始界面 ↑ ---------- #

    def new_game_gui(self):
        print('wip')
    
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
        print('wip')
    # ---------- ↑ 加载金币和更新 ↑ ---------- #
        
game_system()
game.mainloop()