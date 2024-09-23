const path = require('path')
module.exports = {
    getPath: function (fpath){
       //returns appropriate path to input file depending on whether app in run during developement or production
        if(process.argv[3].indexOf('app.asar') === -1){
            var filepath = path.join(__dirname, "../backend/extraResources/");
            filepath = filepath.concat(fpath)} 
        else {
            var filepath = path.join(process.resourcesPath, "backend/extraResources/");
            filepath = filepath.concat(fpath)}
        return filepath},

    getDateAndTime: function (){
        //return current date and time
        var today = new Date();
        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var dateTime = date+' '+time;
        return dateTime;}}