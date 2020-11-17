"use strict";

const express = require('express');

const app = express();
app.use(express.json());

const PORT = 8080;

const XMPP_SERVICE_URL = get_environment_variable("XMPP_SERVICE_URL",
    "ws://127.0.0.1:5280/xmpp-websocket");

const XMPP_DOMAIN = get_environment_variable("XMPP_DOMAIN", "localhost");


function get_environment_variable(varname, defaultvalue) {
    let result = process.env[varname];
    if (result !== undefined)
        return result;
    else
        return defaultvalue;
}

const generate_random_string = function () {
    const l = 5 + Math.floor(Math.random() * 5);
    const chars = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM";
    let str = "";
    for (let i = 0; i < l; i++) {
        const n = Math.floor(Math.random() * chars.length);
        str += chars.substr(n, 1);
    }
    return str;
};

// used to send a message to xmpp MUC
app.post('/messages', async (req, res) => {
    console.log('got a message ...');
    const {client, xml} = require("@xmpp/client");
    const xmpp = client({
        service: XMPP_SERVICE_URL,
        domain: XMPP_DOMAIN,
        resource: generate_random_string(),
        preferredSaslMechanism: "ANONYMOUS"
    });

    try {
        await xmpp.start();
    } catch (e) {
        console.error(e);
        res.status(500).send()
    }

    const conference_address = req.body.room_id + "@" + "conference." + XMPP_DOMAIN;
    const user = req.body.user;

    try {

        await xmpp.send(xml("presence", {
            from: conference_address,
            to: conference_address + "/" + user,
        }, xml("x", {xmlns: "http://jabber.org/protocol/muc"})));
        const message = xml("message", {
                type: "groupchat",
                to: conference_address
            },
            xml("body", {}, req.body.message),
        );
        await xmpp.send(message);
        console.log('message being sent');
        await xmpp.stop();
    } catch (e) {
        console.error(e);
        res.status(500).send();
    }
    res.status(201).send();
});

app.listen(PORT, () => {
    console.log(`Server running at: http://0.0.0.0:${PORT}/`);
});