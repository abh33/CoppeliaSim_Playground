import sim
import time
import random
import os
import sys
print(os.getcwd())
#sheet_path = os.getcwd()+'/resources/backend/extraResources/push_to_sheet/'
#sys.path.append(sheet_path)
#import push_to_sheet
#import numpy as np
#import cv2
from pluck_eval import check_berry_status
score = 0
sim.simxFinish(-1) # just in case, close all opened connections
client_id = sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
if client_id==-1:
    print('[Error] Make sure to open scene before Evaluation.')
else:
    #POSITION POSITION OBJECTS CORRECTLY
    returnCode,fs1=sim.simxGetObjectHandle(client_id,'/wall/ForceSensor[0]',sim.simx_opmode_blocking)
    returnCode,fruit1=sim.simxGetObjectHandle(client_id,'/wall/ForceSensor[0]/fruit0',sim.simx_opmode_blocking)
    returnCode=sim.simxSetObjectPosition(client_id,fs1,-1,[+0.049998,-0.25000,0.31050],sim.simx_opmode_oneshot)

    returnCode,fs2=sim.simxGetObjectHandle(client_id,'/wall/ForceSensor[1]',sim.simx_opmode_blocking)
    returnCode,fruit2=sim.simxGetObjectHandle(client_id,'/wall/ForceSensor[1]/fruit1',sim.simx_opmode_blocking)
    returnCode=sim.simxSetObjectPosition(client_id,fs2,-1,[+0.05,-0.25000,0.24250],sim.simx_opmode_oneshot)

    returnCode,fs3=sim.simxGetObjectHandle(client_id,'/wall/ForceSensor[2]',sim.simx_opmode_blocking)
    returnCode,fruit3=sim.simxGetObjectHandle(client_id,'/wall/ForceSensor[2]/fruit2',sim.simx_opmode_blocking)
    returnCode=sim.simxSetObjectPosition(client_id,fs3,-1,[+0.049998,-0.25000,0.16750],sim.simx_opmode_oneshot)

    returnCode,diff_drive_bot=sim.simxGetObjectHandle(client_id,'./Diff_Drive_Bot',sim.simx_opmode_blocking)
    returnCode=sim.simxSetObjectPosition(client_id,diff_drive_bot,-1,[0.04699,-0.5,0.041],sim.simx_opmode_oneshot)


    #REMOVE ALL EXTRA OBJECTS
    returnCode,last_handle=sim.simxGetObjectHandle(client_id,'./last_handle',sim.simx_opmode_blocking)
    for i in range(last_handle+1,last_handle+200):
        returnCode=sim.simxRemoveObject(client_id,i,sim.simx_opmode_blocking)
        if returnCode>0:
            break
        print(i)


    #INITIALISATION

    emptybuff = bytearray()
    ripe_berries_list=[[(+0.049998,-0.27500,0.31050),fruit1],[(+0.05,-0.2750,0.16750),fruit3]]
    unripe_berries_list=[[(+0.05,-0.26000,0.24250),fruit2]]
    sim.simxSetStringSignal(client_id,'end simulation','false',sim.simx_opmode_blocking)

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
    while True:
        retcode, signal=sim.simxGetStringSignal(client_id, 'end simulation', sim.simx_opmode_blocking)
        string= signal.decode('utf-8')
        if string=='false':
            continue
        else:
            break


    #RESULTS
    untouched, deposited, displaced, unripe_untouched, unripe_deposited, unripe_displaced=check_berry_status(client_id, ripe_berries_list, unripe_berries_list)
    print('total ripe fruits= 2')
    print('total unripe fruits= 1')
    print('correctly deposited ripe fruits=',len(deposited))
    print('undeposited ripe fruits=',len(untouched))
    print('misplaced unripe fruits=',len(unripe_displaced))
    score = 100-len(untouched)*50-len(unripe_displaced)*50
    print('score=',score)
    task_data_dict = {}
    task_data_dict['correctly deposited ripe fruits']= len(deposited)
    task_data_dict['undeposited ripe fruits']= len(untouched)
    task_data_dict['misplaced unripe fruits=']=len(unripe_displaced)
    data = ['Task 4: ARM CONTROL']
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
