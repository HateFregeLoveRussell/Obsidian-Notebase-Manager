{name: deliverable-relationship-obj, version: 1}
<%*	suggestions = ["Sub-Deliverable", "Super-Deliverable"]; 
	decision = await tp.system.suggester(suggestions, suggestions, false,"")
	tR += decision  + ": "
	 while (await tp.system.suggester(["Y","N"],[true,false],false,"Continue Adding Fields?")) {
		tR +=  "\n"
		suggestions.splice(suggestions.indexOf(decision),1);
		decision = await tp.system.suggester(suggestions, suggestions,false,"")
		tR += decision  + ": "
	} 

_%>