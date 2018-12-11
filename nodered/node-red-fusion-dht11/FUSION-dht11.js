/**
 * Copyright 2016 Maxwell Hadley
 * Modified by Andreas Schmid (2018)
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
            if (debugOption) {
                node.log("DHT11 on " + node.path + " - received data");
            }
            var parts, i, msg;
            node.stringBuffer = node.stringBuffer + data.toString('utf8');
            parts = node.stringBuffer.split(lineEnd);
            for (i = 0; i < parts.length - 1; i += 1) {
                msg = {topic:node.topic, payload:parts[i]};
                node.send(msg);
            }
            node.stringBuffer = parts[parts.length-1];
        };

        node.server = net.createConnection(function (connection) {
            if (debugOption) {
                node.log("DHT11 on " + node.path + " - client connected");
            }
            connection.on("data", node.parser);
            if (debugOption) {
                connection.on("end", function () {
                    if (debugOption) {
                        node.log("DHT11 on " + node.path + " - client disconnected");
                    }
                });
            }
        });
        node.server.on('error', function (e) {
            // If the path exists, set status and retry at intervals
            if (e.code == 'EADDRINUSE') {
                if (debugOption) {
                    node.log("DHT11: path " + node.path + " in use, retrying...");
                }
                node.status({fill:"red", shape:"ring", text:"Path in use"});
                setTimeout(function () {
                        node.server.close();
                        node.server.listen(node.path);
                    }, 2000);
            }
        });

		node.server.listen(node.path, function () {
            if (debugOption){
                node.log("DHT11 listening on " + node.path);
            }
                node.status({fill:"green", shape:"dot", text:"listening"})
            });

		node.on("close", function () {
            node.server.close();
            // Boot off anyone connected to the socket
            node.server.unref();
		});
    }

    // Register the node by name.
    RED.nodes.registerType("DHT11-in", dht11InNode);
};
