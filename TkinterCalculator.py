import tkinter as tk
from tkinter import messagebox
import sys

def icon_resource_direct():
    if getattr(sys,"frozen",False):
        path = sys._MEIPASS + "\\assets\\calculator.png"
        return path
    else:
        path = "\\".join(__file__.split("\\")[:-1] + ["\\assets\\calculator.png"])
        return path

icon_file_path = icon_resource_direct()

key = ["%","C","CE","÷",
           "1","2","3","x",
           "4","5","6","-",
           "7","8","9","+",
           "+-","0",".","="]

lable_text = ""

def menu_about():
    messagebox.showinfo(title="关于",message="关于Tkinter-Calculator:\n版本:0.1.0\n作者:Adamo1209")

def calculate(lable_text:str):
    calc_str = lable_text
    for old,new in dict(zip("x÷","*/")).items():
        calc_str = calc_str.replace(old,new)
    try:
        res_str = str(eval(f"float({calc_str})"))
        round_num = (11-len(res_str.split(".")[0]))
        if round_num < 0:
            return "EOE"
        else:
            res_round = str(round(float(res_str),round_num))
            if str(float(res_round.split(".")[0])) == res_round:
                return str(res_round.split(".")[0])
            else:
                return res_round
    except ValueError:
        messagebox.showerror("错误","运算时出现的错误!")
        return ""
    except ZeroDivisionError:
        messagebox.showerror("错误","除数不可为0!")
        return ""

class __key_button_command:
    text_container = None
    lable_container = None
    content = None

    def __init__(self, text_container:tk.Text,content:str,lable_container:tk.Label):
        self.text_container = text_container
        self.content = content
        self.lable_container = lable_container

    def command(self):
        if self.content in list(map(str,range(10))):
            if (self.text_container.get(0.0,tk.END)[0] == "0") and ("." not in self.text_container.get(0.0,tk.END)):
                pass
            else:
                self.text_container.insert(tk.END,self.content)
        elif self.content == ".":
            if ("." in self.text_container.get(0.0,tk.END)) or self.text_container.get(0.0,tk.END) == chr(10):
                pass
            else:
                self.text_container.insert(tk.END,self.content)
        elif self.content == "CE":
            self.text_container.delete(1.0,tk.END)
        elif self.content == "+-":
            text_container_content = self.text_container.get(0.0,tk.END)
            try:
                input_num = float(text_container_content)
                if input_num > 0:
                    self.text_container.insert(0.0,"-")
                elif input_num < 0:
                    self.text_container.delete(0.0)
                else:
                    pass
            except ValueError:
                messagebox.showerror("错误","输入的不是合法数字!")
                self.text_container.delete(0.0,tk.END)
        elif self.content == "%":
            text_container_content = self.text_container.get(0.0,tk.END)
            try:
                input_num = float(text_container_content)
                result_num = input_num/100
                result_num_round = round(result_num,9)
                self.text_container.delete(0.0,tk.END)
                self.text_container.insert(0.0,str(result_num_round))
            except ValueError:
                messagebox.showerror("错误","输入的不是合法数字!")
                self.text_container.delete(0.0,tk.END)
        elif self.content in list("+-x÷"):
            global lable_text
            text_container_content = self.text_container.get(0.0,tk.END)
            try:
                if (lable_text == ""):
                    if (text_container_content.replace(chr(10),"").split(".")[-1] == ""):
                        text_container_content = text_container_content.replace(".","")
                    float(text_container_content.replace(chr(10),""))
                    lable_text += text_container_content.replace(chr(10),"") + self.content
                    self.lable_container.configure(text=lable_text)
                    self.text_container.delete(0.0,tk.END)
                else:
                    if (text_container_content.replace(chr(10),"") == ""):
                        pass
                    else:
                        if all([i not in lable_text for i in "+-x÷"]):
                            lable_text = ""
                            self.lable_container.configure(text=lable_text)
                            if (text_container_content.replace(chr(10),"").split(".")[-1] == ""):
                                text_container_content = text_container_content.replace(".","")
                            float(text_container_content.replace(chr(10),""))
                            lable_text += text_container_content.replace(chr(10),"") + self.content
                            self.lable_container.configure(text=lable_text)
                            self.text_container.delete(0.0,tk.END)
                        else:
                            float(text_container_content.replace(chr(10),""))
                            lable_text += text_container_content.replace(chr(10),"")
                            self.text_container.delete(0.0,tk.END)
                            lable_text = calculate(lable_text) + self.content
                            self.lable_container.configure(text=lable_text)
            except ValueError:
                messagebox.showerror("错误","输入的不是合法数字!")
                self.text_container.delete(0.0,tk.END)
        elif self.content == "C":
            lable_text = ""
            self.lable_container.configure(text=lable_text)
            self.text_container.delete(0.0,tk.END)
        elif self.content == "=":
            text_container_content = self.text_container.get(0.0,tk.END).replace(chr(10),"")
            if any([i in lable_text for i in "+-x÷"]):
                if (text_container_content.split(".")[-1] == "") or (text_container_content == ""):
                    text_container_content += "0"
                try:
                    float(text_container_content)
                    lable_text += text_container_content
                    self.text_container.delete(0.0,tk.END)
                    lable_text = calculate(lable_text)
                    self.lable_container.configure(text=lable_text)
                except ValueError:
                    messagebox.showerror("错误","输入的不是合法数字!")
                    self.text_container.delete(0.0,tk.END)
            else:
                messagebox.showerror("错误","请完善运算表达式")
        else:
            messagebox.showerror("错误","未定义命令!")

def main():
    root = tk.Tk()
    root.title("Tkinter-Calculator")
    root.geometry("300x450")
    root.resizable(False,False)
    root.iconphoto(True,tk.PhotoImage(file=icon_file_path))

    menubar = tk.Menu(root)
    menubar.add_cascade(label="关于",command=menu_about)
    root.config(menu=menubar)
    
    frame_display = tk.Frame(root,background="white",relief='groove',border=5)
    frame_display.pack(padx=1,side="top",fill="x")

    text_up = tk.Label(frame_display,height=1,font=("consolas",20),border=0,background="white")
    text_down = tk.Text(frame_display,height=1,font=("consolas",34),border=0)
    text_up.pack(side="top",anchor="w")
    text_down.pack(side="top",anchor="w")

    frameLabel_input = tk.LabelFrame(root,labelanchor="nw",text="输入",font=("consolas",12))
    frameLabel_input.pack(padx=3,pady=(0,10),side="top",fill="both",expand=True)
    for i in range(5):
        frameLabel_input.rowconfigure(i,weight=1)
    for i in range(4):
        frameLabel_input.columnconfigure(i,weight=1)
    for i,s in enumerate(key):
        tk.Button(frameLabel_input,text=s,font=("consolas",18),width=2,padx=18,pady=10,
                  command=__key_button_command(text_down,s,text_up).command).grid(row=int(i/4),column=int(i%4),sticky="nw")

    root.mainloop()

if __name__ == "__main__":
    print(__file__)
    main()
else:
    print(f">> {__file__}无法作为模块使用")
