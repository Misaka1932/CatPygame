#血条测试

import tkinter as tk
win = tk.Tk()
win.title('血条测试')
win.geometry('1280x720')
hp = 50
label = tk.Label(bg = 'white', width = hp * 2)
label.place(x = 20, y = 20)
label1 = tk.Label(bg = 'red', width = hp * 2)
label1.place(x = 20, y = 20)

def hit():
    global hp
    hp -= 1
    print('hp:', hp)
    if hp < 0:
        print("Game Over")
        label1.destroy()
    label1.config(width = hp * 2)

def hui():
    global hp
    if hp >= 50:
        pass
    elif hp >= 0 and hp < 50:
        hp += 1
        print('hp:', hp)
        label1.config(width = hp * 2)
    else:
        print("Game Over")
        label1.destroy()

b = tk.Button(text="减血", command = hit)
b.place(x = 200, y = 200)
b2 = tk.Button(text = "加血", command = hui)
b2.place(x = 400, y = 200)

win.mainloop()