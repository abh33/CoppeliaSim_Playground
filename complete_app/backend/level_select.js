const fs = require('fs');
const util = require('../backend/utilityFunctions');

function save(saveData){
    var jsonData = JSON.stringify(saveData);
    fs.writeFile(util.getPath('dataStore.json'), jsonData, function(_) {})}

function update(bestScore,l){
    var  bscore = parseInt(bestScore/20);
    if (bestScore>=98){
        var bscore=5}
    for (let i = 1; i <= bscore; i++) {
        let starImg = ('bstar'.concat(i)).concat(l)
        document.getElementById(starImg).src="../frontend/resources/star.png";}}

var saveData = require(util.getPath('dataStore.json'))
var bestScore1 = saveData['bestScore1'];
var bestScore2_1 = saveData['bestScore2_1'];
var bestScore2_2 = saveData['bestScore2_2'];
var bestScore2 = (bestScore2_1+bestScore2_2)/2;
var bestScore3 = saveData['bestScore3'];
var bestScore4 = saveData['bestScore4'];
var bestScore5 = saveData['bestScore5'];
var quiz_done = saveData['quizDone']

update(bestScore1,1);
update(bestScore2,2);
update(bestScore3,3);
update(bestScore4,4);
update(bestScore5,5);

//BUTTON EVENTS
//each event listener pushes the click data to 'clickStreamData.json'
var msg = 'Complete previous level with atleast 3 \u2B50\u2B50\u2B50 to UNLOCK this level.'

var but = document.getElementById('eyantra')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Eyantra Logo\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})})
var but = document.getElementById('back')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Back(from Fruit Plucking Robot)\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_4.html')})

//level 1 is always unlocked
var lvl = document.getElementById('level-1')
lvl.addEventListener('click', function(_){ 
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 1\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_5_1.html');})

//level 2 is unlocked is level 1 score is greater than 60 or task is already attempted
if (bestScore1>=60 || bestScore2>0){
    const lvl = document.getElementById('level-2')
    lvl.addEventListener('click', function(_){ 
        csData = require(util.getPath('clickStreamData.json'))
        csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 2\']'].toString())
        fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
        location.replace('screen_5_2.html');
    })
}
else{
    const lvl = document.getElementById('level-2')
    lvl.addEventListener('click', function(_){
        confirm(msg)
    })
}
//level 3 is unlocked is level 2 score is greater than 60 or task is already attempted
if (bestScore2>=60 || bestScore3>0){
    const lvl = document.getElementById('level-3')
    lvl.addEventListener('click', function(_){ 
        csData = require(util.getPath('clickStreamData.json'))
        csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 3\']'].toString())
        fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
        location.replace('screen_5_3.html');})
}
else{
    const lvl = document.getElementById('level-3')
    lvl.addEventListener('click', function(_){
        confirm(msg)
    })
}
//level 4 is unlocked is level 3 score is greater than 60 or task is already attempted
if (bestScore3>=60 || bestScore4>0){
    const lvl = document.getElementById('level-4')
    lvl.addEventListener('click', function(_){ 
        csData = require(util.getPath('clickStreamData.json'))
        csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 4\']'].toString())
        fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
        location.replace('screen_5_4.html');})
}
else{
    const lvl = document.getElementById('level-4')
    lvl.addEventListener('click', function(_){
        confirm(msg)
    })
}
//level 5 is unlocked is level 4 score is greater than 60 or task is already attempted
if (bestScore4>=60 || bestScore5>0){
    const lvl = document.getElementById('level-5')
    if (quiz_done){
        lvl.addEventListener('click', function(_){ 
            csData = require(util.getPath('clickStreamData.json'))
            csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Level 5\']'].toString())
            fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
            location.replace('screen_5_5.html');})
    }
    else{
        quiz_done=true
        saveData['quizDone']=true
        save(saveData)
        lvl.addEventListener('click', function(_){ location.replace('theme_quiz.html');})
    }
}
else{
    const lvl = document.getElementById('level-5')
    lvl.addEventListener('click', function(_){
        confirm(msg)
    })
}
