var task_backend = require('../backend/task_backend.js');
var resetfilepath = 'task5/task_5_startingArena.ttt'
var filepath = 'task5/task_5_trial.ttt'
var pythonfilepath = 'task5/task_5_eval.py'
var level = '5'
task_backend.run_task_backend(resetfilepath,filepath,pythonfilepath,level);