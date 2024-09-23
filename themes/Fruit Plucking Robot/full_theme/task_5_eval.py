import sim
import random
import os
import numpy as np
import cv2
from pluck_eval import check_berry_status
import sys
print(os.getcwd())
sheet_path = os.getcwd()+'/resources/backend/extraResources/push_to_sheet/'
sys.path.append(sheet_path)
import push_to_sheet
#print ('Program started')
score = 0
sim.simxFinish(-1) # just in case, close all opened connections
client_id = sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
cwd=os.getcwd()
#POSITION BOT AT START POINT
returnCode,diff_drive_bot=sim.simxGetObjectHandle(client_id,'./Diff_Drive_Bot',sim.simx_opmode_blocking)
returnCode=sim.simxSetObjectPosition(client_id,diff_drive_bot,-1,[-0.5,0,0.04],sim.simx_opmode_oneshot)
#REMOVE ALL EXTRA OBJECTS
returnCode,last_handle=sim.simxGetObjectHandle(client_id,'./last_handle',sim.simx_opmode_blocking)
# for i in range(last_handle+1,last_handle+200):
#     returnCode=sim.simxRemoveObject(client_id,i,sim.simx_opmode_blocking)
#     if returnCode>0:
#         break
#     print(i)
#REMOVE FRUITS
returnCode,tree=sim.simxGetObjectHandle(client_id,'./tree',sim.simx_opmode_blocking)
returnCode,fs0=sim.simxGetObjectHandle(client_id,'./tree/ForceSensor[0]',sim.simx_opmode_blocking)
returnCode,tree_end=sim.simxGetObjectHandle(client_id,'./tree/tree_end',sim.simx_opmode_blocking)
#print(tree)
for i in range(fs0,tree_end,1):
    returnCode=sim.simxRemoveObject(client_id,i,sim.simx_opmode_blocking)
    #print('removed',i)
#GENERATE NEW RANDOM FRUITS
get_pos = {'sheet_1_L1':[-0.2,0.15],'sheet_1_L2':[-0.2,0],'sheet_1_L3':[-0.2,-0.15],'sheet_2_L1':[-0.1,-0.25],'sheet_2_L2':[0.05,-0.25],'sheet_2_L3':[0.2,-0.25],
'sheet_3_L1':[0.3,-0.15],'sheet_3_L2':[0.3,0],'sheet_3_L3':[0.3,0.15],'sheet_4_L1':[0.2,0.25],'sheet_4_L2':[0.05,0.25],'sheet_4_L3':[-0.1,0.25]}
sheet_1_fruits=[]
sheet_2_fruits=[]
sheet_3_fruits=[]
sheet_4_fruits=[]
ripe_fruits=[]
unripe_fruits=[]
for i in range(1,5):
    ref1='./sheet_'+str(i)
    r=0
    u=0
    n=0
    for j in range(3):
        for k in range(1,4):
            ref=ref1+'_L'+str(k)
            returnCode,ref_dummy=sim.simxGetObjectHandle(client_id,ref,sim.simx_opmode_blocking)
            #print(ref,returnCode,ref_dummy)
            if j==0:
                pos=round(random.uniform(0.025,0.035),4)
            elif j==1:
                pos=round(random.uniform(0.085,0.115),4)
            elif j==2:
                pos=round(random.uniform(0.165,0.175),4)
            fruit_pos = (get_pos[ref[2:]][0],get_pos[ref[2:]][1],round(0.3385-pos,2))
            #print(fruit_pos)
            random_no=random.randint(1,3)
            if random_no == 1 and r<3:
                r+=1
                print(cwd)
                fruit_holder = cwd+"/resources/backend/extraResources/task5/models/sheet_"+str(i)+"_ripe.ttm"
                returnCode,fruit_holder_handle=sim.simxLoadModel(client_id,fruit_holder,0,sim.simx_opmode_blocking)
                returnCode=sim.simxSetObjectPosition(client_id,fruit_holder_handle,-1,fruit_pos,sim.simx_opmode_oneshot)
                returnCode=sim.simxSetObjectParent(client_id,fruit_holder_handle,tree,True,sim.simx_opmode_oneshot)
                ripe_fruits.append([fruit_pos,fruit_holder_handle+1])
            elif random_no == 2 and u<3:
                u+=1
                fruit_holder = cwd+"/resources/backend/extraResources/task5/models/sheet_"+str(i)+"_unripe.ttm"
                returnCode,fruit_holder_handle=sim.simxLoadModel(client_id,fruit_holder,0,sim.simx_opmode_blocking)
                returnCode=sim.simxSetObjectPosition(client_id,fruit_holder_handle,-1,fruit_pos,sim.simx_opmode_oneshot)
                returnCode=sim.simxSetObjectParent(client_id,fruit_holder_handle,tree,True,sim.simx_opmode_oneshot)
                unripe_fruits.append([fruit_pos,fruit_holder_handle+1])
            elif random_no == 3 and n<3:
                n+=1
            if random_no==1 or random_no==2:
                temp=[fruit_pos,fruit_holder_handle+1]
                if i==1:
                    sheet_1_fruits.append(temp)
                elif i==2:
                    sheet_2_fruits.append(temp)
                elif i==3:
                    sheet_3_fruits.append(temp)
                elif i==4:
                    sheet_4_fruits.append(temp)
