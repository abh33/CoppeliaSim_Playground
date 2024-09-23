
import os
import sys
import traceback
import time
global dev
if os.getcwd().find('AppData\\Local') == -1:
    dev=''
else:
    dev = '/resources'
sys.path.append(os.getcwd()+dev+'/backend/extraResources/push_to_sheet/')
sys.path.append(os.getcwd()+dev+'/backend/extraResources/sim/')
import sim
import push_to_sheet



global output_list_child_eval, output_list_custom_eval, output_list_child, output_list_custom, rtf_python
eval_rtf_python = 0
position = [0, 0, 0]

# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# NOTE: DO NOT change the value of this "client_id" variable here
client_id = -1


def init_remote_api_server():

	global client_id
	##############  ADD YOUR CODE HERE  ##############

	sim.simxFinish(-1)  # just in case, close all opened connections
	client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5) # Connect to CoppeliaSim
	sim.simxGetPingTime(client_id)

	##################################################

	return client_id


def start_simulation():

	global client_id

	##############  ADD YOUR CODE HERE  ##############

	# return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
	if client_id != -1:
		return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)

	# Making sure that last command sent out had time to arrive
	sim.simxGetPingTime(client_id)

	##################################################

	return return_code


def stop_simulation():

	global client_id

	##############  ADD YOUR CODE HERE  ##############
 
	return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot_wait)
	sim.simxGetPingTime(client_id)

	##################################################

	return return_code


def exit_remote_api_server():

	global client_id

	##############  ADD YOUR CODE HERE  ##############

	sim.simxGetPingTime(client_id)
	sim.simxFinish(client_id)

	##################################################


def get_customization_data():
	global client_id

	inputBuffer = bytearray()
	return_code, retInts, retFloats, data_customization, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc_BM_2B',\
									sim.sim_scripttype_customizationscript,'get_required_data_custom',[],[],[],inputBuffer,sim.simx_opmode_blocking)
	# print("eval_data_customization:")
	# print(eval_data_customization)

	return data_customization

def get_child_data():
	global client_id

	inputBuffer = bytearray()
	return_code, retInts, retFloats, data_child, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc_BM_2B',\
									sim.sim_scripttype_childscript,'get_required_data_child',[],[],[],inputBuffer,sim.simx_opmode_blocking)
	# print("eval_data_child:")
	# print(eval_data_child)

	return data_child


def get_customization_data_for_eval():
	global client_id

	inputBuffer = bytearray()
	return_code, retInts, retFloats, eval_data_customization, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc_BM_2B',\
									sim.sim_scripttype_customizationscript,'get_required_data_custom_eval',[],[],[],inputBuffer,sim.simx_opmode_blocking)
	# print("eval_data_customization:")
	# print(eval_data_customization)

	return eval_data_customization


def get_child_data_for_eval():
	global client_id

	inputBuffer = bytearray()
	return_code, retInts, retFloats, eval_data_child, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc_BM_2B',\
									sim.sim_scripttype_childscript,'get_required_data_child_eval',[],[],[],inputBuffer,sim.simx_opmode_blocking)
	# print("eval_data_child:")
	# print(eval_data_child)

	return eval_data_child


# Need this function to call arm_check function only once after atleast one time step of simulation
def wait_for_check_scene():
	global client_id

	return_code_signal = 1
	flag_scene_all_ok = '0'
	init_timeout = time.time()
	end_timeout = init_timeout
	timeout = end_timeout - init_timeout

	# inputBuffer = bytearray()
	# return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc',\
	# 								sim.sim_scripttype_customizationscript,'arm_check',[],[],[],inputBuffer,sim.simx_opmode_blocking)

	# We will wait till we get the signal value. If the correct flag_scene_all_ok signal value is not obtained,
	#  or the timer expires the code will NOT proceed further.
	while(return_code_signal != 0 or flag_scene_all_ok != '1'):
		return_code_signal,flag_scene_all_ok = sim.simxGetStringSignal(client_id, 'gfh36801nc', sim.simx_opmode_blocking)
		end_timeout = time.time()
		timeout = end_timeout - init_timeout
		flag_scene_all_ok = str(flag_scene_all_ok, 'utf-8')
		# print('flag_scene_all_ok',flag_scene_all_ok)
		# print('return_code_signal',return_code_signal)
		if(timeout > 10):
			print('score=',0)
			print('\n[ERROR] Scene could not be checked. Check CoppeliaSim status bar.')
			print('Exiting evaluation')
			end_program()
			sys.exit()
			break


