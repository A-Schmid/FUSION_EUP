/**
 * Copyright 2016 Maxwell Hadley
 * Copyright 2018 Andreas Schmid 
 *
 * Licensed under the BSD 2-clause license - see accompanying LICENSE file
 **/
 
module.exports = function(RED) {
    "use strict";

	var debugOption = false,
        lineEnd = "\n",
        net = require("net"),
        fs = require("fs");

// Set the ipc debug option from the environment variable
	if (process.env.hasOwnProperty("RED_DEBUG") && process.env.RED_DEBUG.toLowerCase().indexOf("FUSION-digitalwrite") >= 0)  {
		debugOption = true;
	}
// Detect platform type and adjust defaults accordingly
    if (require("os").platform() === "win32") {
        lineEnd = "\r\n";
    }

    function digitalwriteInNode(config) {
        RED.nodes.createNode(this, config);

        // node configuration
        this.path = config.path;
		this.id = config.id;
        this.topic = config.topic;
		this.name = config.name;
        this.pin = config.pin;
		var node = this;

        node.status({fill:"yellow", shape:"ring", text:"disconnected"});

        // Process the input buffers assuming they are utf-8 strings. Generate
        // a new message for each line. Handles lines split across multiple data events
        node.stringBuffer = "";
        node.parser = function (data) {
            /*
            //WIP
            // TODO constant for index?
            var value = data[6];
            if (debugOption) {
                node.log("Digital Write on " + node.path + " - received data");
            }
            var parts, i, buf, msg;
            node.stringBuffer = node.stringBuffer + value + "\n";
            parts = node.stringBuffer.split(lineEnd);
            for (i = 0; i < parts.length - 1; i += 1) {
                msg = {topic:node.topic + "Value: ", payload:parts[i]};
                node.send(msg); // send to different outputs
            }
            node.stringBuffer = parts[parts.length-1];
            */
        };

        node.server = net.createConnection({path: node.path}, () =>  {
            if (debugOption) {
                node.log("Digital Write on " + node.path + " - client connected");
            }
        });

        node.server.on("data", node.parser);

        node.server.on("end", function() {
                node.log("Digital Write on " + node.path + " - client disconnected");
        });

        node.server.on("ready", function() {
            // set pin direction
            var msg = Buffer.from([0xaa, 0x02, 0x00, node.id, 0x03, 0x00, node.pin, 0x01, 0x00]);
            node.server.write(msg);
        });
            
        node.server.on("connect", function() {
            node.status({fill:"green", shape:"ring", text:"connected"});
        });

        node.on("input", function (msg) {
            var value = msg.payload;
            if(value != 0) value = 1;
            console.log(value);
            var msg = Buffer.from([0xaa, 0x02, 0x00, node.id, 0x03, 0x01, node.pin, value, 0x00]);
            node.server.write(msg);
        });

		node.on("close", function () {
            node.status({fill:"yellow", shape:"ring", text:"disconnected"});
            //node.server.close();
            // Boot off anyone connected to the socket
            node.server.unref();
		});
    }

    // Register the node by name.
    RED.nodes.registerType("digitalwrite-in", digitalwriteInNode);
};
