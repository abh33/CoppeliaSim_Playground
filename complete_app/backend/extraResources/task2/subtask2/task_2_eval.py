#!python3
import cv2
import numpy as np
from math import sqrt
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

def init_remote_Api(): # for staring our remote api connection
    sim.simxFinish(-1)
    client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    return client_id

def start_simulation(client_id): # for starting simulation
    return_code = -2
    if client_id!= -1:
        return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
    return return_code

def stop_simulation(client_id): # for ending simulation
    return_code = -2
    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)
    sim.simxGetPingTime(client_id)
    return return_code

def exit_remote_Api(client_id): # for ending our remote api connection
    sim.simxFinish(client_id)


class Evaluater():

    def __init__(self, points, width, height, inner_width, inner_height, scale):
        ############# initialization ####################
        self.points = {} # it will hold the points that need to be traversed
        self.W = (width, int(round(scale*width))) # width of the platform
        self.H = (height, int(round(scale*height))) # height of the platform
        self.inW = (inner_width, int(round(scale*inner_width))) # width of the arena
        self.inH = (inner_height, int(round(scale*inner_height))) # height of the arena
        self.scale = scale
        self.prev_pnt = [[-1,-1], (-1,-1)] # it will store the previous point, the point where the bot was before coming to current point. during start its value is not determined
        self.current_crossed_point = "start" # the bot will start from "start" position
        self.actual_path_length = 0 # the actual length of the path needs to be covered
        self.bot_path_length = 0 # the actual length covered by bot
        ############# Default value for drawing ###############
        self.line_colour = (255,255,255)
        self.start_finish_colour = (255,0,0)
        self.control_points_colour = (0,0,255)
        self.bot_colour = (0,255,0)
        self.path_colour = (0,255,0)
        #######################################################
        ####### Here the dictionary will have keys as the name of the checkpoints and values is a list with first element as the coordinates of the checkpoints in absolute coordinates in coppeliasim scene, and second element is the pixel coordinate of the same checkpoints w.r.t. to the arena image we are going to make. remember the size of arena image and original coppeliasim arena are in proportion ###########
        for name,p in points.items():
            p = (int(round(scale*p[0])), int(round(scale*p[1]))) # converting coordinates to pixel coordinates
            p = (p[0]+self.W[1]//2, -p[1]+self.H[1]//2) # setting the origin ti upper left corner
            self.points[name] = [points[name], p]
        self.eval_points = self.points.copy() # we make a copy of this dictionary
        #####################################################

    def set_handle(self, client_id, bot, front):
        ######## to get handle of diff bot, and front slider joint(for knowing orientation) ############
        self.id = client_id
        code, self.bot = sim.simxGetObjectHandle(client_id,bot,sim.simx_opmode_blocking)
        code, self.front = sim.simxGetObjectHandle(client_id,front,sim.simx_opmode_blocking)

    def set_colour(self, line_colour, start_finish_colour, control_points_colour, bot_colour, path_colour):
        ########## to change default colours of drawing ##################
        self.line_colour = line_colour
        self.start_finish_colour = start_finish_colour
        self.control_points_colour = control_points_colour
        self.bot_colour = bot_colour
        self.path_colour = path_colour

    def create_arena(self):
        ######### create the arena #################
        arena = np.zeros((self.H[1], self.W[1], 3),np.uint8) # our blank image to draw the arena
        self.bot_tracked_image = np.zeros((self.H[1], 2*self.W[1], 3),np.uint8) # for drawing arena along with bot raw path side by side, so width is doubled, left side is for arena and right for raw path drawing 
        ########## creating arena limiting boundary###############
        top_left = ((self.W[1]-self.inW[1])//2, (self.H[1]-self.inH[1])//2)
        bottom_right = ((self.W[1]+self.inW[1])//2, (self.H[1]+self.inH[1])//2)
        cv2.rectangle(arena,top_left,bottom_right,(255,255,255),self.W[1]//200)
        ##########################################################
        for name,p in self.points.items():
            p = p[1] # remember second element of the list contains coordinates in pixels(line no. 53)
            if name == "start" or name == "finish": # for start and finish points, we will draw them with different colours
                if name == "start": # for start only, there is no next point for finish as it is the last point
                    next_p = self.points["pt1"][1] # our next point is pt1
                    cv2.line(arena,next_p,p,self.line_colour,self.W[1]//200) # draw the line between them, width of the line is proportional to the size of the image
                cv2.circle(arena,p,self.W[1]//40,self.start_finish_colour,-1) # draw those points, radius of circle is proportional to size of image
            else:
                if name == f"pt{len(self.points.keys())-2}": # ofcourse if we are at 2nd last point, our next point will be "finish"
                    next = "finish"
                else: # else if we are at pt1, next will be pt2, if we are at pt4, next will be pt5 and so on..
                    next = f"pt{int(name[2:])+1}"
                next_p = self.points[next][1]
                cv2.line(arena,next_p,p,self.line_colour,self.W[1]//200) # draw line between this point and its next point
                cv2.circle(arena,p,self.W[1]//40,self.control_points_colour,-1) # draw the point
        self.arena = arena

    def get_position(self):
        ########## getting the position of bot and its front slider wheel #############
        code, bot_position = sim.simxGetObjectPosition(self.id,self.bot,-1,sim.simx_opmode_streaming)
        code, front_position = sim.simxGetObjectPosition(self.id,self.front,-1,sim.simx_opmode_streaming)
        while True:
            code, bot_position = sim.simxGetObjectPosition(self.id,self.bot,-1,sim.simx_opmode_blocking)
            if code == 0:
                break
         ############ here again storing convention is, list 1st element is absolute coordinates and 2nd element is pixel coordinate ############
        x, y = int(round(self.scale*bot_position[0])), int(round(self.scale*bot_position[1]))
        x, y = x + self.W[1]//2, -y + self.H[1]//2
        self.bot_position = (bot_position[:-1],(x,y))
        ##################################################################################################################
        while True:
            code, front_position = sim.simxGetObjectPosition(self.id,self.front,-1,sim.simx_opmode_blocking)
            if code == 0:
                break
        ###################################################################################
        ############ here again storing convention is, list 1st element is absolute coordinates and 2nd element is pixel coordinate ############
        x, y = int(round(self.scale*front_position[0])), int(round(self.scale*front_position[1]))
        x, y = x + self.W[1]//2, -y + self.H[1]//2
        self.front_position = (front_position[:-1],(x,y))
        ################################################################################################################

    def track(self):
        self.tracked = self.arena.copy()
        ########## drawing bot current position and its orientation(orientation with the help of position of front slider)#########
        cv2.circle(self.tracked,self.bot_position[1],self.W[1]//15,self.bot_colour,self.W[1]//200)
        cv2.line(self.tracked,self.bot_position[1],self.front_position[1],self.bot_colour,self.W[1]//50)
        cv2.circle(self.tracked,self.front_position[1],self.W[1]//150,(255,0,0),-1)
        ##########################################################################################################################
        p = self.bot_position[0] # grab bot's current position(in absolute coordinates)
        if self.prev_pnt[0][0] != -1: # if we have our previous point
            self.bot_path_length = self.bot_path_length + sqrt((p[0]-self.prev_pnt[0][0])**2 + (p[1]-self.prev_pnt[0][1])**2) # update bots actual path length by adding the extra path bot travelled from previous point to current point
        else: # otherwise, add the path the bot travelled while moving from "start" to current point(remember initial value of self.current_crossed_point is "start")
            self.bot_path_length = self.bot_path_length + sqrt((p[0]-self.points[self.current_crossed_point][0][0])**2 + (p[1]-self.points[self.current_crossed_point][0][1])**2)


    def show_path(self):
        x, y = self.bot_position[1] # grab pixel coordinates
        for name,p in self.points.items():
            if abs(x-p[1][0]) < self.W[1]/100 and abs(y-p[1][1]) < self.W[1]/100: # if bot have reached the checkpoint
                ######### colour the checkpoint ##################
                cv2.circle(self.arena,p[1],self.W[1]//40,self.path_colour,-1)
                cv2.circle(self.bot_tracked_image[:,self.W[1]:],p[1],self.W[1]//40,self.path_colour,-1)
                #################################################
                ###### we are removing the points which are reached by bot ##############
                if self.current_crossed_point in self.points.keys(): # checking whether we are not trying to remove a already removed point
                    del self.points[self.current_crossed_point] # remove the point
                ########################################################################
                self.current_crossed_point = name # update our current crossed checkpoint
                break
        if self.prev_pnt[1][0] != -1: # if we have our previous point
            cv2.line(self.arena,self.bot_position[1],self.prev_pnt[1],self.path_colour,self.W[1]//250) # draw line between current point and previous point on arena
            cv2.line(self.bot_tracked_image[:,self.W[1]:],self.bot_position[1],self.prev_pnt[1],self.path_colour,self.W[1]//250) # draw line between current point and previous point on our raw path drawing
        self.prev_pnt = self.bot_position # update our previous point
        self.bot_tracked_image[:,:self.W[1]] = self.tracked

    def evaluate(self):
        name_list = list(self.eval_points.keys()) # get all the checkpoints
        ####### calculating actual length of path that was need to travelled ############
        for i,name in enumerate(name_list[1:]):
            self.actual_path_length = self.actual_path_length + sqrt((self.eval_points[name][0][0]-self.eval_points[name_list[i]][0][0])**2 + (self.eval_points[name][0][1]-self.eval_points[name_list[i]][0][1])**2)
        #################################################################################
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
    data = ['Task 2: MOVEMENT / Subtask 2']
    data.append(str(task_data_dict))
    data.append(str(score))
    push_to_sheet.send_to_sheets(data)