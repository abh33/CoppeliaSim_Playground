const util = require('../backend/utilityFunctions')
const dialog = require('@electron/remote').dialog
const fs = require('fs');

module.exports = {run_guideme_backend : function(filepath,level){           //backend for all tasks is implemented into one exporatable module function

    function update(saveData){
        //updates the 'dataStore.json' file with saveData
        var jsonData = JSON.stringify(saveData);
        fs.writeFile(util.getPath('dataStore.json'), jsonData, (_)=>{})}

    function conf(message,detail){
        //displays a confirmation dialog box consisting give parameters
        //returns the clicked response
        let response = dialog.showMessageBoxSync( {
            type: 'question',
            buttons: ['Yes', 'No'],
            title: 'Confirm',
            message: message,
            detail: detail});
        return response;}
    
    //INITIALIZE
    var saveData = require(util.getPath('dataStore.json'))
    var tries = saveData['tries'+level]

    if (tries>=3 || tries==-1){                                     //if more than 3 tries or walkthrough already unlocked
        const sol = document.getElementById('walkthrough')
        sol.addEventListener('click', function(e){                  //onclick
            var det = 'Viewing the solution will deduct a \u2B50 from you total score for this task.'
            var msg = 'Are you sure you want to view the solution?'
            if (tries>=3){                                          //if walkthrough opened first time
            var response = conf(msg,det);                           //take confirmation from user to open walkthrough
                if (response == 0){                                     //if confirmed

                    csData = require(util.getPath('clickStreamData.json'))                  //push clickstream data to 'clickStreamData.json'
                    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Walkthrough\']'].toString())
                    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})

                    var bestScore = saveData['bestScore'+level]             //deduct score for current task as penalty
                    var latestScore = saveData['latestScore'+level]
                    bestScore = bestScore-20
                    latestScore = latestScore-20
                    saveData['tries'+level] = -1
                    saveData['bestScore'+level] = bestScore
                    saveData['latestScore'+level] = latestScore
                    update(saveData)                                        //update data
                    location.replace(filepath);}}                           //change window html file to walkthrough file
            else{location.replace(filepath);}})}                    //else normally change window html file to walkthrough file without score deduction
    else{                                                        //if tries less than 3
        var msg = 'Complete 3 tries to unlock solution'          //display message box
        const sol = document.getElementById('walkthrough')
        sol.addEventListener('click', function(_){
            confirm(msg)})}}}