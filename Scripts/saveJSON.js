function saveJSON(jsonData, tp) {
    jsonString = JSON.stringify(jsonData)
    console.log(`saved JSON: ${jsonString}`)
    const relative = tp.file.path(true)
    const absolute = tp.file.path()
    const scriptsAbsolute = absolute.substring(0, (absolute.length - relative.length)) + "Scripts/"
   
    var fs = require('fs');
    fs.writeFileSync(`${scriptsAbsolute}/transmissionData.json`, jsonString, function(err) {
        if (err) {
            console.log(err);
        }
    });
}
module.exports = saveJSON;