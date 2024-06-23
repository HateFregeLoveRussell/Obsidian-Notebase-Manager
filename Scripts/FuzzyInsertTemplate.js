next_5 = '    --------------------Next 5--------------------'
exit = '  -----------------------Exit-----------------------'
function abbreviatePath(relativePath, maxPartLength = 4) {
  const parts = relativePath.split("\\");
  const abbreviatedParts = parts.map((part, index) => {
    if (index === parts.length - 1) {
      // Keep the last part (file name) intact
      return part;
    } else {
      // Abbreviate directory names if they exceed maxPartLength
      const abbreviatedPart = part.length > maxPartLength ? part.substr(0, maxPartLength) + "." : part;
      return abbreviatedPart;
    }
  });
  return abbreviatedParts.join("\\");
}


function treatSuggesterItems(item){
  if (item != exit && item != next_5){
    return (`Path: ${abbreviatePath(item.path)} \nName: ${item.name} \nVersion: ${item.version}
    ---------------Confidence: ${item.confidence}---------------`)
  }
  else {
    return (item)
  }
}

async function insertTemplate(tp, decision){
  tfile = tp.file.find_tfile(decision.path)
  contentJSON = await tp.user.makePOSTRequest({"path": decision.path,}, 'getTemplateContent', tp);
  contentJSON = JSON.parse(contentJSON.out)
  console.log(contentJSON)
  if (contentJSON.type == 'object'){
    fm = JSON.parse(contentJSON.content.replace(/'/g, '"'))
    fm = JSON.stringify(fm,null,2).replace(/"([^"]+)":/g, '$1:')
    return fm
  } else {
    fm = contentJSON.content
    return fm
  }
}


async function FuzzyInsertTemplate(tp) {
  response = await tp.system.prompt("Input Template Name...", null, false, false)
  if (response == null) {return}
  lowerBound = 0
  upperBound = 5
  first_iter = true

  while (true) {
    querryjson = await tp.user.makePOSTRequest({"value": response, "bounds": [lowerBound, upperBound]}, 'fuzzyMatch/templateSearch', tp);
    querryjson = JSON.parse(querryjson.out)
    console.log(querryjson)
    querrylist = Object.keys(querryjson).map(key => ({
      path: key,
      name: querryjson[key].name,
      version: querryjson[key].version,
      confidence: querryjson[key].FuzzyMatch
    }))
    if (querrylist.length == 0) {console.log("There are No More Entries To Display");return ""}
    if (querrylist.filter(dict => dict.confidence == 100).length == 1 && first_iter) {
      returnvalue = await insertTemplate(tp, querrylist.filter(dict => dict.confidence == 100)[0])
      return returnvalue
    }
    querrylist[querrylist.length] = next_5
    querrylist[querrylist.length] = exit
    //console.log(querrylist)
    decision = await tp.system.suggester(((item) => treatSuggesterItems(item)), querrylist)
    if (decision == null) {return ""}
    if (decision == exit){
      return ""
    } else if (decision != next_5) {
      returnValue = await insertTemplate(tp, decision)
      return returnValue
    } 
    lowerBound += 5
    upperBound += 5
    first_iter = false
  }
}

module.exports = FuzzyInsertTemplate