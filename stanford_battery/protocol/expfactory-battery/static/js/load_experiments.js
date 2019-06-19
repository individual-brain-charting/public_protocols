function loadjscssfile(filename, filetype){
	if (filetype == "js") {
		document.write('<script src =' + filename + '></script>')
	}
	else if (filetype = "css") {
		document.write('<link href =' + filename + ' rel="stylesheet" type="text/css">')
	}
}


/* Draws experiments randomly to fill up a certain amount of time. 
Completely avoids any knapsack type optimization and just stops 
when it can't find another experiment to add */

var experimentDraw = function(lst, time) {
	var time = time || "[SUB_TOTALTIME_SUB]"
	var return_list = []
	var total_time = 0
	while (total_time < time && lst.length > 0) {
		index = Math.floor(Math.random()*lst.length)
		if ((total_time + lst[index].time) < time) {
			total_time += lst[index].time
			return_list.push(lst[index].name)
		} 
		lst.splice(index,1)
	}
    return return_list
}

// full list of experiment names:
experiment_list = [SUB_EXPERIMENTTIMES_SUB]						
experiment_names = experimentDraw(experiment_list)


/* takes an experiment array and concatenates it with the array of each experiment \
identified in 'experiment_names' */
function cat_experiments(experiment_array) {
	for (i = 0; i < experiment_names.length; i++) {
		switch (experiment_names[i]) {
                [SUB_EXPERIMENTCONCAT_SUB]
		}
	}
}
