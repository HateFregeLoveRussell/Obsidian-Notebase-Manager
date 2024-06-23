async function ValidateNote( tp)
{
   const filePath = await tp.file.path(true)
   response = await tp.user.makePOSTRequest({"path": `../../${filePath}`}, 'validateNote', tp);
   response = JSON.parse(response.out)
   console.log(response)
   
}
module.exports = ValidateNote;