def load_eval_model():
	global client_id
	cwd = os.getcwd()
	#print(cwd)
	# Remove model if previously loaded.
	#try:
	return_code, disc_handle = sim.simxGetObjectHandle(client_id, 'Disc_BM_2B', sim.simx_opmode_blocking)
	if(return_code == 0): #This means that the object exists from before
		return_code, arm_handle = sim.simxGetObjectHandle( client_id, 'robotic_arm', sim.simx_opmode_blocking)
		return_code = sim.simxSetObjectParent( client_id, arm_handle, -1, True, sim.simx_opmode_blocking)
		return_code = sim.simxRemoveModel( client_id, disc_handle, sim.simx_opmode_blocking)
	#cwd = os.getcwd()
	#return_code,evaluation_screen_handle=sim.simxLoadModel(client_id,cwd+'//evaluation_projector_screen.ttm',0,sim.simx_opmode_blocking) #Load the new model
	return_code, disc_handle = sim.simxLoadModel( client_id, cwd+dev+'/backend/extraResources/task3/test_dummy_task_3.ttm', 0, sim.simx_opmode_blocking) #Load the new model
	if(return_code != 0):
		# print('[ERROR] Evaluation script failed to load. Please try again.')
		print('score=',0)
		print('\n[ERROR] Evaluation failed to start. Please try again.')
		end_program()
		sys.exit()
	else:
		# print('Evaluation script loaded successfully.')
		print('\nEvaluation started successfully.')
	# except Exception:
	# 	end_program()


# End the program
# Will stop the simulation, call organize_screen_end, clear string signals, exit the server
def end_program():
	global client_id


	return_code = stop_simulation()

	return_code, disc_handle = sim.simxGetObjectHandle(client_id, 'Disc_BM_2B', sim.simx_opmode_blocking)

	if (return_code == 0):				# This means that the object exists from before
		return_code, arm_handle = sim.simxGetObjectHandle( client_id, 'robotic_arm', sim.simx_opmode_blocking)
		if return_code == 0:
			return_code = sim.simxSetObjectParent( client_id, arm_handle, -1, True, sim.simx_opmode_blocking)
			returnCode = sim.simxSetObjectPosition( client_id, arm_handle, -1, position, sim.simx_opmode_blocking)
		inputBuffer = bytearray()
		return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc_BM_2B',\
									sim.sim_scripttype_customizationscript,'organize_screen_end',[],[],[],inputBuffer,sim.simx_opmode_blocking)


	# This is used to clear all the signals.
	return_code = sim.simxClearStringSignal(client_id, '', sim.simx_opmode_oneshot)

	try:
		exit_remote_api_server()

		if (start_simulation() == sim.simx_return_initialize_error_flag):
			print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

		else:
			print('score=',0)
			print('\n[ERROR] Failed disconnecting from Remote API server!')
			# print('[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

	except Exception:
		print('score=',0)
		# print('\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('\n[ERROR] The connection to Remote API Server did not end successfully!')
		print('Stop the CoppeliaSim simulation manually if required.\n')
		# traceback.print_exc(file=sys.stdout)
		print()


