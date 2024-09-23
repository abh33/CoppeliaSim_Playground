#!python3
from task2_2 import Evaluater
import cv2
import sys
import os
if os.getcwd().find('AppData\\Local') == -1:
    dev=''
else:
    dev = '/resources'
sys.path.append(os.getcwd()+dev+'/backend/extraResources/push_to_sheet/')
sys.path.append(os.getcwd()+dev+'/backend/extraResources/sim/')
import sim
import push_to_sheet

def init_remote_Api(): # for starting our remote api connection
    sim.simxFinish(-1)
    client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    return client_id

def start_simulation(client_id): # for starting simulation
    return_code = -2
    if client_id!= -1:
        return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
    return return_code

def stop_simulation(client_id): # for stopping simulation
    return_code = -2
    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)
    sim.simxGetPingTime(client_id)
    return return_code

def exit_remote_Api(client_id): # for ending our remote api connection
    sim.simxFinish(client_id)


# all distances here are in meters
W,H = 2.0, 2.0
w,h = 1.35, 1.35
# the convention is, for starting point the key should be "start", for finish point the key should be "finish" and for all
# intermediate points the key values will be "pt1" then "pt2" then "pt3" ... and so on. the values are just there x and y in m
points = {"start":[0.500,0.500], "pt1":[-0.500,0.500], "pt2":[-0.500,-0.498], "pt3":[0.500,-0.498], "finish":[0.500,0.500]}
scale = 250 # this scale is used to convert the raw value in meters to considerable pixel size to draw them

if __name__ == "__main__":
    client_id = init_remote_Api()
    code = start_simulation(client_id)

    eval = Evaluater(points,W,H,w,h,scale) # our evaluator class
    # eval.set_colour((255,0,0),(0,0,255),(0,255,0),(255,255,255),(255,0,255))
    eval.create_arena() # first creating the arena
    eval.set_handle(client_id,'./Diff_Drive_Bot','./Diff_Drive_Bot/front_slider_joint') # setting handles
    while True:
        eval.get_position() # get position of bot
        eval.track() # track and draw its position
        eval.show_path() # draw the raw path followed by the bot
        cv2.imshow("bot tracking", eval.bot_tracked_image)
        if cv2.waitKey(1) == ord('q') or eval.current_crossed_point == "finish":
            break
    cv2.destroyAllWindows()

    stop_simulation(client_id)
    exit_remote_Api(client_id)

    eval.evaluate() # this will call the inner evaluator function
    print("Error = ",abs(eval.error),"m")
    score = 100-abs(eval.error)*100/eval.actual_path_length
    print('score=',score)
    task_data_dict = {}
    task_data_dict['Error']= str(abs(eval.error))+" m"
    data = ['Task 2:MOVEMENT / Subtask 1']
    data.append(str(task_data_dict))
    data.append(str(score))
    push_to_sheet.send_to_sheets(data)