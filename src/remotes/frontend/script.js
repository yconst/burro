//--- Model, Singleton

var ImageData = {
	data: "",
	updateData: function(data) {
		this.data = data
	}
}

var CommandData = {
	data: {"yaw":0, "throttle":0},
	updateData: function(data) {
		this.data = data
	}
}

var PilotData = {
	data: {"pilots":["None"], "pilot_index":0},
	updateData: function(data) {
		this.data = data
	},
	updateIndex: function(data) {
		m.request({
		    method: "POST",
		    url: "/api/v1/setpilotindex",
		    data: data
		})
		.then(function(result) {
		    var dataCopy = Object.assign({}, this.data)
			dataCopy["pilot_index"] = data["index"]
			this.data = dataCopy
		})
	}
}

var OptionsData = {
	data: {"record": false},
	updateData: function(data) {
		m.request({
		    method: "POST",
		    url: "/api/v1/setoptions",
		    data: data
		})
		.then(function(result) {
		    var dataCopy = Object.assign({}, this.data)
			dataCopy["record"] = data["record"]
			this.data = dataCopy
		})
	}
}

//--- Dispatcher, Singleton

var Dispatcher = {
	applyAction: function(action) {
		if (action.target == 'image')
		{
			if (action.action == 'update-data')
			{
				ImageData.updateData(action.value)
			}
		}
		else if (action.target == 'command')
		{
			if (action.action == 'update-data')
			{
				CommandData.updateData(action.value)
			}
		}
		else if (action.target == 'pilot')
		{
			if (action.action == 'update-data')
			{
				PilotData.updateData(action.value)
			}
			if (action.action == 'update-index')
			{
				PilotData.updateIndex(action.value)
			}
		}
		else if (action.target == 'options')
		{
			if (action.action == 'update-data')
			{
				OptionsData.updateData(action.value)
			}
		}
		m.redraw()
	}
}

//--- Actions, Constructor

var Action = function(target, action, data) {
	return {
		target: target,
		action: action,
		value: data
	}
}

//--- API, Singleton

var AjaxAPI = {
	address: '',
	start: function() {
		var that = this
		this.intervalID = setInterval(function(){
			that.update()
		}, 200)
	},
	stop: function() {
		clearInterval(this.intervalID)
	},
	update: function() {
		m.request({
		    method: "GET",
		    url: "/api/v1/status"
		})
		.then(function(result) {
		    var action1 = Action("image", "update-data", result.image)
		    Dispatcher.applyAction(action1)
		    var action2 = Action("command", "update-data", {"yaw" : result.yaw, "throttle" : result.throttle})
		    Dispatcher.applyAction(action2)
		    var action3 = Action("pilot", "update-data", {"pilots" : result.pilots, "selected_pilot" : result.selected_pilot})
		    Dispatcher.applyAction(action3)
		})
	}
}

//--- View, Factory

var ImageView = function() {
	return {
		view: function() {
			return m("img", {class:"viewport", src:"data:image/jpeg;base64," + ImageData.data})
		}
	}
}

var CommandView = function() {
	return {
		view: function() {
			var left = Math.min(Math.max(CommandData.data.yaw, -1), 1)*50+50
			return m( "div", {class:"sliderBox"}, 
				m("div", {class:"sliderKnob", style:"left:" + left + "%;"}) 
			)
		}
	}
}

var PilotsView = function() {
	return {
		view: function (ctrl) {
		    return m('select', { onchange: m.withAttr('value', function(value) {
		    	var action = Action("pilot", "update-index", {"index" : PilotData.data.pilots.indexOf(value)})
		    	Dispatcher.applyAction(action)
		    }) }, [
		      	PilotData.data.pilots.map(function(name) {
		        	return m('option', name)
		      	})
		    ])
		}
	}
}

var RecordBox = function() {
	return {
		view: function(ctrl) {
			return m('input', {type: "checkbox", onchange: m.withAttr('value', function(value) {
				var action = Action("options", "update-data", {"record" : value})
		    	Dispatcher.applyAction(action)
			}) }, "Record")
		}
	}
}

m.mount(document.getElementById("imageContainer"), ImageView)
m.mount(document.getElementById("sliderContainer"), CommandView)
m.mount(document.getElementById("pilotsContainer"), PilotsView)
m.mount(document.getElementById("recordBoxContainer"), RecordBox)
AjaxAPI.start()