def task_3_cardinal_main():

	global output_list_child_eval, output_list_custom_eval, position, client_id, output_list_child, output_list_custom
	global rtf_python, eval_rtf_python

	# # Importing the sim module for Remote API connection with CoppeliaSim
	# try:
	# 	sim = __import__('sim')
		
	# except Exception:
	# 	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	# 	print('\n[WARNING] Make sure to have following files in the directory:')
	# 	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	# 	sys.exit()


	# Initiate the Remote API connection with CoppeliaSim server
	print('\nConnection to CoppeliaSim Remote API Server initiated.')
	print('Trying to connect to Remote API Server...')

	try:
		client_id = init_remote_api_server()
		if (client_id != -1):
			print('\nConnected successfully to Remote API Server in CoppeliaSim!')


			# Students should have opened task_3_scene.ttt with robotic arm present in it

			# Getting arm's default position
			return_code, arm_handle = sim.simxGetObjectHandle( client_id, 'robotic_arm', sim.simx_opmode_blocking)
			if return_code != sim.simx_return_ok:
				print('score=',0)
				print("[ERROR] Couldn't find robotic_arm in opened scene")
				print("Make sure you have opened task_3_scene.ttt which contains your robotic_arm")
				end_program()
				sys.exit()

			# Save original position of robotic arm 	
			returnCode, position = sim.simxGetObjectPosition( client_id, arm_handle, -1, sim.simx_opmode_blocking) 
			
			# Loading our disc force model
			load_eval_model()
			wait_for_check_scene()

			init_real_time = time.time()


			#  Start simulation
			return_code = start_simulation()

			if (return_code == sim.simx_return_novalue_flag):
				print('\nSimulation started correctly in CoppeliaSim.')

			else:
				print('score=',0)
				print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
				end_program()
				sys.exit()


			# Waiting for 1 simulation sec so that at least one time step is simulated
			# sleep(1.)
			return_code, init_sim_time = sim.simxGetStringSignal( client_id, 'time', sim.simx_opmode_blocking)
			# if return_code != sim.simx_return_ok:   # NOT SURE ABOUT THIS CONDITION
			# 	print("[ERROR] MAIN Script present in the task_3_scene has been modifed.")
			# 	print(("Download the scene file again."))
			# 	end_program()
			# 	sys.exit()

			check = 0
			while check <= 1.0:
				return_code, new_sim_time = sim.simxGetStringSignal( client_id, 'time', sim.simx_opmode_blocking)
				if return_code == sim.simx_return_remote_error_flag:
					print("[ERROR] Task 3 scene main script was tampered. Exiting ...")
					end_program()
					sys.exit()
				if new_sim_time == '':
					new_sim_time = '0'
				check = float(new_sim_time)


			# AFTER STARTING SIMULATION, CHECKING DYNAMICS AND MASS
			inputBuffer = bytearray()
			return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id, 'Disc_BM_2B',\
											sim.sim_scripttype_childscript,'dynamics_and_mass_check',[],[],[],inputBuffer,sim.simx_opmode_blocking)

			
			# Delay for stabilizing RTF and to check stability while evaluating 
			# 10 secs
			return_code, init_sim_time = sim.simxGetStringSignal( client_id, 'time', sim.simx_opmode_blocking)
			check = 0
			while check <= 10.0:
				return_code, new_sim_time = sim.simxGetStringSignal( client_id, 'time', sim.simx_opmode_blocking)
				# print(return_code)
				if return_code == sim.simx_return_remote_error_flag:
					print("\n[ERROR] It seems simulation was stopped in between. Exiting ...")
					end_program()
					sys.exit()
				check = float(new_sim_time) - float(init_sim_time)


			# Getting data from child script
			data_child = get_child_data()
			p = ",".join(data_child)
			output_list_child = p.split(',')

			# Getting EVAL data from child script
			eval_data_child = get_child_data_for_eval()
			p = ",".join(eval_data_child)
			output_list_child_eval = p.split(',')

			#  Stop simulation
			return_code = stop_simulation()
			end_real_time = time.time()

			# RTF calculation
			end_simulation_time = 0; rtf_python = 0
			return_code, end_simulation_time = sim.simxGetStringSignal(client_id, 'time', sim.simx_opmode_blocking)
			rtf_python = float("{0:.5f}".format(float(end_simulation_time)/(end_real_time - init_real_time)))
			print('\nCalculated Real-Time Factor (rtf) = ', rtf_python)
			if rtf_python >= 0.8:
				eval_rtf_python = 1
			else:
				eval_rtf_python = 0



			# This delay is necessary otherwise RTF is not received correctly
			# time.sleep(0.1)
			

			# Getting data from customization script
			data_customization = get_customization_data()
			p = ",".join(data_customization)
			output_list_custom = p.split(',')

			# Getting EVAL data from customization script
			eval_data_customization = get_customization_data_for_eval()
			p = ",".join(eval_data_customization)
			output_list_custom_eval = p.split(',')

			# This function will stop the simulation, call organize_screen_end, clear string signals, exit the server
			end_program()
	   
		else:
			print('score=',0)
			print('\n[ERROR] Failed connecting to Remote API server!')
			print('[WARNING] Make sure the CoppeliaSim software is running and')
			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
			# print('[ERROR] OR init_remote_api_server function is not configured correctly, check the code!')
			print()
			input('Press enter to exit')
			sys.exit()

	except KeyboardInterrupt:
			print('score=',0)
			print('\n[ERROR] Test script for Task 3 interrupted by user!')
			end_program()
			sys.exit()

	except Exception:
		print('score=',0)
		print('\nUh oh! An unknown ERROR occured.')
		print('Stop the CoppeliaSim simulation manually if started.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		end_program()
		sys.exit()


# Main function
try:
	if __name__ == '__main__':

		print("Keep CoppeliaSim opened with task_3_scene")


		task_3_cardinal_main()

		eval_no_of_joints = int(output_list_custom_eval[0])
		eval_vol          = int(output_list_custom_eval[1])
		torque            = output_list_custom_eval[2]
		force             = output_list_custom_eval[3]
		eval_rtf          = eval_rtf_python                                   # int(output_list_custom_eval[4])
		individual_values = output_list_custom_eval[5:]

		eval_all_dynamics = int(output_list_child_eval[0])
		eval_mass         = int(output_list_child_eval[1])

		no_of_joints      = output_list_custom[0]
		vol               = output_list_custom[1]
		rtf               = rtf_python                                        # output_list_custom[2]
		mass              = output_list_child[0]
		dynamics_not_enabled_list = output_list_child[1:]


		# print(eval_no_of_joints)
		# print(eval_vol)
		# print(eval_rtf)
		# print(eval_all_dynamics)
		# print(eval_mass)
		task_data_dict = {}
		print("\nChecking Constraints\n")
		score = 0
		if eval_no_of_joints:
			print("No. of joints          :    SATISFIED")
			task_data_dict['No. of joints']='SATISFIED'
			score+=20
		else:
			print("No. of joints          :    NOT SATISFIED")
			task_data_dict['No. of joints']='NOT SATISFIED'

		if eval_vol:
			print("Bounding Box Volume    :    SATISFIED")
			task_data_dict['Bounding Box Volume']='SATISFIED'
			score+=20
		else:
			print("Bounding Box Volume    :    NOT SATISFIED")
			task_data_dict['Bounding Box Volume']='NOT SATISFIED'

		print("Total Torque Required  :   ", torque, " Nm")
		task_data_dict['Total Torque Required']=str(torque) + " Nm"
		print("Total Force Required   :   ", force, " N")
		task_data_dict['Total Force Required ']=str(force) + " N"
		print("Torque/ Force required for individual joints in order: ", individual_values)
		task_data_dict['Torque/ Force required for individual joints in order:']=str(individual_values)
		
		if eval_rtf:
			print("RTF                    :    SATISFIED")
			task_data_dict['RTF']='SATISFIED'
			score+=20
		else:
			print("RTF                    :    NOT SATISFIED")
			task_data_dict['RTF']=' NOT SATISFIED'

		# print(eval_all_dynamics)
		if eval_all_dynamics:
			print("Dynamics enabled       :    SATISFIED")
			task_data_dict['Dynamics enabled']='SATISFIED'
			score+=20
		else:
			print("Dynamics enabled       :    NOT SATISFIED")
			task_data_dict['Dynamics enabled']='NOT SATISFIED'

		if eval_mass:
			print("Total Mass             :    SATISFIED")
			task_data_dict['Total Mass']='SATISFIED'
			score+=20
		else:
			print("Total Mass             :    NOT SATISFIED")
			task_data_dict['Total Mass']='NOT SATISFIED'
		print('score=',score)
		data = ['Task 3: DESIGNING']
		data.append(str(task_data_dict))
		data.append(str(score))
		push_to_sheet.send_to_sheets(data)


except KeyboardInterrupt:
	print('score=',0)
	print('\n[ERROR] Test script for Task 3 interrupted by user!')
	end_program()


except Exception:
	print('score=',0)
	print('\n[ERROR] An Exception occurred')
	print('Stop the CoppeliaSim simulation manually if started.\n')
	traceback.print_exc(file=sys.stdout)
	print()
	end_program()
	sys.exit()