returnCode=sim.simxRemoveObject(client_id,tree_end,sim.simx_opmode_blocking)
tree_ends = cwd+"/resources/backend/extraResources/task5/models/tree_end.ttm"
returnCode,tree_end=sim.simxLoadModel(client_id,tree_ends,0,sim.simx_opmode_blocking)
returnCode=sim.simxSetObjectParent(client_id,tree_end,tree,True,sim.simx_opmode_oneshot)
returnCode=sim.simxRemoveObject(client_id,last_handle,sim.simx_opmode_blocking)
last_han = cwd+"/resources/backend/extraResources/task5/models/last_handle.ttm"
returnCode,last_handle=sim.simxLoadModel(client_id,last_han,0,sim.simx_opmode_blocking)
total_ripe_fruits=len(ripe_fruits)
total_unripe_fruits=len(unripe_fruits)
#SETUP
#(0,0) pos = (320,320) pix
pos=(-0.5,0)
rad=15
start=True
init=False
stop=False
allow=False
divergence=0
divergence_x=0
divergence_y=0
latest_check=(320,595)
pos_list=[]
check_points=[(70,70),(570,70),(70,570),(570,570),(70,320),(570,320),(70,320+75),(570,320+75),(70,320-75),(570,320-75),(320,70),(320,570),(320+75,70),(320+75,570),(320-75,70),(320-75,570)]
check_colors=[(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255),(0,0,255)]
#500 pix = 1 metre
returnCode,diff_drive_bot=sim.simxGetObjectHandle(client_id,'./Diff_Drive_Bot',sim.simx_opmode_blocking)
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
    start=True
    blank = np.zeros([640,640,3],np.uint8)
    blank = cv2.line(blank, (70,320),(570,320),(255,255,255),2)
    blank = cv2.line(blank, (70,320+75),(570,320+75),(255,255,255),2)
    blank = cv2.line(blank, (70,320-75),(570,320-75),(255,255,255),2)
    blank = cv2.line(blank, (320,70),(320,570),(255,255,255),2)
    blank = cv2.line(blank, (320+75,70),(320+75,570),(255,255,255),2)
    blank = cv2.line(blank, (320-75,70),(320-75,570),(255,255,255),2)
    for check_point,check_color in zip(check_points,check_colors):
        #print(check_point,check_color)
        blank = cv2.circle(blank,check_point,15,check_color,-1)
    blank = cv2.rectangle(blank, (70,70),(570,570),(255,255,255),2)
    returnCode,position=sim.simxGetObjectPosition(client_id,diff_drive_bot,-1,sim.simx_opmode_streaming)
    returnCode,position=sim.simxGetObjectPosition(client_id,diff_drive_bot,-1,sim.simx_opmode_buffer)
    pos=(round(position[0],4),round(position[1],4))
    pix_pos = ((int(-1*pos[1]*500)+320),(int(-1*(pos[0]-0.05)*500)+320))
    for check_point,check_color in zip(check_points,check_colors):
        if (pix_pos[0]-check_point[0])**2+(pix_pos[1]-check_point[1])**2<=rad:
            latest_check=check_point
            init=True
            start=False
            check_colors[check_points.index(check_point)]=(0,255,0)
            if check_point==(320+75,570):
                allow=True
            if check_point==(70,320) and allow:
                stop=True
    fnt = cv2.FONT_ITALIC                                      # for text select font
    blank = cv2.putText(blank,'Press Q to abort',(250,40),fnt,0.8,(0,0,255),2)
    blank = cv2.putText(blank,'latest checkpoint',(latest_check[0]-50,latest_check[1]-10),fnt,1,(0,0,255),2)
    if init and start:
        x=pix_pos[0]
        y=pix_pos[1]
        if x>=570:
            divergence_x=x-570
        if x<=570 and x>320:
            divergence_x=570-x
        if x<=70:
            divergence_x=70-x
        if x>=70 and x<320:
            divergence_x=x-70
        if y>=570:
            divergence_y=y-570
        if y<=570 and y>320:
            divergence_y=570-y
        if y<=70:
            divergence_y=70-y
        if y>=70 and y<320:
            divergence_y=y-70
        divergence+=min(divergence_x,divergence_y)
    blank = cv2.putText(blank,'divergence='+str(divergence/10000)+'%',(150,150),fnt,0.5,(0,0,255),2)
    line_following_score=100-divergence/10000
    pos_list.append(pix_pos)
    for pos in pos_list:
        blank = cv2.circle(blank,pos,2,(0,255,0),-1)
    #print(pos,pix_pos)
    blank = cv2.circle(blank,pix_pos,50,(255,0,0),2)
    cv2.imshow('test',blank)
    if cv2.waitKey(1)==ord('q') or stop:      #...Press Q to Quit Video
        blank = np.zeros([640,640,3],np.uint8)
        untouched, deposited, displaced, unripe_untouched, unripe_deposited, unripe_displaced=check_berry_status(client_id, ripe_fruits, unripe_fruits)
        return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)
        if (return_code == sim.simx_return_novalue_flag) or (return_code == sim.simx_return_ok):
            print('\nSimulation stopped correctly.')
        else:
            print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
            print('[ERROR] stop_simulation function is not configured correctly, check the code!')
            print('Stop the CoppeliaSim simulation manually.')
        break
