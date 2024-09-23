//IMPORTS
const {app, BrowserWindow} = require('electron');   
const { execSync } = require("child_process");      //used to execute python or any external programs in a command line
const dialog = require('electron').dialog           //used to display dialog boxes
require('@electron/remote/main').initialize()       //usage of normal electron module from renderer process is deprecated, hence electron/remote is installed
const path = require('path');
const fs = require('fs');                           //file system
const ipc = require('electron').ipcMain             //used for inter process communication between main and renderer process

//INITIALIZING
var dev='';
if(!(isDev())){var dev = 'resources.'} //set dev as 'resources.' only if app is run during production, as file paths change after buiding app(this will be later concatinated with filepath)

//Set-up Visual Streaming(add-on feature in Coppeliasim): we need to set autostart variable to 'true' in the add-on lua code file for this feature to autostart
try{
fs.copyFile(getPath('simAddOnVisualization stream.lua'),__dirname.substring(0,1)+':\\Program Files\\CoppeliaRobotics\\CoppeliaSimEdu\\simAddOnVisualization stream.lua',()=>{})}         //copy the edited lua file in the coppeliasim folder
catch(_){}


var internet = -1  //Initialize internet variable to -1(later will be used to determine online/offline mode for app)

//FUNCTIONS

function getDateAndTime(){
    // returns current data and time
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = date+' '+time;
    return dateTime;}

function getPath(fpath){
    //returns appropriate path to input file depending on whether app in run during developement or production
    if(isDev()){
        var filepath = path.join(__dirname, "backend/extraResources/");
        filepath = filepath.concat(fpath)} 
    else {
        var filepath = path.join(process.resourcesPath, "backend/extraResources/");
        filepath = filepath.concat(fpath)}
    return filepath}

function isDev() {
    //returns true if app is run during developement
    return __dirname.indexOf('AppData\\Local') == -1;}//true if current directory path does noy consist of production directory folder name

function clickStreamData(data){
    //pushes click stream data to google sheet by executing a python function(push_to_sheet.clickStreamData(data))
    //returns true if data was pushed successfully
    var returnCode=false;
    const ret = execSync('python -c "'.concat("from "+dev+"backend.extraResources.push_to_sheet import push_to_sheet; push_to_sheet.clickStreamData([".concat(data).concat("])\""))).toString()
    if (ret==1){
        returnCode=true}
    return returnCode}

function getSaveData(win){
    //loads save data from google sheet by executing a python function(push_to_sheet.getSaveData())
    // returns data if loaded succesfully else pops a confirmation box to reload/continue offline/quit
    var ret = execSync('python -c "from '+dev+'backend.extraResources.push_to_sheet import push_to_sheet; push_to_sheet.getSaveData()"').toString()
    if (ret==0){
        win.hide()
        message= 'Internet Connection Not Found!',
        detail= 'Make sure you are connected to Internet.'
        var response = conf(['Reload','Continue offline','Quit'],'No Internet Connection!',message,detail)
        if (response==0){win.show();var ret = getSaveData(win)} //call the function again if reload is clicked
        if (response==1){win.show();var ret = 1}                //offline mode
        else{var ret = 2}}
    return ret}

function conf(buttons,title,message,detail){
    //displays a confirmation dialog box consisting give parameters
    //returns the clicked response
    let response = dialog.showMessageBoxSync( {
        type: 'question',
        buttons: buttons,
        title: title,
        message: message,
        detail: detail});
    return response;}

