#!python3

import sim
import sys
import os
#print(os.getcwd())
#sheet_path = os.getcwd()+'\\backend\\extraResources\\push_to_sheet'
#print(sheet_path)
#sys.path.append(sheet_path)
# print(cv2_path)
# import cv2
#import push_to_sheet
import cv2
#print(sys.path)
print(cv2.__file__)
#print(push_to_sheet.__file__)
from evaluator import Evaluater

def init_remote_Api():
    sim.simxFinish(-1)
    client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    return client_id

def start_simulation(client_id):
    return_code = -2
    if client_id!= -1:
        return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
    return return_code

def stop_simulation(client_id):
    return_code = -2
    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)
    sim.simxGetPingTime(client_id)
    return return_code

def exit_remote_Api(client_id):
    sim.simxFinish(client_id)


# all distances here are in meters
W,H = 2.0, 2.0
w,h = 1.35, 1.35
# the convention is, for starting point the key should be "start", for finish point the key should be "finish" and for all
# intermediate points the key values will be "pt1" then "pt2" then "pt3" ... and so on. the values are just there x and y in m
points = {"start":[0.500,0.500], "pt1":[-0.500,0.500], "pt2":[-0.500,-0.498], "pt3":[0.500,-0.498], "finish":[0.500,0.500]}
scale = 250

if __name__ == "__main__":
    client_id = init_remote_Api()
    if client_id==-1:
        print('[Error] Make sure to open scene before Evaluation.')
    else:
        code = start_simulation(client_id)

        eval = Evaluater(points,W,H,w,h,scale)
        # eval.set_colour((255,0,0),(0,0,255),(0,255,0),(255,255,255),(255,0,255))
        eval.create_arena()
        eval.set_handle(client_id,'./Diff_Drive_Bot','./Diff_Drive_Bot/front_slider_joint')
        while True:
            eval.get_position()
            eval.track()
            eval.show_path()
            cv2.imshow("bot tracking", eval.bot_tracked_image)
            if cv2.waitKey(1) == ord('q') or eval.current_crossed_point == "finish":
                break
        cv2.destroyAllWindows()

        stop_simulation(client_id)
        exit_remote_Api(client_id)

        eval.evaluate()
        print("Error = ",abs(eval.error),"m")
        score = 100-abs(eval.error)*100/eval.actual_path_length
        print('score=',score)
        task_data_dict = {}
        task_data_dict['Error']= abs(eval.error)+" m"
        data = ['Task 2:MOVEMENT / Subtask 1']
        data.append(str(task_data_dict))
        data.append(str(score))
        #push_to_sheet.send_to_sheets(data)