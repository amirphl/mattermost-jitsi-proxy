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

const random_string = function () {
    const l = 5 + Math.floor(Math.random() * 5);
    const chars = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM";
    let str = "";
    for (let i = 0; i < l; i++) {
        const n = Math.floor(Math.random() * chars.length);
        str += chars.substr(n, 1);
    }
    return str;
};

app.post('/messages', (req, res) => {
    const {client, xml} = require("@xmpp/client");
    const debug = require("@xmpp/debug");
    const xmpp = client({
        service: XMPP_SERVICE_URL,
        domain: XMPP_DOMAIN,
        resource: random_string(),
        preferredSaslMechanism: "ANONYMOUS"
    });

    xmpp.on("error", (err) => {
    });

    xmpp.on("offline", () => {
    });

    xmpp.on("stanza", async (stanza) => {
        // if (stanza.is('message')) {
        //     if (stanza.getChild('body') && stanza.getChild('body').text()) {
        //         if (stanza.attrs.type === 'groupchat') {
        //             console.log("client ", client_index, " received ", stanza.getChild('body').text());
        //         }
        //     }
        // }
    });

    xmpp.on("online", async (client_jid) => {
        const conference_address = req.body.room_id + "@" + "conference." + XMPP_DOMAIN;
        await xmpp.send(xml("presence", {
            from: client_jid,
            to: conference_address + "/" + req.body.user
        }, xml("x", {xmlns: "http://jabber.org/protocol/muc"})));

        const message = xml("message", {
                type: "groupchat",
                to: conference_address
            },
            xml("body", {}, req.body.message),
        );
        xmpp.send(message);
        xmpp.stop();
    });

    xmpp.start().catch(console.error);
    res.send({message: "ok"});
});

// make the server listen to requests
app.listen(PORT, () => {
    console.log(`Server running at: http://0.0.0.0:${PORT}/`);
});