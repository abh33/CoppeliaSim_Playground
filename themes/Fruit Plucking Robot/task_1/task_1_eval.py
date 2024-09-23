import sim
import time
import random
import sys
import os
print(os.getcwd())
#sheet_path = os.getcwd()+'/resources/backend/extraResources/push_to_sheet/'
#sys.path.append(sheet_path)
#import push_to_sheet
# import os
# import numpy as np
# import cv2
sim.simxFinish(-1) # just in case, close all opened connections
client_id = sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim

if client_id==-1:
    print('[Error] Make sure to open scene before Evaluation.')
else:
    print('Evaluation Started...')
    #POSITION POSITION OBJECTS CORRECTLY
    returnCode,vs=sim.simxGetObjectHandle(client_id,'/Vision_sensor',sim.simx_opmode_blocking)
    returnCode,block=sim.simxGetObjectHandle(client_id,'/Cuboid',sim.simx_opmode_blocking)

    returnCode=sim.simxSetObjectPosition(client_id,vs,-1,[0,-1.2050,0.52500],sim.simx_opmode_oneshot)
    returnCode=sim.simxSetObjectPosition(client_id,block,-1,[0,0.245,0.525],sim.simx_opmode_oneshot)

    #REMOVE ALL EXTRA OBJECTS
    returnCode,last_handle=sim.simxGetObjectHandle(client_id,'./last_handle',sim.simx_opmode_blocking)
    for i in range(last_handle+1,last_handle+200):
        returnCode=sim.simxRemoveObject(client_id,i,sim.simx_opmode_blocking)
        if returnCode>0:
            break
        print(i)


    #INITIALISATION
    seqno= random.randint(1,6)

    if seqno==1:
        seq=[2,4, 5, 1, 2, 3, 4, 1 ,5, 2, 5 ,1, 3, 2, 1] #where 1=orange(1,0.64,0), 2=green(0,1,0), 3=lightblue(0,1,1), 4=lavender(1,0.75,1), 5=black(0,0,0)
    elif seqno==2: #orange=4, green=4
        seq=[ 3, 1, 2, 4, 1 ,5, 2, 4,1, 5,2, 3,5 ,1 , 2]
    elif seqno==3:
        seq=[ 2,3, 5,2,  3, 1,5 ,1, 2, 4, 1 ,5, 2, 4,1 ]
    elif seqno==4:
        seq=[ 1 ,3,2,  4, 1 ,4,1, 3,5, 2,  5,2, 1,5, 2]
    else:
        seq=[2, 5, 1,2, 3, 5, 2,  1, 4, 1, 3, 4, 1 ,5, 2]

    #print(seqno, seq)

    emptybuff = bytearray()
    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_oneshot)
    correctlyDetected_orange=0
    correctlyDetected_green=0
    correctlyDetected_unknown=0
    penalties=0

    #START THE SIMULATION
    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
    sim.simxGetPingTime(client_id)
    if (return_code == sim.simx_return_novalue_flag) or (return_code == sim.simx_return_ok):
        print('\nSimulation started correctly in CoppeliaSim.')
    else:
        print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
        print('start_simulation function is not configured correctly, check the code!')
        print()


    #LOOP
    for element in seq:
        #print('in loop for', element)

        #set color
        sim.simxCallScriptFunction(
            client_id, "last_handle", sim.sim_scripttype_childscript, 'change_color', [element],[],[],emptybuff, sim.simx_opmode_blocking)

        #wait for signal
        startTime= time.time()

        #reset response received tag
        responseReceived=False
        
        while (time.time()-startTime)<1:
            return_code, string=sim.simxGetStringSignal(client_id,'colorDetected',sim.simx_opmode_blocking)
            detected= string.decode('utf-8')
            
            if detected== 'waiting':
                continue

            elif (detected== 'orange' and responseReceived==False):
                if element==1:
                    correctlyDetected_orange+=1
                    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_blocking)
                else:
                    penalties+=1
                    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_blocking)
                    print('penalty. correct ans=',element,'ur ans=',detected)

                responseReceived=True

            elif (detected== 'green' and responseReceived==False):
                if element==2:
                    correctlyDetected_green+=1
                    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_blocking)
                else:
                    penalties+=1
                    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_blocking)
                    print('penalty. correct ans=',element,'ur ans=',detected)

                responseReceived=True

            elif (detected== 'unknown' and responseReceived==False):
                if ((element==3) or (element==4) or (element==5)):
                    correctlyDetected_unknown+=1
                    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_blocking)
                else:
                    penalties+=1
                    sim.simxSetStringSignal(client_id,'colorDetected','waiting',sim.simx_opmode_blocking)
                    print('penalty. correct ans=',element,'ur ans=',detected)

                responseReceived=True

            else:
                continue
        
        #check if response was received this time
        if responseReceived==False:
            penalties+=1
    score = (15-penalties)*100/15

    #PRINT RESULTS
    print('correctly detected orange=', correctlyDetected_orange)
    print('correctly detected green=', correctlyDetected_green)
    print('correctly detected unknown=', correctlyDetected_unknown)
    print('penalties=', penalties)
    print("score=", int(score))
    task_data_dict = {}
    task_data_dict['correctly detected orange']= correctlyDetected_orange
    task_data_dict['correctly detected green']= correctlyDetected_green
    task_data_dict['correctly detected unknown']= correctlyDetected_unknown
    data = ['Task 1: DETECTION']
    data.append(str(task_data_dict))
    data.append(str(score))
    #push_to_sheet.send_to_sheets(data)
    #STOP SIMULATION
    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)
    if (return_code == sim.simx_return_novalue_flag) or (return_code == sim.simx_return_ok):
        print('\nSimulation stopped correctly.')
    else:
        print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
        print('[ERROR] stop_simulation function is not configured correctly, check the code!')
        print('Stop the CoppeliaSim simulation manually.')

    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(client_id)
    # Now close the connection to CoppeliaSim:
    sim.simxFinish(client_id)
    #print('connection ended')
