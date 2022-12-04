import tkinter as tk
from functools import partial
from threading import Thread
from tkinter import *
import time

# historial id
last_id = 0
processes = list()

# ROOT WINDOW CONFIGURATION
root_window = tk.Tk()
root_window.title("FIFO (FIRST IN FIRST OUT)")
root_window.geometry('1920x1080')
root_window.config(bg="#FEBE8C")
center_coordinates = int(root_window.winfo_screenwidth() / 2), int(root_window.winfo_screenheight() / 2)
last_x_position, last_y_position = 30,center_coordinates[1] - 20
arrival_time_input, burst_time_input = Entry(), Entry()

arrival_time_input_var, burst_time_input_var = tk.IntVar(root_window), tk.IntVar(root_window)

class Application(Thread):
    # Widgets
    title_label = Label(root_window, width=center_coordinates[1], height=1, text="FIFO")
    title_label.config(bg="#B2B2B2", font=("Verdana, sans-serif", 50), fg="#FFFFFF")
    # New process box info
    new_process_box = LabelFrame(root_window, bg="#DEBACE", width=600, height=200,
                                 text="Nuevo proceso:", font="Helvetica 18 bold")

    arrival_time_input_label = Label(new_process_box, text="Arrival time:", bg="#DEBACE", 
                                     font=("Verdana, sans-serif", 15))
    burst_time_input_label = Label(new_process_box, text="Burning time", bg="#DEBACE",
                                     font=("Verdana, sans-serif", 15))
    
    info_box = LabelFrame(root_window, bg="#8CE60E", width=500, height= 200)
    
    arrival_time_average_label = Label(info_box, bg="#8CE60E", text="Average arrival time: ")
    turn_around_time_average_label = Label(info_box, bg="#8CE60E", text="Arrival turn around time: ")
    arrival_time_average_result= Label(info_box, bg="#8CE60E", text="0")
    turn_around_time_average_result = Label(info_box, bg="#8CE60E", text="0")
    

    
    arrival_time_input = Entry(new_process_box, textvariable=arrival_time_input_var)
    burst_time_input = Entry(new_process_box, textvariable=burst_time_input_var)
    add_button = Button(new_process_box, text='Add process', command=lambda:add_process(get_input_value(arrival_time_input_var),
                                                                                          get_input_value(burst_time_input_var)))

    def run(self):
        self.title_label.pack(anchor=CENTER)
        self.new_process_box.pack(padx=20, pady=30)
        self.info_box.place(x=0, y=90)
        self.arrival_time_average_label.grid(row=1, padx=20, pady=30)
        self.turn_around_time_average_label.grid(row=2, padx=20, pady=30)
        self.turn_around_time_average_result.grid(row=1, column=1, padx=20, pady=30)
        self.arrival_time_average_result.grid(row=2, column=1, padx=20, pady=30)
        
        self.arrival_time_input_label.grid(row=1, padx=20, pady=30)
        self.burst_time_input_label.grid(row=2, padx=20, pady=30)
        self.arrival_time_input.grid(row=1, column=1, padx=20, pady=30)
        self.burst_time_input.grid(row=2, column=1, padx=20, pady=30)
        self.add_button.grid(row=3, column=2, sticky=W, pady=10)
        
        while(True):
            print("processes:len(processes): ", len(processes))
            show_run_info(processes)             
            serve_process()


class ProcessBox(Widget):
    def __init__(self, root_window, process, x, y):
        self.process = process
        self.box = LabelFrame(root_window, text="Process " + str(self.process.process_id), bg="black",
                              fg="white", font=("Verdana, sans-serif", 35))
        self.box.place(x=x, y=y)
        
        self.arrival_time_text = Label(self.box, text="Arrival time: " + str(self.process.arrival_time) +
                                                      "\nBurning time: " + str(self.process.burst_time), fg="black")
        self.arrival_time_text.pack()

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time

def calc_waiting_time(processes):
    waiting_time_array = [0] * len(processes) 
    burst_time = processes[0].process.burst_time
        
    for i in range(1, len(processes)):  
        waiting_time_array[i] = burst_time + waiting_time_array[i - 1]
        burst_time = processes[i-1].process.burst_time

    return waiting_time_array

def calc_turn_around_time(processes):
    turn_around_array_time = [0]* len(processes)
    waiting_time_array = calc_waiting_time(processes)
    
    for i in range(0, len(processes)):
        burst_time = processes[i].process.burst_time
        turn_around_array_time[i] = burst_time + waiting_time_array[i]
    
    return turn_around_array_time
        
def show_run_info(processes):
    if(len(processes) == 0):
        return
    
    waiting_time_array = calc_waiting_time(processes)
    turn_around_time_array = calc_turn_around_time(processes)
    total_waiting_time = 0
    total_turn_around_time = 0
    for i in range(0, len(processes)):
        total_waiting_time = total_waiting_time + waiting_time_array[i]
        total_turn_around_time = total_turn_around_time + turn_around_time_array[i]
    app.arrival_time_average_result.config(text=str(total_waiting_time/2))
    app.turn_around_time_average_result.config(text=str(total_turn_around_time/2))

def add_example_processes():
    # Tiempos de llegada
    arrival_times = [2, 4, 0]
    # Tiempo de procesamiento
    burst_times = [5, 3, 5]
    
    for i in range(0, 3):
        add_process(arrival_times[0], burst_times[i])

def get_input_value(input_var):
    return input_var.get()

def check_arrival_time(arrival_time):
    if get_arrival_times_as_array().__contains__(arrival_time):
        arrival_time += 1
        return check_arrival_time(arrival_time)
    return arrival_time

def add_process(arrival_time, burst_time):    
    arrival_time = check_arrival_time(arrival_time)
    global last_id
    last_id += 1
    processBox = create_process_box(last_id, arrival_time, burst_time)
    processes.append(processBox)
    reorder_processes()
    
def create_process_box(id, arrival_time, burst_time):
    global last_x_position, last_y_position
    process_box = ProcessBox(root_window, Process(id, arrival_time, burst_time),
                             last_x_position, last_y_position)
    return process_box

def serve_process():
    if(len(processes) == 0):
        return    
    current_process_index = get_next_process_to_exec()
    current_process = processes[current_process_index]
    time.sleep(current_process.process.burst_time)
    current_process.box.place_forget()
    current_process.arrival_time_text.pack_forget()
    processes.pop(current_process_index)
    reorder_processes()
    
    
def reorder_processes():
    x_coordinate = 100
    for i in range(len(processes)):
        processes[i].box.place(x=x_coordinate, y=last_y_position)
        x_coordinate += 280


def get_next_process_to_exec():  
    processes_to_check = get_arrival_times_as_array()
    return processes_to_check.index(min(processes_to_check, default=0))
        
def get_arrival_times_as_array():
    processes_to_check = []
    for i in range(0, len(processes)):
        current = processes[i].process.arrival_time
        processes_to_check.append(current)
    return processes_to_check

def main():
    global app
    app = Application()
    add_example_processes()
    app.start()
    root_window.mainloop()

if __name__ == '__main__':
    main()
    
    