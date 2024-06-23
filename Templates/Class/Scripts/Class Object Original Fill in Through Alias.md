<%_* 
let candidates = app.vault.getMarkdownFiles().filter(x => "frontmatter" in app.metadataCache.getFileCache(x)).filter(x => x.basename !== tp.file.title)
	const {update} = app.plugins.plugins["metaedit"].api
	let alias = await tp.system.prompt("Insert Class Alias...", "", false, false)
	candidates = candidates.filter(x => ("class" in app.metadataCache.getFileCache(x).frontmatter))
	candidates = candidates.filter(x => app.metadataCache.getFileCache(x).frontmatter.class !== null)
	candidates = candidates.filter(x => !x.path.startsWith("Templates"))
	candidates = candidates.filter(x => typeof(app.metadataCache.getFileCache(x).frontmatter.class) != `string`)
	console.log(candidates)
	candidates = candidates.filter(x => "class-alias" in app.metadataCache.getFileCache(x).frontmatter.class)
	console.log(candidates)
	candidates = candidates.filter(x => app.metadataCache.getFileCache(x).frontmatter.class["class-alias"] === alias)
	console.log(candidates)
	if (candidates.isEmpty) {console.log("Empty Candidates")}
	if (!candidates.isEmpty) {
		let fm =  app.metadataCache.getFileCache(candidates[0]).frontmatter["class"]
		console.log(fm)
		//await update("class", JSON.stringify(fm),tp.file.find_tfile(tp.file.title))
		tR += JSON.stringify(fm,null,2).replace(/"([^"]+)":/g, '$1:')
	} 
_%>