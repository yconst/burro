//--- Model, Singleton

var Store = {
	data: {
		"image":"",
		"yaw":0, 
		"throttle":0,
		"pilots":["None"], 
		"index":0,
		"record": false
	},
	updateData: function(data) {
		var dataCopy = Object.assign({}, this.data)
		for (var attrname in data) { dataCopy[attrname] = data[attrname]; }
		this.data = dataCopy
	}
}

var waiting = false

//--- Dispatcher, Singleton

var Dispatcher = {
	applyAction: function(action, update_backend) {
		if (action.action == 'update-data')
		{
			Store.updateData(action.value)
		}
		if (update_backend) {
			ws.send(JSON.stringify(action))
			waiting = true
		}
		if (waiting == false) {
			m.redraw()
		}
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

var ws = new WebSocket("ws://"+window.location.hostname+":80/api/v1/ws")
ws.onopen = function (event) {
	console.log("Websocket open")
}
ws.onmessage = function (event) {
	obj = JSON.parse(event.data)
	if (obj.ack == "ok") {
		// Ack
		console.log("Received Ack")
		waiting = false
		m.redraw()
	}
	else if (obj.test) {
		// Settings
	}
	else if (obj.image) {
		// Status
		var action1 = Action("image", "update-data", {"image" : obj.image})
	    Dispatcher.applyAction(action1, false)
	    var action2 = Action("command", "update-data", obj.controls)
	    Dispatcher.applyAction(action2, false)
	    var action3 = Action("pilot", "update-data", obj.pilot)
	    Dispatcher.applyAction(action3, false)
	    var action3 = Action("record", "update-data", {"record" : obj.record})
	    Dispatcher.applyAction(action3, false)

	    // Re-send data request
	    setTimeout(function() {
	    	ws.send(JSON.stringify(Action("", "get", "status")))
	    }, 100)
	    
	}
}
ws.onclose = function (event) {
	console.log("Websocket close")
}

//--- View, Factory

var ImageView = function() {
	return {
		view: function() {
			return m("img", {class:"viewport", src:"data:image/jpeg;base64," + Store.data.image})
		}
	}
}

var CommandView = function() {
	return {
		view: function() {
			var left = Math.min(Math.max(Store.data.yaw, -1), 1)*50+50
			return m( "div", {class:"sliderBox"}, 
				m("div", {class:"sliderKnob", style:"left:" + left + "%;"}) 
			)
		}
	}
}

var PilotsView = function() {
	return {
		view: function (ctrl) {
		    return m('select', { 
		    	onchange: m.withAttr('value', function(value) {
			    	var action = Action("pilot", "update-data", {"index" : Store.data.pilots.indexOf(value)})
			    	Dispatcher.applyAction(action, true)
		    	}
		    ) }, [
		      	Store.data.pilots.map(function(name, index) {
		        	return m('option' + (Store.data.index === index  ? '[selected=true]' : ''), name)
		      	})
		    ])
		}
	}
}

var RecordBox = function() {
	return {
		view: function(ctrl) {
			return m('input', {
				type: "checkbox", 
				class: "js-switch",
				checked: Store.data.record,
				onchange: m.withAttr('checked', function(checked) {
					var action = Action("record", "update-data", {"record" : checked})
			    	Dispatcher.applyAction(action, true)
				}) }, "Record")
		}
	}
}

var Veil = function() {
	return {
		view: function(ctrl) {
			var vis = waiting == true?"visible":"hidden"
			var style = "visibility:" + vis + ";"
			return m('div', {class:"veil", style:style},"")
		}
	}
}

// Mount elements
m.mount(document.getElementById("imageContainer"), ImageView)
m.mount(document.getElementById("sliderContainer"), CommandView)
m.mount(document.getElementById("pilotsContainer"), PilotsView)
m.mount(document.getElementById("recordBox"), RecordBox)
m.mount(document.getElementById("veilContainer"), Veil)

// ---
// Document References
// ---
// https://jsbin.com/xatavo/edit?html,js,output
