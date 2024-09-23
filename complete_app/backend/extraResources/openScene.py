import sys
import os
if os.getcwd().find('AppData\\Local') == -1:
    dev=''
else:
    dev = '/resources'
sys.path.append(os.getcwd()+dev+'/backend/extraResources/sim/')
import sim
def open(path):
    client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)#attempts to connect to coppeliasim
    if client_id!=-1:                                                 #if connect successfully
        sim.simxLoadScene(client_id,path,0,sim.simx_opmode_blocking)  #Load Scene
        print(1)
    else:
        print(0)