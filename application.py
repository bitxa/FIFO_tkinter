import tkinter as tk
from threading import Thread
from tkinter import *

# ROOT WINDOW CONFIGURATION
root_window = tk.Tk()
root_window.title("FIFO (FIRST IN FIRST OUT)")
root_window.geometry('1920x1080')

#helpers
processes = list()
center_coordinates = int(root_window.winfo_screenwidth()/2), int(root_window.winfo_screenheight()/2)
last_x_position = 30
last_y_position = center_coordinates [1] -50



class Application(Thread):
    
    # Widgets
    title_label = Label(root_window, width = center_coordinates[1], height= 1, text = "FIFO")
    title_label.config(bg="#B2B2B2", font=("Verdana, sans-serif", 50), fg="#FFFFFF")
    horizontal_scrollbar = Scrollbar(root_window, orient = 'horizontal')
    horizontal_scrollbar.config(command=root_window.xview)
    
        
    def run(self): 
        self.title_label.pack(anchor=CENTER)
        self.horizontal_scrollbar.pack(side = BOTTOM, fill = X)
        
        #pruebas
        for i in range(0, 10):
            processBox = addProcessBox(1, 2,3)
            processBox.arrival_time_text.pack()
            processes.append(processBox)

        #emptyProcesses(processes)
  
            

        
class ProcessBox(Widget):
    def __init__(self, root_window, process, x, y):
        self.process = process

        self.box = LabelFrame(root_window, text="Process " + str(self.process.process_id), bg = "black", 
                              fg = "white", font=("Verdana, sans-serif", 35))
        self.box.place(x = x, y = y)      

        self.arrival_time_text  = Label(self.box, text="Arrival time: " + str(self.process.arrival_time) +
                                        "\nBurning time: " + str(self.process.burning_time), fg="black")
    
    def delete(self):
        self.arrival_time_text.destroy()
        self.box.pack_forget()
            
class Process():
    def __init__(self, process_id, arrival_time, burning_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burning_time = burning_time



def addProcessBox(id, arrival_time, burning_time):
    
    global last_x_position, last_y_position
    
    process_box = ProcessBox(root_window, Process(id, arrival_time, burning_time),
                              last_x_position, last_y_position)
    last_x_position += 300 

    return process_box

def loadProcesses(processes_info):
    for i in processes_info:
        print("a")
        
        
       

def main():
    if __name__ == '__main__':
        app = Application()
        app.start()
        root_window.mainloop()

def emptyProcesses(processes):
    for i in range(0, len(processes)):
        processBox = processes[i]
        processBox.box.place_forget()
        processBox.arrival_time_text.pack_forget()  
          
    processes.clear()

main()      
        
        

