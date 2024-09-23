var fs = require('fs');
const util = require('../backend/utilityFunctions')

function update(saveData){
    var jsonData = JSON.stringify(saveData);
    fs.writeFile(util.getPath('dataStore.json'), jsonData, (_)=>{})
}

var but = document.getElementById('eyantra')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Eyantra Logo\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
})
var but = document.getElementById('back')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Back(from Level 2(select)\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_5.html')
})
var but = document.getElementById('stage-1')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 2.1\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_5_2_1.html')
})

var saveData = require(util.getPath('dataStore.json'));
var bestScore2_1 = saveData['bestScore2_1'];
var bestScore2_2 = saveData['bestScore2_2'];

if (bestScore2_1>=60 || bestScore2_2>0){
    const sub = document.getElementById('stage-2');
    sub.addEventListener('click', function(e){ 
        csData = require(util.getPath('clickStreamData.json'))
        csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 2.2\']'].toString())
        fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
        location.replace('screen_5_2_2.html');})
}
else{
    msg = 'Complete Subtask 1 with atleast 3 \u2B50\u2B50\u2B50 to UNLOCK this Subatask'
    const sub = document.getElementById('stage-2')
    sub.addEventListener('click', function(e){
        confirm(msg);
    })
}

update(saveData)