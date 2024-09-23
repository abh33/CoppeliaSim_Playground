const util = require('../backend/utilityFunctions')
const fs = require('fs')

//BUTTON EVENTS
//each event listener pushes the click data to 'clickStreamData.json'
var but = document.getElementById('fruit-plucking-robot')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Fruit Plucking Robot\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_4.html')
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
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Back(from theme-select)\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_2.html')
})
var but = document.getElementById('copsim')
but.addEventListener('click',(_)=>{
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Copsim Logo\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
})