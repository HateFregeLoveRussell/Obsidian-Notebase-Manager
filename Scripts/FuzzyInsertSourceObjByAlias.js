next_5 = '    --------------------Next 5--------------------'
exit = '  -----------------------Exit-----------------------'

function treatSuggesterItems(item){
    if (item !== exit && item !== next_5){
        return (`Alias: ${(item['source_alias'])} 
    ---------------Confidence: ${item.confidence}---------------`)
    }
    else {
        return (item)
    }
}
async function FuzzyInsertTemplate(tp) {
    response = await tp.system.prompt("Input Source Alias...", null, false, false)
    if (response == null) {return}
    let lowerBound = 0
    let upperBound = 5
    let first_iter = true

    let querryjson;
    let querrylist;
    let returnvalue;
    let decision;
    while (true) {
        querryjson = await tp.user.makePOSTRequest({
            "value": response,
            "bounds": [lowerBound, upperBound]
        }, '/fuzzyMatch/SearchSourcesByAlias', tp);
        querryjson = JSON.parse(querryjson.out)
        console.log(querryjson)
        querrylist = Object.keys(querryjson).map(key => ({
            source: querryjson[key]['source'],
            source_alias: querryjson[key]['source-alias'],
            confidence: querryjson[key]['FuzzyMatch']
        }))
        if (querrylist.length === 0) {
            console.log("There are No Entries To Display");
            return ""
        }
        if (querrylist.filter(dict => dict.confidence === 100).length === 1 && first_iter) {
            returnvalue = querrylist.filter(dict => dict.confidence === 100)[0]['source']
            returnvalue = JSON.stringify(returnvalue,null,2).replace(/"([^"]+)":/g, '$1:')
            return returnvalue
        }
        querrylist[querrylist.length] = next_5
        querrylist[querrylist.length] = exit
        //console.log(querrylist)
        decision = await tp.system.suggester(((item) => treatSuggesterItems(item)), querrylist)
        if (decision == null) {
            return ""
        }
        if (decision === exit) {
            return ""
        } else;
        if (decision !== next_5) {
            returnvalue = decision['source']
            returnvalue = JSON.stringify(returnvalue,null,2).replace(/"([^"]+)":/g, '$1:')
            return returnvalue
        }
        lowerBound += 5
        upperBound += 5
        first_iter = false
    }
}

module.exports = FuzzyInsertTemplate
// const mdc = app.metadataCache
// const file = tp.file.find_tfile(tp.file.title)
// const {update} = app.plugins.plugins["metaedit"].api
// let candidates = app.vault.getMarkdownFiles().filter(x => "frontmatter" in mdc.getFileCache(x)).filter(x => x.basename !== tp.file.title)
// candidates = candidates.filter(x => !x.path.startsWith("Templates"))
//
// candidates = candidates.filter(x => ("source" in mdc.getFileCache(x).frontmatter))
// candidates = candidates.filter(x => mdc.getFileCache(x).frontmatter.source !== null)
//
// console.log(`The following are all candidates containing a non-null source field: `)
// console.log(candidates)
//
// let sources = []
// candidates.forEach(
//     function (e) {
//         let source = mdc.getFileCache(e).frontmatter.source
//         if (Array.isArray(source)) {
//             source.forEach(x => this.push(x), this)
//         } else {
//             this.push(source)
//         }
//     }, sources
// )
//
// let alias = await tp.system.prompt("Insert Class Alias...", "", false, false)
//
// sources = sources.filter(x => x["source-alias"] === alias)
//
// console.log(`The following are all candidates containing alias: `)
// console.log(sources)
//
// if (candidates.isEmpty) {console.log("Empty Candidates")}
// else {
//     let fm = sources[0]
//     let fileSource = mdc.getFileCache(file)
//     if ("frontmatter" in fileSource) {
//         fileSource = fileSource.frontmatter
//         console.log("frontmatter exists")
//         if ("source" in fileSource) {
//             console.log("Source Field Exists but may be null")
//             console.log(`${fileSource}`)
//             if (fileSource.source != null) {
//                 fileSource = fileSource.source
//                 console.log("Source Entry Exists")
//                 if(Array.isArray(fileSource)) {
//                     await update("source",JSON.stringify(fileSource.push(fm),null,2).replace(/"([^"]+)":/g, '$1:'),file)
//                     new Notice (tp.file.title + " - Source Field Updated",4000)
//                 } else {
//                     await update("source",JSON.stringify(new Array(fileSource, fm),null,2).replace(/"([^"]+)":/g, '$1:'),file)
//                     new Notice (tp.file.title + " - Source Field Updated",4000)
//                 }
//             } else {
//                 await update("source", JSON.stringify(fm,null,2).replace(/"([^"]+)":/g, '$1:'),file)
//                 new Notice (tp.file.title + " - Source Field Added",4000)
//             }
//         } else {
//             console.log("Source Does not exist")
//             newFileContent = tp.file.content.split("\n")
//             newFileCOntent = newFileContent.splice(1,0, `source: ${JSON.stringify(fm)}`)
//             console.log(newFileContent)
//             await app.vault.modify(file, newFileContent.join("\n"))
//             new Notice (tp.file.title + " - Source Field Added",4000)
//         }
//     } else {
//         new Notice (tp.file.title + " - No Frontmatter Found",4000)
//     }
// }
