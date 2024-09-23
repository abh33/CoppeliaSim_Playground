#!python3
import cv2

import numpy as np
import sim
from math import sqrt

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


class Evaluater():

    def __init__(self, points, width, height, inner_width, inner_height, scale):
        self.points = {}
        self.W = (width, int(round(scale*width)))
        self.H = (height, int(round(scale*height)))
        self.inW = (inner_width, int(round(scale*inner_width)))
        self.inH = (inner_height, int(round(scale*inner_height)))
        self.scale = scale
        self.prev_pnt = [[-1,-1], (-1,-1)]
        self.current_crossed_point = "start"
        self.actual_path_length = 0
        self.bot_path_length = 0
        self.line_colour = (255,255,255)
        self.start_finish_colour = (255,0,0)
        self.control_points_colour = (0,0,255)
        self.bot_colour = (0,255,0)
        self.path_colour = (0,255,0)
        for name,p in points.items():
            p = (int(round(scale*p[0])), int(round(scale*p[1])))
            p = (p[0]+self.W[1]//2, -p[1]+self.H[1]//2)
            self.points[name] = [points[name], p]

    def set_handle(self, client_id, bot, front):
        self.id = client_id
        code, self.bot = sim.simxGetObjectHandle(client_id,bot,sim.simx_opmode_blocking)
        code, self.front = sim.simxGetObjectHandle(client_id,front,sim.simx_opmode_blocking)

    def set_colour(self, line_colour, start_finish_colour, control_points_colour, bot_colour, path_colour):
        self.line_colour = line_colour
        self.start_finish_colour = start_finish_colour
        self.control_points_colour = control_points_colour
        self.bot_colour = bot_colour
        self.path_colour = path_colour

    def create_arena(self):
        arena = np.zeros((self.H[1], self.W[1], 3),np.uint8)
        self.bot_tracked_image = np.zeros((self.H[1], 2*self.W[1], 3),np.uint8)
        top_left = ((self.W[1]-self.inW[1])//2, (self.H[1]-self.inH[1])//2)
        bottom_right = ((self.W[1]+self.inW[1])//2, (self.H[1]+self.inH[1])//2)
        cv2.rectangle(arena,top_left,bottom_right,(255,255,255),self.W[1]//200)
        for name,p in self.points.items():
            p = p[1]
            if name == "start" or name == "finish":
                if name == "start":
                    next_p = self.points["pt1"][1]
                    cv2.line(arena,next_p,p,self.line_colour,self.W[1]//200)
                cv2.circle(arena,p,self.W[1]//40,self.start_finish_colour,-1)
            else:
                if name == f"pt{len(self.points.keys())-2}":
                    next = "finish"
                else:
                    next = f"pt{int(name[2:])+1}"
                next_p = self.points[next][1]
                cv2.line(arena,next_p,p,self.line_colour,self.W[1]//200)
                cv2.circle(arena,p,self.W[1]//40,self.control_points_colour,-1)
        self.arena = arena

    def get_position(self):
        code, bot_position = sim.simxGetObjectPosition(self.id,self.bot,-1,sim.simx_opmode_streaming)
        code, front_position = sim.simxGetObjectPosition(self.id,self.front,-1,sim.simx_opmode_streaming)
        while True:
            code, bot_position = sim.simxGetObjectPosition(self.id,self.bot,-1,sim.simx_opmode_blocking)
            if code == 0:
                break
        x, y = int(round(self.scale*bot_position[0])), int(round(self.scale*bot_position[1]))
        x, y = x + self.W[1]//2, -y + self.H[1]//2
        self.bot_position = (bot_position[:-1],(x,y))
        while True:
            code, front_position = sim.simxGetObjectPosition(self.id,self.front,-1,sim.simx_opmode_blocking)
            if code == 0:
                break
        x, y = int(round(self.scale*front_position[0])), int(round(self.scale*front_position[1]))
        x, y = x + self.W[1]//2, -y + self.H[1]//2
        self.front_position = (front_position[:-1],(x,y))

    def track(self):
        self.tracked = self.arena.copy()
        cv2.circle(self.tracked,self.bot_position[1],self.W[1]//15,self.bot_colour,self.W[1]//200)
        cv2.line(self.tracked,self.bot_position[1],self.front_position[1],self.bot_colour,self.W[1]//50)
        cv2.circle(self.tracked,self.front_position[1],self.W[1]//150,(255,0,0),-1)
        p = self.bot_position[0]
        if self.prev_pnt[0][0] != -1:
            self.bot_path_length = self.bot_path_length + sqrt((p[0]-self.prev_pnt[0][0])**2 + (p[1]-self.prev_pnt[0][1])**2)
        else:
            self.bot_path_length = self.bot_path_length + sqrt((p[0]-self.points[self.current_crossed_point][0][0])**2 + (p[1]-self.points[self.current_crossed_point][0][1])**2)


    def show_path(self):
        x, y = self.bot_position[1]
        for name,p in self.points.items():
            if abs(x-p[1][0]) < self.W[1]/100 and abs(y-p[1][1]) < self.W[1]/100:
                cv2.circle(self.arena,p[1],self.W[1]//40,self.path_colour,-1)
                cv2.circle(self.bot_tracked_image[:,self.W[1]:],p[1],self.W[1]//40,self.path_colour,-1)
                self.current_crossed_point = name
                break
        if self.prev_pnt[1][0] != -1:
            cv2.line(self.arena,self.bot_position[1],self.prev_pnt[1],self.path_colour,self.W[1]//250)
            cv2.line(self.bot_tracked_image[:,self.W[1]:],self.bot_position[1],self.prev_pnt[1],self.path_colour,self.W[1]//250)
        self.prev_pnt = self.bot_position
        self.bot_tracked_image[:,:self.W[1]] = self.tracked

    def evaluate(self):
        name_list = list(self.points.keys())
        for i,name in enumerate(name_list[1:]):
            self.actual_path_length = self.actual_path_length + sqrt((self.points[name][0][0]-self.points[name_list[i]][0][0])**2 + (self.points[name][0][1]-self.points[name_list[i]][0][1])**2)
        self.error = self.bot_path_length - self.actual_path_length








# all distances here are in meters
W,H = 1.600, 1.800
w,h = 1.400, 1.400
# the convention is, for starting point the key should be "start", for finish point the key should be "finish" and for all
# intermediate points the key values will be "pt1" then "pt2" then "pt3" ... and so on. the values are just there x and y in m
points = {"start":[-0.600,-0.620], "pt1":[0.585,-0.620], "pt2":[0.585,0.104], "pt3":[0.317,0.104], "pt4":[0.317,-0.455],
            "pt5":[0.059,-0.455], "pt6":[0.059,0.294], "pt7":[0.585,0.294], "pt8":[0.585,0.590], "pt9":[-0.134,0.590],
            "pt10":[-0.134,-0.455], "pt11":[-0.330,-0.455], "pt12":[-0.330,0.589], "pt13":[-0.607,0.589], "finish":[-0.607,-0.212]}
scale = 250

if __name__ == "__main__":
    client_id = init_remote_Api()
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
    print('score=',100-abs(eval.error)*100/eval.actual_path_length)