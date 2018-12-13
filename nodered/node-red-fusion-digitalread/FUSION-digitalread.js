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
	if (process.env.hasOwnProperty("RED_DEBUG") && process.env.RED_DEBUG.toLowerCase().indexOf("FUSION-dht11") >= 0)  {
		debugOption = true;
	}
// Detect platform type and adjust defaults accordingly
    if (require("os").platform() === "win32") {
        lineEnd = "\r\n";
    }

    function dht11InNode(config) {
        RED.nodes.createNode(this, config);

        // node configuration
		this.path = config.path;
        this.topic = config.topic;
		this.name = config.name;
		var node = this;

        node.status({fill:"yellow", shape:"ring", text:"disconnected"});

        // Process the input buffers assuming they are utf-8 strings. Generate
        // a new message for each line. Handles lines split across multiple data events
        node.stringBuffer = "";
        node.parser = function (data) {
            //WIP
            var value = data[5];
            if (debugOption) {
                node.log("Digital Read on " + node.path + " - received data");
            }
            var parts, i, buf, msg;
            node.stringBuffer = node.stringBuffer + value + "\n";
            parts = node.stringBuffer.split(lineEnd);
            for (i = 0; i < parts.length - 1; i += 1) {
                console.log(parts[i]);
                msg = {topic:node.topic + "Value: ", payload:parts[i]};
                node.send(msg); // send to different outputs
            }
            node.stringBuffer = parts[parts.length-1];
        };

        console.log(node.path);
        node.server = net.createConnection({path: node.path}, () =>  {
            // TODO: handshake and pin selection
            console.log(node.pin);
            var msg = "asdf" + node.pin + "jkl";
            node.server.write(msg);
            console.log("Digital Read init");
            if (debugOption) {
                node.log("Digital Read on " + node.path + " - client connected");
            }
        });
        node.server.on("data", node.parser);
        node.server.on("end", function() {
                node.log("Digital Read on " + node.path + " - client disconnected");
        });

        node.server.on('error', function (e) {
            // If the path exists, set status and retry at intervals
            if (e.code == 'EADDRINUSE') {
                if (debugOption) {
                    node.log("Digital Read: path " + node.path + " in use, retrying...");
                }
                node.status({fill:"red", shape:"ring", text:"Path in use"});
                setTimeout(function () {
                        node.server.close();
                        //node.server.listen(node.path);
                    }, 2000);
            }
        });

		node.on("close", function () {
            node.server.close();
            // Boot off anyone connected to the socket
            node.server.unref();
		});
    }

    // Register the node by name.
    RED.nodes.registerType("digitalread-in", digitalreadInNode);
};
