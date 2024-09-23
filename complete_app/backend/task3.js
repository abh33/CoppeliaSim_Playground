var task_backend = require('../backend/task_backend.js');
var resetfilepath = 'task3/task_3_startingArena.ttt'
var filepath = 'task3/task_3_trial.ttt'
var pythonfilepath = 'task3/task_3_eval.py'
var level = '3'
task_backend.run_task_backend(resetfilepath,filepath,pythonfilepath,level);