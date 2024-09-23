var task_backend = require('../backend/task_backend.js');
var resetfilepath = 'task1/task_1_startingArena.ttt'
var filepath = 'task1/task_1_trial.ttt'
var pythonfilepath = 'task1/task_1_eval.py'
var level = '1'
task_backend.run_task_backend(resetfilepath,filepath,pythonfilepath,level);