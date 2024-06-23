<%*
type = await tp.system.suggester(["HW", "Assignment", "Project", "Lab", "Quiz", "Exam"],["HW", "Assignment", "Project", "Lab", "Quiz", "Exam"],false)
tR += `{type: ${type}, `
if (type != "HW") {
	decision = await tp.system.suggester(["standard", "non-standard"],["standard", "non-standard"],false)
	tR += `grading: ${decision}, `
	tR += `weight: ` _%>
	<%_tp.file.cursor()_%>
<%_*
	tR += `, `	
} 
tR += `due: `
_%>
<%_tp.file.cursor()%>, alias: <%tp.file.cursor() _%>,  
<%_* tR += ` template: {name: deliverable-obj, version: 1}}` _%>


