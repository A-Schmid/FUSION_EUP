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
            var humi = data[5];
            var temp = data[6];
            //console.log("temp: " + data[5] + " humi: " + data[6]);
            if (debugOption) {
                node.log("DHT11 on " + node.path + " - received data");
            }
            var parts, i, buf, msgTemp, msgHumi;
            node.stringBuffer = node.stringBuffer + temp + "|" + humi + "\n";
            parts = node.stringBuffer.split(lineEnd);
            for (i = 0; i < parts.length - 1; i += 1) {
                buf = parts[i].split('|');
                console.log(buf);
                msgTemp = {topic:node.topic + "Temperature", payload:buf[0]};
                msgHumi = {topic:node.topic + "Humidity", payload:buf[1]};
                //msg = {topic:node.topic, payload:parts[i]};
                node.send([msgTemp, msgHumi]); // send to different outputs
            }
            node.stringBuffer = parts[parts.length-1];
        };

        node.server = net.createConnection({path: node.path}, () =>  {
            console.log("DHT11 init");
            if (debugOption) {
                node.log("DHT11 on " + node.path + " - client connected");
            }
        });
        node.server.on("data", node.parser);
        node.server.on("end", function() {
                node.log("DHT11 on " + node.path + " - client disconnected");
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
                        //node.server.listen(node.path);
                    }, 2000);
            }
        });

		node.on("close", function () {
            //node.server.close();
            // Boot off anyone connected to the socket
            node.server.unref();
		});
    }

    // Register the node by name.
    RED.nodes.registerType("DHT11-in", dht11InNode);
};
