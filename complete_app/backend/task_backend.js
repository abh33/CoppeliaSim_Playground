const {shell} = require('electron');
const { execSync } = require('child_process')
var fs = require('fs');
const {BrowserWindow} = require('@electron/remote')
const dialog = require('@electron/remote').dialog
const ipc = require('electron').ipcRenderer;
const util = require('../backend/utilityFunctions')
module.exports = {                                                                  //backend for all tasks is implemented into one exporatable module function
    run_task_backend : function(resetfilepath,filepath,pythonfilepath,level){       //each task script(js) file only needs to require and call this function with given arguments

        const win2 = new BrowserWindow({show:false,frame:false, resizable:false,                    //temporary loading window
            width:192,
            height:108 });
        win2.loadFile("frontend/loading.html")

        function conf(message,detail){
            //displays a confirmation dialog box consisting give parameters
            //returns the clicked response
            let response = dialog.showMessageBoxSync( {
                type: 'question',
                buttons: ['Yes', 'No'],
                title: 'Confirm',
                message: message,
                detail: detail});
            return response;
            }

        function update(saveData,latestScore,bestScore){
            //updates the html file with appropriate stars and scores
            //updates the 'dataStore.json' file with saveData
            //this function is called everytime there is any change in saveData

            //update scores
            var latestScore_star = parseInt(latestScore/20);          //1 star for 20 score
            var bestScore_star = parseInt(bestScore/20);
            if (latestScore>=98){latestScore_star=5}                  //5 star if score > 97
            if (bestScore>=98){bestScore_star=5}
            if (latestScore>0){
                document.getElementById('latest-score').innerHTML = latestScore }    //set score in html only if score is +ve
            else{
                document.getElementById('latest-score').innerHTML = 0}               //else set score in html as 0
            if (bestScore>0){
                document.getElementById('best-score').innerHTML = bestScore}
            else{
                document.getElementById('best-score').innerHTML = 0}

            //update stars
            for (let i = 1; i <= latestScore_star; i++) {
                let starImg = 'lstar'.concat(i)
                document.getElementById(starImg).src="../frontend/resources/star.png";}
            for (let i = 1; i <= bestScore_star; i++) {
                let starImg = 'bstar'.concat(i)
                document.getElementById(starImg).src="../frontend/resources/star.png";}

            //update 'dataStore.json'
            var jsonData = JSON.stringify(saveData);
            fs.writeFileSync(util.getPath('dataStore.json'), jsonData, function(err) {
                if (err) {
                    console.error(err);}})}
        
        //INITIALIZE
        var dev='';
        if(!(process.argv[3].indexOf('app.asar') === -1)){var dev = 'resources.'} //set dev as 'resources.' only if app is run during production, as file paths change after buiding app(this will be later concatinated with filepath)
        var saveData = require(util.getPath('dataStore.json'))                      //load save data from 'dataStore.json' file
        if(saveData['server'+level]==true){                                         //if 'visual stream server on' bool of given level is true
            document.getElementById("demo").src = 'http://127.0.0.1:23020';}        //set src to visual stream server link
        var tries = saveData['tries'+level]
        var latestScore = saveData['latestScore'+level];
        var bestScore = saveData['bestScore'+level];
        if (tries==-1){                                                             //if walkthrough/solution enabled
            var penalty=-20}                                                        //set penalty to -20(i.e -1 star)
        else{
            var penalty=0}                                                          //else no penalty
        update(saveData,latestScore,bestScore);                                     //update all data

        //create scene folder
        var sceneFilePath = __dirname.substring(0,3)+'CoppeliaSim Playground/Themes/Fruit Plucking Robot/Scene Files/task'+level+'/task_'+level+'.ttt'
        if(!fs.existsSync(sceneFilePath)){
            fs.mkdirSync(__dirname.substring(0,3)+'CoppeliaSim Playground/Themes/Fruit Plucking Robot/Scene Files/task'+level,{recursive:true})
            fs.copyFileSync(util.getPath(filepath),sceneFilePath)}

        //BUTTON EVENTS
        //each event listener pushes the click data to 'clickStreamData.json'
        var but = document.getElementById('eyantra')
        but.addEventListener('click',(_)=>{                                     //on click
            clickStrmData = require(util.getPath('clickStreamData.json'))
            clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Eyantra Logo\']'].toString())    //push click data to 'clickStreamData.json'
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})
        })
        var but = document.getElementById('back')
        but.addEventListener('click',(_)=>{
            clickStrmData = require(util.getPath('clickStreamData.json'))
            clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Back(from Level-'+level+')\']'].toString())
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})
            location.replace('screen_5.html')
        })
        var but = document.getElementById('task-desc')
        but.addEventListener('click',(_)=>{
            clickStrmData = require(util.getPath('clickStreamData.json'))
            clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level-'+level+' Description\']'].toString())
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})
        })
        var but = document.getElementById('guide-me')
        but.addEventListener('click',(_)=>{
            clickStrmData = require(util.getPath('clickStreamData.json'))
            clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level-'+level+' Guide Me\']'].toString())
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})
        })

        //EVALUATE
        const evaluate = document.getElementById('evaluate');
        evaluate.addEventListener('click', function(_){       //On Click
            var msg = 'Make sure to open scene befor starting Evaluation.\nAlso make sure no other scene is Open to avoid any conflit\nDo not pause the simulation during Evaluation.'
            response = conf('Evaluate:',msg);                 //take confirmation from user for evaluation
            if (response == 0){                               //if confirmed
                console.log('Evaluation Starting...')
                win2.show()                                                     //display loading window     
                var _ = ipc.sendSync('lock-window');                            //disable main window

                clickStrmData = require(util.getPath('clickStreamData.json'))           //push clickstream data to 'clickStreamData.json'
                clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Evaluate\']'].toString())
                fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})

                var data = execSync('python '+util.getPath(pythonfilepath)).toString();         //execute task evaluation python file using child process
                console.log((data))                                                             //log output data of evaluation to console
                console.log('Guide me Penalty=',penalty)

                win2.hide()                                                             //hide loading window
                var _ = ipc.sendSync('unlock-window');                                  //enable main window

                var index = data.search('score=')                            //extract score from task output data
                var score = '';
                for (let i = index+6; i <= index+11; i++) {
                    score = score.concat(data.charAt(i))}
                var latestScore = parseInt(score)+penalty;                   //add penalty to score

                if(latestScore>bestScore){
                    bestScore = latestScore;}                           //set bestScore
                if (index==-1){
                    latestScore=0}                                      //if evaluation failed, set latest score as 0
                else{
                    if(tries!=-1){tries++};                             //else increment tries
                    saveData['tries'+level]=tries;}                     //update all data
                saveData['latestScore'+level]=latestScore;
                saveData['bestScore'+level]=bestScore;
                update(saveData,latestScore,bestScore);}})
        
        //RESTART
        function levelRestart(){
            win2.show()                                                                       //display loading window
            var path1 = util.getPath(resetfilepath)
            var path2 = util.getPath(filepath)

            clickStrmData = require(util.getPath('clickStreamData.json'))                     //push clickstream data to 'clickStreamData.json'
            clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Restart\']'].toString())
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})

            fs.copyFile(path1, path2, () => {});                                              //copy reset scene file as scene file
            fs.copyFile(path1, __dirname.substring(0,3)+'CoppeliaSim Playground/sceneFiles/task'+level+'/task_'+level+'.ttt', () => {});

            saveData['latestScore'+level]=0;                                                  //update data
            saveData['bestScore'+level]=0;
            update(saveData,0,0);
            setTimeout(()=>{
            win2.hide();                                                                       //hide loading window
            location.replace('screen_5.html')},1000)}

        const restartButton = document.getElementById('restart');
        restartButton.addEventListener('click', function(_){              //On Click
            response = conf('Confirm Restart?','This will reset all the progress in the scene.')  //take confirmation from user for restart
            if (response == 0){                                                                   //if confirmed
                levelRestart()
                openScene()}})                                             //change main window location
        
        //OPEN SCENE
        function openScene(){
            win2.show()                                                                         //display loading window
            var _ = ipc.sendSync('lock-window');                                                //disable main window

            clickStrmData = require(util.getPath('clickStreamData.json'))                       //push clickstream data to 'clickStreamData.json'
            clickStrmData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Open Scene\']'].toString())
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})
            const ret = execSync('python -c "from '+dev+'backend.extraResources import openScene; openScene.open(r\''+sceneFilePath+'\')"').toString() //attempt to open file using sim.simxLoadScene using python(in case a scene is already open)
            var sceneOpenDelay = 3000                                //initialize sceneOpenDelay as 3 sec
            if (ret==0){                                             //if failed to open scene directly
                sceneOpenDelay = 10000                               //set sceneOpenDelay as 10 sec
                shell.openPath(sceneFilePath)}             //open scene using shell command
                                                                     //set timeout for sceneOpenDelay seconds
            setTimeout(()=>{                                         //on timeout
                saveData['server1']=false                            //set all visual stream server bools to false
                saveData['server2_1']=false
                saveData['server2_2']=false
                saveData['server3']=false
                saveData['server4']=false
                saveData['server5']=false
                saveData['server'+level] = true;                     //set current level visual stream server bool to true
                document.getElementById("demo").src = 'http://127.0.0.1:23020';   //start visual stream server in html
                update(saveData,saveData['latestScore'+level],saveData['bestScore'+level]);  //update save data
                },sceneOpenDelay)

            var _ = ipc.sendSync('unlock-window');                          //enable main window
            win2.hide()}                                                    //hide loading window
        const openSceneButton = document.getElementById('openScene');
        openSceneButton.addEventListener('click', function(_){            //On Click
            var response = conf('Open CoppeliaSim Scene?','Make sure no Other Scenes are Open before Opening this Scene.')  //take confirmation from user for opening scene
            if (response == 0){                                                                     //if confirmed
               openScene()}})
        
        //CONSOLE ON HTML
        //rewires all console.logs as an HTML element to display data on HTML
        rewireLoggingToElement(
            () => document.getElementById("log"),
            () => document.getElementById("log-container"), true);

        function rewireLoggingToElement(eleLocator, eleOverflowLocator, autoScroll) {
            fixLoggingFunc('log');
            // fixLoggingFunc('debug');
            // fixLoggingFunc('warn');
            fixLoggingFunc('error');
            // fixLoggingFunc('info');

            function fixLoggingFunc(name) {
                console['old' + name] = console[name];
                console[name] = function(...arguments) {
                    const output = produceOutput(name, arguments);
                    const eleLog = eleLocator();

                    if (autoScroll) {
                        const eleContainerLog = eleOverflowLocator();
                        const isScrolledToBottom = eleContainerLog.scrollHeight - eleContainerLog.clientHeight <= eleContainerLog.scrollTop + 1;
                        eleLog.innerHTML += output + "<br>";
                        if (isScrolledToBottom) {
                            eleContainerLog.scrollTop = eleContainerLog.scrollHeight - eleContainerLog.clientHeight;}} 
                    else {
                        eleLog.innerHTML += output + "<br>";}
                    console['old' + name].apply(undefined, arguments);};}

            function produceOutput(name, args) {
                return args.reduce((output, arg) => {
                    return output +
                        "<span class=\"log-" + (typeof arg) + " log-" + name + "\">" +
                            (typeof arg === "object" && (JSON || {}).stringify ? JSON.stringify(arg) : arg) +
                        "</span>&nbsp;";}, '');}}}}
