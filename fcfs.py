from threading import *

import time

# Número de procesos
N = 4

# ID de proceso
pids = [0] * N

# Tiempos de llegada
arrival_times = [ 2, 4, 0, 5];

# Tiempo de procesamiento
burning_times = [ 1, 2, 4, 5];

# historial id
id = 0

class ExecutorThread(Thread):
    def run(self):
        while True:
            if(len(pids)== 0):
                break
            
            orderProcessesByArrivalTime()
            index = getNextProcessToExecute()
            print ("\nEjecutando un nuevo proceso.\n")

            time.sleep(burning_times[index]) 
            global N
            N = N - 1 

            print("ids: ", pids)
            
            print("\nEl proceso con id ", pids[index], " ha sido ejecutado.")
            
            pids.pop(index)
            arrival_times.pop(index)
            burning_times.pop(index)
            
            
        print("Todos los procesos han sido ejecutados")        

class MenuThread(Thread):
    def run(self):
        while(True):
            print("\n¿Añadir proceso? \n")
            op = str(input("1. y \n2. n\n=>"))
            
            if(op  == "y"):
                print("\n===========================Nuevo Proceso============================")
                arrival_time = int(input("Ingrese el tiempo de llegada: "))
                burning_time = int(input("Ingrese el tiempo de procesamiento: "))
                addProcess(arrival_time, burning_time)
    
            CalcularTiempoDeEsperaPromedio(pids, arrival_times, burning_times)
            


def CalcularTiempoDeEsperaPromedio(pids, arrival_times, burning_times):
    # tiempo de espera, array vacio
    waitingTimes = [0]*N;

    # El tiempo de espera del primer proceso se inicizaliza en 0
    waitingTimes[0] = 0;

    print("P.No ", "Tiempo de llegada\t" , "Tiempo de procesamiento", "Tiempo de espera");
    print(pids[0] , "\t\t" , arrival_times[0] , "\t\t" , burning_times[0] , "\t\t" , waitingTimes[0]);
    #wt[i] = (at[i - 1] + bt[i - 1] + wt[i - 1]) - at[i];
    
    # Se calcula el tiempo de espera de los procesos
    for i in range(1, N):	
        waitingTimes[i] = (arrival_times [i - 1] + burning_times[i-1] + waitingTimes[i-1]) - arrival_times [i - 1] 
        print(pids[i] , "\t\t" , arrival_times[i] , "\t\t" , burning_times[i] , "\t\t" , waitingTimes[i])     

    # Promedio
    average = 0.0;
    sum = 0;

    # Se suman todos los tiempos de espera
    for i in range(0, N):
        sum = sum + waitingTimes[i];
    
    # Se halla el promedio de tiempo de espera diviendo la suma para el nim de proceso
    average = sum / N;

    print("Tiempo de espera promedio: = " , average);


def addProcess(arrival_time, burning_time):
    global N
    N = N + 1
    pids.append(giveID())
    arrival_times.append(arrival_time)
    burning_times.append(burning_time)
    orderProcessesByArrivalTime()
    CalcularTiempoDeEsperaPromedio(pids, arrival_times, burning_times)

def orderProcessesByArrivalTime():
    for i in range(0, N):
        for j in range(1, N):
            if arrival_times[i] < arrival_times[j - 1]:
                swapB = arrival_times[j - 1]
                swapA = arrival_times[i]
                arrival_times[i] = swapB
                arrival_times[j - 1] = swapA
            
def getNextProcessToExecute():        
    return arrival_times.index(min(arrival_times))

def generarIDsIniciales():
    for i in range(0,N):
        pids[i] = i	
    return

def giveID():
    global id
    id = pids[-1] + id
    print ("last id: ", id)
    return id


    
if __name__ == '__main__':
    generarIDsIniciales()
    
    CalcularTiempoDeEsperaPromedio(pids, arrival_times, burning_times)

    executor_thread =  ExecutorThread()
    menu_thread = MenuThread()

    menu_thread.start()
    executor_thread.start()

    menu_thread.join()
    