local log = module._log;
--local authenticated_rooms = {};
--if authenticated_rooms[room_id] ~= nil then do something end

function getAllData(t, prevData)
    -- if prevData == nil, start empty, otherwise start with prevData
    local data = prevData or {}

    -- copy all the attributes from t
    for k, v in pairs(t) do
        log("info", tostring(k) .. " ---- " .. tostring(v));
        data[k] = data[k] or v
    end

    -- get t's metatable, or exit if not existing
    local mt = getmetatable(t)
    if type(mt) ~= 'table' then return data end

    -- get the __index from mt, or exit if not table
    local index = mt.__index
    if type(index) ~= 'table' then return data end

    -- include the data from index into data, recursively, and return
    return getAllData(index, data)
end

module:hook("muc-occupant-groupchat", function(event)
    local room_id = tostring(event.origin.jitsi_web_query_room);
    local message = tostring(event.stanza:get_child_text("body"));

    if string.sub(message, 1, 1) == '/' then
        local f = assert(io.popen("python3 /prosody-plugins/send_message.py" .. " " .. room_id .. " '" .. message .. "'", 'r'));
        local output = f:read('*all');
        log("info", output);
    end
end);