cv2.destroyAllWindows()
# print('sheet 1-\n',sheet_1_fruits)
# print('sheet 2-\n',sheet_2_fruits)
# print('sheet 3-\n',sheet_3_fruits)
# print('sheet 4-\n',sheet_4_fruits)
# print('ripe fruits-\n',ripe_fruits)
# print('unripe fruits-\n',unripe_fruits)
#print(untouched, deposited, displaced, unripe_untouched, unripe_deposited, unripe_displaced)
print('line_following_score(out of 100)=',line_following_score)
print('total ripe fruits=',total_ripe_fruits)
print('total unripe fruits=',total_unripe_fruits)
print('correctly deposited ripe fruits=',len(deposited))
print('displaced ripe fruits=',len(displaced))
print('undeposited ripe fruits=',len(untouched))
print('misplaced unripe fruits=',len(unripe_displaced))
score = (total_ripe_fruits-len(untouched)-len(displaced)*100/total_ripe_fruits)+(total_unripe_fruits-len(unripe_displaced)*100/total_unripe_fruits)
score = score*0.6+line_following_score*0.4
if len(deposited)==0:
    score = 0
print('score=',score)
task_data_dict = {}
task_data_dict['line_following_score(out of 100)']=line_following_score
task_data_dict['total ripe fruits']=total_ripe_fruits
task_data_dict['total unripe fruits']=total_unripe_fruits
task_data_dict['correctly deposited ripe fruits']=len(deposited)
task_data_dict['displaced ripe fruits']=len(displaced)
task_data_dict['undeposited ripe fruits']=len(untouched)
task_data_dict['misplaced unripe fruits']=len(unripe_displaced)
data = ['Task 5: FULL THEME']
data.append(str(task_data_dict))
data.append(str(score))
push_to_sheet.send_to_sheets(data)
# Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
sim.simxGetPingTime(client_id)
# Now close the connection to CoppeliaSim:
sim.simxFinish(client_id)
#print('connection ended')