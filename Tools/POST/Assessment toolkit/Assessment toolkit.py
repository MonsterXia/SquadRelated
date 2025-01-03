import base64
import os
import tkinter as tk
from tkinter import ttk
import random
from logo import img

entry_length = []
entry_width = []
label_area = []
weapon_description_label = ["Grenade", "LAT", "HAT"]
grenade_must = ["M203", "GP-25", "SL40"]
grenade_random = [
    # "SL40",
    "L123A2",
    # "GP-25",
    "M203",
    "QLG-10",
    # "M320 GLM HEDP",
    "MKE MGL",
    "M203A1",
    "HK 79"
]
LAT_must = ["M136 AT-4 CS", "RPG7", "RPG26"]
LAT_random = [
    "M72A7 LAW",
    "DZJ08",
    # "RPG-7",
    "RPG-7V2",
    # "M136 AT-4 CS",
    # "RPG-26",
    "FN FAL HEAT Rifle Grenade",
    "HAR-66 LAW"
]
HAT_must = ["M3 MAAWS", "RPG-28", "RPG-7V2"]
HAT_random = [
    # "M3 MAAWS",
    "PF98",
    "NLAW",
    # "RPG-28",
    "RPG-29",
    "RPG-7",
    # "RPG-7V2",
    "Carl Gustav M2",
    "MK153 SMAW"
]

grenade_random_select = ""
LAT_random_select = ""
HAT_random_select = ""

def get_random():
    grenade_random_select= random.sample(grenade_random, 1)[0]
    LAT_random_select = random.sample(LAT_random, 1)[0]
    HAT_random_select = random.sample(HAT_random, 1)[0]

    weapon_select_grenade.config(text=grenade_random_select)
    weapon_select_LAT.config(text=LAT_random_select)
    weapon_select_HAT.config(text=HAT_random_select)

root = tk.Tk()
root.title("Post Assessment Toolkit")

icon = open("gui_icon.ico", "wb+")
icon.write(base64.b64decode(img))  # 写入到临时文件中
icon.close()
root.iconbitmap("gui_icon.ico")  # 设置图标
os.remove("gui_icon.ico")  # 删除临时图标
# root.iconbitmap('logo.ico')

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=5)

frame.grid_columnconfigure(1, minsize=250)
frame.grid_columnconfigure(2, minsize=250)
frame.grid_columnconfigure(3, minsize=250)

in_line_distance = 7
title_font = 14
content_font = 10

# Grenade
grenade_label = tk.Label(frame, text=weapon_description_label[0], font=title_font, pady=in_line_distance)
grenade_label.grid(row=0, column=0)
# Required: A B C
grenade_must_label = tk.Label(frame, text="Required", font=content_font, pady=in_line_distance)
grenade_must_label.grid(row=1, column=0)
grenade_0 = tk.Label(frame, text=grenade_must[0], font=content_font)
grenade_0.grid(row=1, column=1)
grenade_1 = tk.Label(frame, text=grenade_must[1], font=content_font)
grenade_1.grid(row=1, column=2)
grenade_2 = tk.Label(frame, text=grenade_must[2], font=content_font)
grenade_2.grid(row=1, column=3)
grenade_random_label = tk.Label(frame, text="Random", font=content_font, pady=in_line_distance)
grenade_random_label.grid(row=2, column=0)
weapon_select_grenade = tk.Label(frame, text=grenade_random_select, font=content_font)
weapon_select_grenade.grid(row=2, column=1)
separator = ttk.Separator(frame, orient='horizontal')
separator.grid(row=3, column=0, columnspan=4, sticky="ew")

# LAT
LAT_label = tk.Label(frame, text=weapon_description_label[1], font=title_font, pady=in_line_distance)
LAT_label.grid(row=4, column=0)
# Required: A B C
LAT_must_label = tk.Label(frame, text="Required", font=content_font, pady=in_line_distance)
LAT_must_label.grid(row=5, column=0)
LAT_0 = tk.Label(frame, text=LAT_must[0], font=content_font)
LAT_0.grid(row=5, column=1)
LAT_1 = tk.Label(frame, text=LAT_must[1], font=content_font)
LAT_1.grid(row=5, column=2)
LAT_2 = tk.Label(frame, text=LAT_must[2], font=content_font)
LAT_2.grid(row=5, column=3)
LAT_random_label = tk.Label(frame, text="Random", font=content_font, pady=in_line_distance)
LAT_random_label.grid(row=6, column=0)
weapon_select_LAT = tk.Label(frame, text=LAT_random_select, font=content_font)
weapon_select_LAT.grid(row=6, column=1)
separator = ttk.Separator(frame, orient='horizontal')
separator.grid(row=7, column=0, columnspan=4, sticky="ew")

# HAT
HAT_label = tk.Label(frame, text=weapon_description_label[2], font=title_font, pady=in_line_distance)
HAT_label.grid(row=8, column=0)
# Required: A B C
HAT_must_label = tk.Label(frame, text="Required", font=content_font, pady=in_line_distance)
HAT_must_label.grid(row=9, column=0)
HAT_0 = tk.Label(frame, text=HAT_must[0], font=content_font)
HAT_0.grid(row=9, column=1)
HAT_1 = tk.Label(frame, text=HAT_must[1], font=content_font)
HAT_1.grid(row=9, column=2)
HAT_2 = tk.Label(frame, text=HAT_must[2], font=content_font)
HAT_2.grid(row=9, column=3)
HAT_random_label = tk.Label(frame, text="Random", font=content_font, pady=in_line_distance)
HAT_random_label.grid(row=10, column=0)
weapon_select_HAT = tk.Label(frame, text=HAT_random_select, font=content_font)
weapon_select_HAT.grid(row=10, column=1)

button = tk.Button(root, text="Get Equipments", command=get_random)
button.pack(pady=10)

root.mainloop()