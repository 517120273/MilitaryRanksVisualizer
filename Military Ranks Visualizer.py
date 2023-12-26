#116 – 郭艺煊 - Military Ranks Visualizer 
import turtle as t
import tkinter as tk
from tkinter import ttk
import json
import math

class MyApp():
    def __init__(self, root):
        # Initialize the application.
        self.root = root # Store the incoming root object in the instance variable self.root
        self.root.title("Military Ranks Visualizer")
        self.root.geometry("700x420+475+300")
        self.style = ttk.Style(root) # To customizing the appearance of the application
        self.menubar = tk.Menu(self.root)
        self.create_menu()
        self.create_tree()
        self.create_overview()
        self.create_text()
        self.selected_item = None
        self.introduction_label = None

    def create_menu(self):
        # Create the menu bar for the application.
        self.menubar.add_command(label="绘制军衔", command=self.show_tree)
        self.menubar.add_command(label="军衔总览", command=self.show_overview)
        self.menubar.add_command(label="使用说明", command=self.show_explanation)
        self.menubar.add_command(label="关于", command=self.show_about)
        # Configure the menu bar to the root window
        self.root.configure(menu=self.menubar)

    def create_tree(self):
        # Create the treeview for the application.
        self.style.configure("Treeview.Heading", font = ("宋体", 12))
        self.style.configure("Treeview", font = ("宋体", 12))
        self.tree = ttk.Treeview(self.root)
        self.tree.heading("#0", text = "中国人民解放军军衔")
        # Create a Combobox for selecting the branch of the military
        self.branch = tk.StringVar()
        self.branch.set("陆军")  # Default selection is Army.
        self.branch_menu = ttk.Combobox(self.root, textvariable=self.branch, values=["陆军", "海军", "空军"], font=("宋体", 12), width=10) 
        items = {
            "将官": ["上将", "中将", "少将"],
            "校官": ["大校", "上校", "中校", "少校"],
            "尉官": ["上尉", "中尉", "少尉"],
            "士兵": ["军士", "义务兵"],
        }
         # Iterate through the dictionary to create the military rank tree
        for parent, children in items.items():
            parent_item = self.tree.insert("", "end", text=parent)
            for child in children:
                child_item = self.tree.insert(parent_item, "end", text=child)
                # Add a third-level menu.
                grandchild_items = ["一级军士长", "二级军士长", "三级军士长", "一级上士", "二级上士", "中士",
                                    "下士"] if child == "军士" else ["上等兵", "列兵"] if child == "义务兵" else []
                for grandchild in grandchild_items:
                    self.tree.insert(child_item, "end", text=grandchild)
        self.tree.pack()
        self.branch_menu.pack()
        self.draw_button = tk.Button(self.root, text="绘制军衔", command=self.draw_graphics)
        self.draw_button.pack()

    def get_introduction(self, selected_text):
        with open("ranks_introductions.json", "r", encoding = "utf-8")as introduction_file:
            introduction_dict = json.load(introduction_file)
        return introduction_dict.get(selected_text)

    def draw_graphics(self):
        selected_item = self.tree.focus()  # Get the selected rank item
        if selected_item:
            selected_text = self.tree.item(selected_item, "text")
            # Clear the previous introduction text
            if self.introduction_label:
                self.introduction_label.pack_forget()
            # Add introduction text
            introduction_text = self.get_introduction(selected_text)
            self.introduction_label = tk.Label(self.root, text=introduction_text, font=("宋体", 12))
            self.introduction_label.pack()
            # Draw the selected military rank using Turtle graphics.
            self.draw_turtle_graphics(selected_text)

    def draw_turtle_graphics(self, selected_text):
        try:
            t.reset() # Clear the previous Turtle graphics
        except t.Terminator: # If the Turtle graphics window is closed
            t.reset() 

        # Set the Turtle window position and attributes
        t.title("Military Ranks Visualizer")
        t.setup(width=500, height=500, startx=1180)
        t.colormode(255)
        t.speed(1000)

        # Get the selected branch and set color
        branch = self.branch.get()
        color = {"陆军": deep_green, "海军": navy_blue, "空军": airforce_blue}[branch]
        # Define functions for each rank
        ranks = {   "上将": self.上将,"中将": self.中将,"少将": self.少将,
                    "大校": self.大校,"上校": self.上校,"中校": self.中校,"少校": self.少校,
                    "上尉": self.上尉,"中尉": self.中尉,"少尉": self.少尉,
                    "一级军士长": self.一级军士长,"二级军士长": self.二级军士长,"三级军士长": self.三级军士长,
                    "一级上士": self.一级上士,"二级上士": self.二级上士,"中士": self.中士,"下士": self.下士,
                    "上等兵": self.上等兵,"列兵": self.列兵,}
        # Get the drawing function for the selected rank
        selected_function = ranks.get(selected_text)
        # If there's a drawing function for the selected rank, call it with the color parameter
        if selected_function:
            selected_function(color)
                        
    def create_overview(self):
        # Create the overview frame to display the hierarchy of military ranks.
        overview_text = '''（军官军衔，分三等十级）                    （士兵军衔，分四等九级）
                              
                                              （上接军官军衔）   
 - 将官                        - 高级军士             ↓
               - 上将                           - 一级军士长   
                  ↓                                  ↓
    ↓        - 中将                ↓   -军士长 - 二级军士长
                  ↓                                  ↓
               - 少将                           - 三级军士长            
                  ↓                                  ↓              
- 校官                         - 中级军士         
               - 大校                           - 一级上士
                  ↓               ↓   - 上士        ↓
    ↓         - 上校                            - 二级上士
                  ↓                                  ↓
               - 中校          - 初级军士                      
                  ↓                               - 中士
               - 少校                                 ↓
                  ↓               ↓               - 下士
- 尉官                                                ↓        
               - 上尉          - 义务兵                    
                  ↓                              - 上等兵     
    ↓         - 中尉                                 ↓
                  ↓                               - 列兵
               - 少尉 
                  ↓
（士兵）     （后接士兵军衔）
    '''
        self.overview_frame = tk.Frame(root)
        tk.Label(self.overview_frame, text=overview_text, justify=tk.LEFT, font=("宋体", 11)).pack()

    def create_text(self):
        # Create the about frame for displaying text.
        self.about_frame = tk.Frame(root)
        tk.Label(self.about_frame, text="\n关于作者：本作品由116郭艺煊制作", justify=tk.LEFT, wraplength=400, font=("宋体", 15)).pack()
        tk.Label(self.about_frame, text="\n关于作品：本作品使用tkinter、turtle制作", justify=tk.LEFT, wraplength=400, font=("宋体", 15)).pack()

        # Create the explanation frame.
        self.explanation_frame = tk.Frame(root)
        atext = """
    使用说明：
    1. 从菜单中选择一个军衔，并且在在“绘制军衔”按钮上方的下拉菜单中选择军种。
    2. 点击“绘制军衔”按钮，使用Turtle可视化所选军衔。
    3. 在军衔绘制的同时，在按钮下方会展示该军衔所对应简介。
    4. 点击“军衔总览”查看所有军衔的层次结构。

    注意：
    选择一个军衔后，点击“绘制军衔”按钮，Turtle图形可能需要一些时间才能出现。
    """
        tk.Label(self.explanation_frame, text=atext, justify=tk.LEFT, wraplength=400, font=("宋体", 15)).pack()

    def show_content(self, content_frame):
        # Hide other content
        self.about_frame.pack_forget()
        self.explanation_frame.pack_forget()
        self.tree.pack_forget()
        self.draw_button.pack_forget()
        self.overview_frame.pack_forget()
        self.branch_menu.pack_forget()
        self.clear_introduction_label()

        # Display the specified content
        content_frame.pack()

    def show_tree(self):
        self.show_content(self.tree)
        self.branch_menu.pack()
        self.draw_button.pack()

    def show_overview(self):
        self.show_content(self.overview_frame)

    def show_explanation(self):
        self.show_content(self.explanation_frame)

    def show_about(self):
        self.show_content(self.about_frame)

    def clear_introduction_label(self):       
        if self.introduction_label: # Checks whether the label exists
            self.introduction_label.pack_forget()
            self.introduction_label = None

    def 上将(self, color):
        self.draw_template(color)
        self.star(25, -51, -195 + 27 * s)
        self.star(25, -51, -195 + 39 * s)
        self.star(25, -51, -195 + 51.5 * s)
        self.麦穗(-51, -195 + 5 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 中将(self, color):
        self.draw_template(color)
        self.star(25, -51, -195 + 31 * s)
        self.star(25, -51, -195 + 47 * s)
        self.麦穗(-51, -195 + 5 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 少将(self, color):
        self.draw_template(color)
        self.star(25, -51, -195 + 39 * s)
        self.麦穗(-51, -195 + 5 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 大校(self, color):
        self.draw_template(color)
        self.draw_line(-55, -195, yellow)
        self.draw_line(-100 + 33 * s - 45, -195, yellow)
        self.star(25, -51, -195 + 14 * s)
        self.star(25, -51, -195 + 14 * s + 12 * s)
        self.star(25, -51, -195 + 14 * s + 24 * s)
        self.star(25, -51, -195 + 14 * s + 36 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 上校(self, color):
        self.draw_template(color)
        self.draw_line(-55, -195, yellow)
        self.draw_line(-100 + 33 * s - 45, -195, yellow)
        self.star(25, -51, -195 + 17 * s)
        self.star(25, -51, -195 + 17 * s + 15 * s)
        self.star(25, -51, -195 + 17 * s + 15 * s + 15 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 中校(self, color):
        self.draw_template(color)
        self.draw_line(-55, -195, yellow)
        self.draw_line(-100 + 33 * s - 45, -195, yellow)
        self.star(25, -51, -195 + 21 * s)
        self.star(25, -51, -195 + 42 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 少校(self, color):
        self.draw_template(color)
        self.draw_line(-55, -195, yellow)
        self.draw_line(-100 + 33 * s - 45, -195, yellow)
        self.star(25, -51, -195 + 32 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 上尉(self, color):
        self.draw_template(color)
        self.draw_line(-98 + 16 * s, -195, yellow)
        self.star(25, -51, -195 + 17 * s)
        self.star(25, -51, -195 + 17 * s + 15 * s)
        self.star(25, -51, -195 + 17 * s + 15 * s + 15 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 中尉(self, color):
        self.draw_template(color)
        self.draw_line(-98 + 16 * s, -195, yellow)
        self.star(25, -51, -195 + 21 * s)
        self.star(25, -51, -195 + 42 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)
    
    def 少尉(self, color):
        self.draw_template(color)
        self.draw_line(-98 + 16 * s, -195, yellow)
        self.star(25, -51, -195 + 32 * s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 一级军士长(self, color):
        self.draw_template(color)
        self.angle(4.7, -100 + 3.5 * s, -200+11.5*s)
        self.angle(4.7, -100 + 3.5 * s, -200+18.5*s)
        self.angle(4.7, -100 + 3.5 * s, -200+25.5*s)
        self.angle(2.5, -100 + 3.5 * s, -200+32.5*s)
        self.gun(175, 20)
        self.gun2(175, 20, color)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 二级军士长(self, color):
        self.draw_template(color)
        self.angle(4.7, -100 + 3.5 * s, -200+11.5*s)
        self.angle(4.7, -100 + 3.5 * s, -200+18.5*s)
        self.angle(4.7, -100 + 3.5 * s, -200+25.5*s)
        self.gun(175, 20)
        self.gun2(175, 20, color)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 三级军士长(self, color):
        self.draw_template(color)
        self.angle(4.7, -100 + 3.5 * s, -200+11.5*s)
        self.angle(4.7, -100 + 3.5 * s, -200+18.5*s)
        self.angle(2.5, -100 + 3.5 * s, -200+25.5*s)
        self.gun(175, 25)
        self.gun2(175, 25, color)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 一级上士(self, color):
        self.draw_template(color)
        self.angle(4.7, -100 + 3.5 * s, -200+11.5*s)
        self.angle(4.7, -100 + 3.5 * s, -200+18.5*s)
        self.gun(175, 35)
        self.gun2(175, 35, color)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 二级上士(self, color):
        self.draw_template(color)
        self.angle(5, -100 + 3.5 * s, -200+11.5*s)
        self.angle(2.5, -100 + 3.5 * s, -200+13.5*s)
        self.gun(175, 80)
        self.gun2(175, 80, color)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 中士(self, color):
        self.draw_template(color)
        self.angle(5, -100 + 3.5 * s, -200+11.5*s)
        self.gun(175, 80)
        self.gun2(175, 80)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 下士(self, color):
        self.draw_template(color)
        self.angle(2.5, -100 + 3.5 * s, -200+11.5*s)
        self.gun(175, 80)
        self.gun2(175, 80, color)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 上等兵(self, color):
        self.draw_template(color)
        self.angle(2.5, -100 + 3.5 * s, -200+11.5*s)
        self.angle(2.5, -100 + 3.5 * s, -200+17*s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def 列兵(self, color):
        self.draw_template(color)
        self.angle(2.5, -100 + 3.5 * s, -200+11.5*s)
        self.draw_circle(9 * s / 2, -50 + 9 * s, -195 + 17 * s + 15 * s + 15 * s + 15 * s + 13 * s)

    def draw_template(self, color):
        # Draw the template of the military rank.
        s = 5
        t.pencolor(color)
        t.penup() 
        t.goto(-100, -200)
        t.pendown() 
        t.begin_fill()
        t.forward(33 * s)
        t.seth(91)
        t.forward(75 * s)
        t.seth(148)
        t.forward(18 * s)
        t.seth(32)
        t.backward(18 * s)
        t.seth(89)
        t.backward(75 * s)
        t.hideturtle()
        t.fillcolor(color)
        t.end_fill()
        t.up()
    
    def draw_line(self, x, y, color):
        t.pencolor(color)
        t.pensize(10)
        t.goto(x, y)
        t.down()
        t.seth(90)
        t.forward(62 * s)
        t.up()

    def star_angle(self, x):
        t.pencolor(yellow)
        t.forward(x)
        t.left(72)
        t.forward(x)

    def star(self, x, y, z):
        t.goto(y, z)
        t.pensize(1)
        t.pencolor(yellow)
        t.begin_fill()
        t.down()
        t.seth(0)
        self.star_angle(x)
        t.seth(288)
        self.star_angle(x)
        t.seth(216)
        self.star_angle(x)
        t.seth(144)
        self.star_angle(x)
        t.seth(72)
        self.star_angle(x)
        t.fillcolor(yellow)
        t.end_fill()
        t.up()

    def 麦穗(self, n, m): 
        # Initialize data list and the number of points to draw
        data = []
        points = 100
        # Read Fourier series data from a file
        f = open("data.txt", "r")
        for line in f:
            line = eval(line)
            data.append(line)
        # Set the number of Fourier series terms, add 1 because it includes the DC component
        N = len(data) + 1
        x = [0] * N
        y = [0] * N
        # Draw the graph based on Fourier series data
        t.goto(m, n)
        t.penup()
        t.pencolor(yellow)
        t.pensize(2)
        t.begin_fill()
        for j in range(points):
            for i in range(len(data)):
                # Calculate each component of the Fourier series
                if i % 2 == 0:
                    x[i] = data[i][0] * math.cos(i / points * 3.14 * j) - data[i][1] * math.sin(i / points * 3.14 * j)
                    y[i] = data[i][0] * math.sin(i / points * 3.14 * j) + data[i][1] * math.cos(i / points * 3.14 * j)
                else:
                    x[i] = data[i][0] * math.cos(-(i+1) / points * 3.14 * j) - data[i][1] * math.sin(-(i+1) / points * 3.14 * j)
                    y[i] = data[i][0] * math.sin(-(i+1) / points * 3.14 * j) + data[i][1] * math.cos(-(i+1) / points * 3.14 * j)
            # Move the Turtle to the calculated coordinates and draw
            t.goto(int(sum(x))+175, -int(sum(y)+80)) 
            t.pendown()
        t.end_fill()
        t.penup()

    def gun(self, m, n):
        # Initialize data list and the number of points to draw
        data = []
        points = 1200
      # Read Fourier series data from a file
        f = open("data1.txt","r")
        for line in f:
            line = eval(line)
            data.append(line)
      # Set the number of Fourier series terms, add 1 because it includes the DC component
        N = len(data) + 1
        x = [0] * N
        y = [0] * N
      # Draw the graph based on Fourier series data
        t.penup()
        t.pencolor(yellow)
        t.pensize(2)
        t.begin_fill()
        for j in range(points):
            for i in range(len(data)):
            # Calculate each component of the Fourier series
                if i % 2 == 0:
                    x[i] = data[i][0] * math.cos(i / points * 3.14 * j) - data[i][1] * math.sin(i / points * 3.14 * j)
                    y[i] = data[i][0] * math.sin(i / points * 3.14 * j) + data[i][1] * math.cos(i / points * 3.14 * j)
                else:
                    x[i] = data[i][0] * math.cos(-(i+1) / points * 3.14 * j) - data[i][1] * math.sin(-(i+1) / points * 3.14 * j)
                    y[i] = data[i][0] * math.sin(-(i+1) / points * 3.14 * j) + data[i][1] * math.cos(-(i+1) / points * 3.14 * j )
         # Move the Turtle to the calculated coordinates and draw
            t.goto(int(sum(x))+m, -int(sum(y)+n))
            t.pendown()
        t.end_fill()
        t.up()
    
    def gun2(self, m, n, color):
        # Initialize data list and the number of points to draw
        data = []
        points = 200
      # Read Fourier series data from a file
        f = open("data2.txt","r")
        for line in f:
            line = eval(line)
            data.append(line)
      # Set the number of Fourier series terms, add 1 because it includes the DC component
        N = len(data) + 1 
        x = [0] * N
        y = [0] * N
      # Draw the graph based on Fourier series data
        t.penup()
        t.pencolor(color)
        t.pensize(2)
        t.begin_fill() 
        for j in range(points):
            for i in range(len(data)):
            # Calculate each component of the Fourier series
                if i % 2 == 0:
                    x[i] = data[i][0] * math.cos(i / points * 3.14 * j) - data[i][1] * math.sin(i / points * 3.14 * j)
                    y[i] = data[i][0] * math.sin(i / points * 3.14 * j) + data[i][1] * math.cos(i / points * 3.14 * j)
                else:
                    x[i] = data[i][0] * math.cos(-(i+1) / points * 3.14 * j) - data[i][1] * math.sin(-(i+1) / points * 3.14 * j)
                    y[i] = data[i][0] * math.sin(-(i+1) / points * 3.14 * j) + data[i][1] * math.cos(-(i+1) / points * 3.14 * j)
         # Move the Turtle to the calculated coordinates and draw
            t.goto(int(sum(x))+m, -int(sum(y)+n))
            t.pendown()
        t.fillcolor(color)
        t.end_fill()
        t.up()
        
    def angle(self, l, x, y):
        t.goto(x, y)
        t.pensize(1)
        t.pencolor(yellow)
        t.begin_fill()
        t.down()
        t.seth(-25)
        t.forward(14*s)
        t.seth(25)
        t.forward(14*s)
        t.seth(90)
        t.forward(l*s)
        t.seth(-155)
        t.forward(14*s)
        t.seth(155)
        t.forward(14*s)
        t.seth(270)
        t.forward(l*s)
        t.fillcolor(yellow)
        t.end_fill()
        t.up()

    def draw_circle(self, r, x, y):
        t.goto(x, y)
        t.seth(144)
        t.begin_fill()
        t.circle(r)
        t.fillcolor(yellow)
        t.end_fill()
        t.mainloop()

if __name__ == "__main__":
    deep_green = (35, 46, 35)
    navy_blue = (32, 38, 44)
    airforce_blue = (26, 48, 68)
    yellow = (236, 199, 16)
    s = 5
    # Create a Tkinter root window
    root = tk.Tk()
    # Create an instance of the MyApp application, passing the root window
    app = MyApp(root)
    # Enter the Tkinter event loop, waiting for user interaction
    root.mainloop()