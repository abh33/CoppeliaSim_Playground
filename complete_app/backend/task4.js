var task_backend = require('../backend/task_backend.js');
var resetfilepath = 'task4/task_4_startingArena.ttt'
var filepath = 'task4/task_4_trial.ttt'
var pythonfilepath = 'task4/task_4_eval.py'
var level = '4'
task_backend.run_task_backend(resetfilepath,filepath,pythonfilepath,level);