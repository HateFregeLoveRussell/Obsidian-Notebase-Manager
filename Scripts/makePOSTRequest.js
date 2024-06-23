
async function makePOSTRequest(json, url, tp)
{
    console.log("Saving JSON")
    await saveJSON(json, tp)
    console.log("Making curl call")
    cmd = `curl -X POST -H "Content-Type: application/json" -d @POSTtransmissionData.json http://127.0.0.1:5000/${url}`
    const result = await sh(cmd, tp);
    return result;
}
async function sh(cmd, tp)
{
   const { promisify } = require('util');
   const exec = promisify(require('child_process').exec);
   const relative = await tp.file.path(true)
   const absolute = await tp.file.path()
   const scriptsAbsolute = absolute.substring(0, (absolute.length - relative.length)) + "Scripts/"
   cmd = `cd ${scriptsAbsolute} & ${cmd}`
   console.log(cmd)
   const result = await exec(cmd);
   return {out: result.stdout.trim(), err: result.stderr.trim()};
}
function saveJSON(jsonData, tp) {
    jsonString = JSON.stringify(jsonData)
    const relative = tp.file.path(true)
    const absolute = tp.file.path()
    const scriptsAbsolute = absolute.substring(0, (absolute.length - relative.length)) + "Scripts/"
   
    var fs = require('fs');
    console.log(`writing location: ${scriptsAbsolute}/POSTtransmissionData.json`)
    fs.writeFile(`${scriptsAbsolute}/POSTtransmissionData.json`, jsonString, function(err) {
        if (err) {
            console.log(err);
        }
    });
}
module.exports = makePOSTRequest;