'''
Created on 17-Jun-2022

@author: User
'''
import sys
import os
if os.getcwd().find('AppData\\Local') == -1:
    dev=''
else:
    dev = '/resources'
sys.path.append(os.getcwd()+dev+'/backend/extraResources/sim/')
import sim


def check_berry_status(client_id, ripe_berries, unripe_berries):
    untouched=[]
    deposited=[]
    displaced=[]
    unripe_untouched=[]
    unripe_displaced=[]
    unripe_deposited=[]
    
    for berry in ripe_berries:
        _,pos=sim.simxGetObjectPosition(client_id,berry[1],-1,sim.simx_opmode_blocking)
        pos=(round(pos[0],2),round(pos[1],2),round(pos[2],2))
        #check if untouched
        if (pos[0]>berry[0][0]-0.05 and pos[0]<berry[0][0]+0.05) and (pos[1]>berry[0][1]-0.05 and pos[1]<berry[0][1]+0.05) and (pos[2]>berry[0][2]-0.05 and pos[2]<berry[0][2]+0.05):
            untouched.append(berry)
            
        elif ((-0.2<pos[0]<0.3) and ((-0.9<pos[1]<-0.6) or 
                    (-0.2<pos[0]<0.3) and(0.6<pos[1]<0.9))):
            deposited.append(berry)
            
        else:
            displaced.append(berry)
            
            
    for berry in unripe_berries:
        _,pos=sim.simxGetObjectPosition(client_id,berry[1],-1,sim.simx_opmode_blocking)
        pos=(round(pos[0],2),round(pos[1],2),round(pos[2],2))
        #check if untouched
        if (pos[0]>berry[0][0]-0.05 and pos[0]<berry[0][0]+0.05) and (pos[1]>berry[0][1]-0.05 and pos[1]<berry[0][1]+0.05) and (pos[2]>berry[0][2]-0.05 and pos[2]<berry[0][2]+0.05):
            unripe_untouched.append(berry)
            
        elif ((-0.2<pos[0]<0.3) and ((-0.8<pos[1]<-0.67) or 
                    (-0.2<pos[0]<0.3) and(0.6<pos[1]<0.88))):
            unripe_deposited.append(berry)
            
        else:
            unripe_displaced.append(berry)
            
    return untouched, deposited, displaced, unripe_untouched, unripe_deposited, unripe_displaced    


if __name__ == '__main__':
    pass