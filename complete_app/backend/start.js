const util = require('../backend/utilityFunctions')
const fs = require('fs')

const but = document.getElementById('start')
but.addEventListener('click',(_)=>{                             //push clickstream data to 'clickStreamData.json'
    csData = require(util.getPath('clickStreamData.json'))
    csData.push([('[\''+util.getDateAndTime()+'\'').toString(),'\'Start\']'].toString())
    fs.writeFile(util.getPath('clickStreamData.json'), JSON.stringify(csData),()=>{})
    location.replace('screen_2.html')
})