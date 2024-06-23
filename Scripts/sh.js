// In: cmd = a complete command to run in the command line shell. It is up 
//           to the user to make certain the command is properly formatted 
//           for their platform
// Out: an object with two properties:
//      out = the trimmed content the command sent to standard out.
//      err = the trimmed content the command sent to standard error.
async function sh(cmd, tp)
{
   const { promisify } = require('util');
   const exec = promisify(require('child_process').exec);
   const relative = await tp.file.path(true)
   const absolute = await tp.file.path()
   const scriptsAbsolute = absolute.substring(0, (absolute.length - relative.length)) + "Scripts/Python/"
   cmd = `cd ${scriptsAbsolute} & ${cmd}`
   console.log(cmd)
   const result = await exec(cmd);
   return {out: result.stdout.trim(), err: result.stderr.trim()};
}
module.exports = sh;