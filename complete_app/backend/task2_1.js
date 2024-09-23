var task_backend = require('../backend/task_backend.js');
var resetfilepath = 'task2/subtask1/task_2_startingArena.ttt'
var filepath ='task2/subtask1/task_2_trial.ttt'
var pythonfilepath = 'task2/subtask1/task_2_eval.py'
var level = '2_1'
task_backend.run_task_backend(resetfilepath,filepath,pythonfilepath,level);