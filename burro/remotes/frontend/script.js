//--- Model, Singleton

const Store = {
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
		"is_recording": false,
		"f_time": 0
	},
	updateData: function(data) {
		const dataCopy = Object.assign({}, this.data)
		for (let attrname in data) { dataCopy[attrname] = data[attrname] }
		this.data = dataCopy
	}
}

var waiting = false

//--- Dispatcher, Singleton

const Dispatcher = {
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

const ws = new WebSocket("ws://"+window.location.hostname+":80/api/v1/ws")
ws.onmessage = function (event) {
	obj = JSON.parse(event.data)
	if (obj.ack == "ok") {
		waiting = false
		m.redraw()
	}
	else if (obj.test) { /* TODO */ }
	else if (obj.image) {
		const payload = {"target": "data", "value": obj}
		Dispatcher.set(payload, false)
	    setTimeout(function() {
	    	const payload = {"target": "status", "action": "get"}
	    	ws.send(JSON.stringify(payload))
	    }, 100)
	    
	}
}

//--- Views, Factory

const ImageView =  {
	view: function() {
		return m("img", {class:"viewport", src:"data:image/png;base64," + Store.data.image})
	}
}

const CommandView = {
	view: function() {
		const classes = classNames({
		    sliderBox: true, 
		    record_enable: Store.data.record,
		    recording: Store.data.is_recording
		})
		const left = Math.min(Math.max(Store.data.controls.yaw, -1), 1) * 50 + 50
		return m( "div", {class: classes}, 
			m("div", {class:"sliderKnob", style:"left:" + left + "%;"}) 
		)
	}
}

const PilotsView = {
	view: function (ctrl) {
	    return m('select', { 
	    	onchange: m.withAttr('value', function(value) {
	    		const payload = {"target": "pilot", "value": {"index" : Store.data.pilot.pilots.indexOf(value)}}
		    	Dispatcher.set(payload, true)
	    	}
	    ) }, [
	      	Store.data.pilot.pilots.map(function(name, index) {
	        	return m('option' + (Store.data.pilot.index === index  ? '[selected=true]' : ''), name)
	      	})
	    ])
	}
}

const RecordBox = {
	view: function(ctrl) {
		return m('input', {
			type: "checkbox", 
			class: "js-switch",
			checked: Store.data.record,
			onchange: m.withAttr('checked', function(checked) {
				const payload = {"target": "record", "value": {"record" : checked}}
		    	Dispatcher.set(payload, true)
			}) }, "Record")
	}
}

const ThrottleValue = {
	view: function() {
		return m("span", Math.round((Store.data.controls.throttle * -1 + 0.00001) * 100) / 100)
	}
}

const FTimeValue = {
	view: function() {
		return m("span", Math.round((Store.data.f_time + 0.00001) * 1000) + " ms")
	}
}

const Veil = {
	view: function(ctrl) {
		const vis = waiting == true?"visible":"hidden"
		const style = "visibility:" + vis + ";"
		return m('div', {class:"veil", style:style},"")
	}
}

m.mount(document.getElementById("imageContainer"), ImageView)
m.mount(document.getElementById("sliderContainer"), CommandView)
m.mount(document.getElementById("pilotsContainer"), PilotsView)
m.mount(document.getElementById("recordBox"), RecordBox)
m.mount(document.getElementById("throttleValue"), ThrottleValue)
m.mount(document.getElementById("ftimeValue"), FTimeValue)
m.mount(document.getElementById("veilContainer"), Veil)

const draggie = new Draggabilly('#primaryContainer', { containment: '#container' })

window.onresize = function(event) {
    if (document.documentElement.clientWidth <= 920) {
    	draggie.disable()
    } else {
    	draggie.enable()
    }
}
