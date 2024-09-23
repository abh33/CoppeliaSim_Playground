const fs = require('fs');
const util = require('../backend/utilityFunctions')


//BUTTON EVENTS
//each event listener pushes the click data to 'clickStreamData.json'
var but = document.getElementById('theme_desc')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Theme Description\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_4_rules.html')
})
var but = document.getElementById('eyantra')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Eyantra Logo\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
})
var but = document.getElementById('back')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Back(from Fruit Plucking Robot)\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_3.html')
})
var but = document.getElementById('rulebook')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Rulebook\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
})
var but = document.getElementById('theme-quiz')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Theme-Quiz\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('./theme_quiz.html')
})
var but = document.getElementById('play')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Play\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_5.html')
})

//INITIALIZE
var saveData = require(util.getPath('dataStore.json'))
var bestScore1 = saveData['bestScore1'];
var bestScore2_1 = saveData['bestScore2_1'];
var bestScore2_2 = saveData['bestScore2_2'];
var bestScore2 = (bestScore2_1+bestScore2_2)/2;
var bestScore3 = saveData['bestScore3'];
var bestScore4 = saveData['bestScore4'];
var bestScore5 = saveData['bestScore5'];

//change progress bar color to crimson if level is completed
if (bestScore1>=60){
    document.getElementById('dot-1').style.backgroundColor = 'crimson'
    document.getElementById('bar-1').style.backgroundColor = 'crimson'
}
else{
    document.getElementById('dot-1').style.backgroundColor = 'gray'
    document.getElementById('bar-1').style.backgroundColor = 'gray'
}

if ((bestScore2+bestScore2_1)/2>=60){
    document.getElementById('dot-2').style.backgroundColor = 'crimson'
    document.getElementById('bar-2').style.backgroundColor = 'crimson'
}
else{
    document.getElementById('dot-2').style.backgroundColor = 'gray'
    document.getElementById('bar-2').style.backgroundColor = 'gray'
}

if (bestScore3>=60){
    document.getElementById('dot-3').style.backgroundColor = 'crimson'
    document.getElementById('bar-3').style.backgroundColor = 'crimson'
}
else{
    document.getElementById('dot-3').style.backgroundColor = 'gray'
    document.getElementById('bar-3').style.backgroundColor = 'gray'
}

if (bestScore4>=60){
    document.getElementById('dot-4').style.backgroundColor = 'crimson'
    document.getElementById('bar-4').style.backgroundColor = 'crimson'
}
else{
    document.getElementById('dot-4').style.backgroundColor = 'gray'
    document.getElementById('bar-4').style.backgroundColor = 'gray'
}

if (bestScore5>=60){
    document.getElementById('dot-5').style.backgroundColor = 'crimson'
}
else{
    document.getElementById('dot-5').style.backgroundColor = 'gray'
}