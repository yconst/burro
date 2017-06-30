//--- Model, Singleton

var Store = {
	data: {
		"image":"",
		"controls": {
			"angle":0,
			"yaw":0, 
			"throttle":0
		},
		"pilot": {
			"pilots":["None"], 
			"index":0
		},
		"record": false,
		"is_recording": false
	},
	updateData: function(data) {
		var dataCopy = Object.assign({}, this.data)
		for (var attrname in data) { dataCopy[attrname] = data[attrname] }
		this.data = dataCopy
	}
}

var waiting = false

//--- Dispatcher, Singleton

var Dispatcher = {
	set: function(payload, update_backend) {
		Store.updateData(payload.value)
		if (update_backend) {
			payload.action = "set"
			ws.send(JSON.stringify(payload))
			waiting = true
		}
		if (waiting == false) {
			m.redraw()
		}
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
		var payload = {"target": "data", "value": obj}
		Dispatcher.set(payload, false)

	    // Re-send data request
	    setTimeout(function() {
	    	var payload = {"target": "status", "action": "get"}
	    	ws.send(JSON.stringify(payload))
	    }, 100)
	    
	}
}
ws.onclose = function (event) {
	console.warn("Websocket close")
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
			var left = Math.min(Math.max(Store.data.controls.yaw, -1), 1)*50+50
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
		    		var payload = {"target": "pilot", "value": {"index" : Store.data.pilot.pilots.indexOf(value)}}
			    	Dispatcher.set(payload, true)
		    	}
		    ) }, [
		      	Store.data.pilot.pilots.map(function(name, index) {
		        	return m('option' + (Store.data.pilot.index === index  ? '[selected=true]' : ''), name)
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
					var payload = {"target": "record", "value": {"record" : checked}}
			    	Dispatcher.set(payload, true)
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

// Make primary container draggable
var draggie = new Draggabilly('#primaryContainer', {
	containment: '#container'
})

// Bind to window resize
window.onresize = function(event) {
    if (document.documentElement.clientWidth <= 920) {
    	draggie.disable()
    } else {
    	draggie.enable()
    }
}