function startMainProcess() {
    //app main process
    const win = new BrowserWindow({ //this is the main window
        show:false,
        width:1920,
        height:1080,
        webPreferences: {
            nodeIntegration: true,  //node integration is enabled for renderer processes(js scripts for html) to use node modules
            contextIsolation: false,//context isolation needs to be disabled for node integration
            //devTools: false
        }});

    require("@electron/remote/main").enable(win.webContents) //enables usage of electron remote for renderer processes in main window

    const win2 = new BrowserWindow({                  //this is temporary window shown when application is loading
        frame:false,
        alwaysOnTop:true,
        resizable:false,
        width:192,
        height:108 });
    win2.loadFile("frontend/loading.html")                                  //loading html file is loaded
    win2.once('ready-to-show',()=>{                                         //after window is ready
        var ret = getSaveData(win2);                                        //load save data from google sheet into ret
        if(ret==2){app.exit()}
        else{
        win.loadFile("frontend/screen_1.html")                              //load screen_1 html to main window
        win.once("ready-to-show",()=>{
            var clickStrmData = []
            clickStrmData.push([('[\''+getDateAndTime()+'\'').toString(),'\'Session Started\']'].toString())  //push final elements to clickstream data list
            fs.writeFile(getPath('clickStreamData.json'), JSON.stringify(clickStrmData),()=>{})
            win.show()                              //display main window
            win2.hide()});                          //hide loading window
        if (ret==1){internet=1}                                             //set global variable internet=1 if offline mode(i.e ret==1)
        else{fs.writeFile(getPath('dataStore.json'),ret, () => {})}}})       //else write dataStore json file with loaded data

    win.on('close', function (e) {                          //when main window is closed
        message= 'Do you want to save data?',
        detail= 'Make sure to manually close all opened scenes after exiting.'
        if (internet==1){                                   //if offline mode, show exit confirmation
            var response = conf(['Exit','Cancel'],'Confirm','Are you sure you want to Exit?','Data will not be saved in offline mode.')
            if(response == 1) {e.preventDefault()}
            else{
                var saveData = require(getPath('dataStore.json'))                   //load save data dictionary from 'dataStore.json'
                saveData['server1']=false                                           //set 'visual stream server on' bools for all task to false
                saveData['server2_1']=false
                saveData['server2_2']=false
                saveData['server3']=false
                saveData['server4']=false
                saveData['server5']=false
                //update 'dataStore.json'
                var jsonData = JSON.stringify(saveData);
                fs.writeFileSync(getPath('dataStore.json'), jsonData, (_)=>{})
                app.exit()}}
        else{                                               //else, show save data confirmation
            var response = conf(['Save', 'Don\'t Save','Cancel'],'Confirm',message,detail)

            if(response == 2) {e.preventDefault()}                                  //if cancel is clicked prevent app exit

            else if(response == 0){                                                 //if save is clicked

                win2.show()                                                         //show loading window
                var clickStrmData = require(getPath('clickStreamData.json'))        //load clickstream data list from 'clickStreamData.json'
                var saveData = require(getPath('dataStore.json'))                   //load save data dictionary from 'dataStore.json'
                saveData['server1']=false                                           //set 'visual stream server on' bools for all task to false
                saveData['server2_1']=false
                saveData['server2_2']=false
                saveData['server3']=false
                saveData['server4']=false
                saveData['server5']=false

                var _ = execSync('python -c "from '+dev+'backend.extraResources.push_to_sheet import push_to_sheet; push_to_sheet.saveData(r\''+(JSON.stringify(saveData))+'\')"')  //pushes savedata to google sheets by calling python function(push_to_sheet.saveData(saveData))

                clickStrmData.push([('[\''+getDateAndTime()+'\'').toString(),'\'Session Ended\']'].toString())  //push final elements to clickstream data list
                clickStrmData.push(['[\'***\'','\'***\']'].toString())
                var returnCode = clickStreamData(clickStrmData)                                                 //push click stream data to google sheets
                while (returnCode==false){                                                                      //while failed to push to google sheets
                    win2.hide()
                    message= 'Failed to Save data!',
                    detail= 'Make sure you are connected to Internet.'
                    var response = conf(['Retry','Don\'t Save'],'No Internet Connection!',message,detail)       //display confirmation box to retry/dont save
                    if (response==0){win2.show();var returnCode = clickStreamData(clickStrmData);}              
                    if (response==1){returnCode=true}}
                win2.close()
                app.exit()}
            else{                                               //else dont save clicked
                win2.close();
                app.exit()}                                     //exit without saving
            }});

    ipc.on('lock-window',function(event){           //disables main window when called from a renderer process
        win.setEnabled(false)
        event.returnValue='window-locked'})

    ipc.on('unlock-window',function(event){         //enables main window when called from a renderer process
        win.setEnabled(true)
        event.returnValue='wincow-unlocked'})}      //end of main process funtion

//APP
app.whenReady().then(startMainProcess);