const { Server } = require("socket.io");
const server = new Server({ /* options */ });
const io = require('socket.io-client')
const gridURL = "http://localhost:3001";
let gridSocket = io.connect(gridURL)
const http = require(`http`)
const port = 3000
const connections = {}

var energyCost

function checkAuth(id) {
    for (conn in connections) {
        if (conn == id) {
            return true
        } else {
            return false
        }
    }
}

server.on("connection", (socket) => {
    console.log(`Connection established (ID: ${socket.id})`)

    socket.on("authenticate", async (data, callback) => {
        // AUTHENTICATE ID AND TOKEN WITH DATABASE
        authenticated = await getAuth(data.id, data.token)
        //console.log(`authentication result ${authenticated}`)
        billTotal = 0
        console.log(`Fetching readings for user ${data.id}`)
        billTotal = await getBillTotal(data.id)
        //console.log(`BILLTOTAL----------${billTotal}`)
        if (authenticated) {
            connections[data.id] = {
                "bill": billTotal,
                "socket": socket.id
            }
            console.log(`Socket ${socket.id} authenticated with ID ${data.id}. Existing bill of ${billTotal}`)
        } else {
            socket.disconnect()
        }
        callback(authenticated, billTotal)
    })

    socket.on("reading", (data) => {
        if (data.usage < 0) {
            console.log(`CLIENT ${data.id} INVALID READING ${data.usage}kWh. CLOSING CONNECTION`)
            socket.emit("warning", "Invalid reading provided. Closing connection.")
            socket.disconnect()
            return
        }
        if (!checkAuth(data.id)) {
            socket.emit("warning", "Authentication failed")
            return 
        }
        readingCost = data.usage * energyCost
        connections[data.id].bill += readingCost
        // LOG READING TO DATABASE
        DBLogReading(data.id, data.time, readingCost)
        console.log(`Reading from ${data.id}: ${data.usage} (£${readingCost}, £${connections[data.id].bill})`)
        socket.emit("updateBill", connections[data.id].bill)
    })
    
    socket.on("disconnect", (reason) => {
        console.log(`Connection ended, forgetting client. (Disconnect reason: ${reason})`)
        foundID = ""
        for (conn in connections) {
            if (connections[conn].socket == socket.id) {
                foundID = conn
            }
        }
        if (foundID) {
            console.log(`Forgetting client ${foundID} on socket ${socket.id}`)
            delete connections[foundID]
        } else {
            console.log(`Could not find client associated with socket ${socket.id}`)
        }
    })
});

async function getBillTotal(id) {
    return new Promise((resolve) => {
        var getReadings = http.get({
            hostname: 'localhost',
            port: 3002,
            path: `/readings/${id}`,
            json: true
        }, function(res) {        
            var bodyChunks = [];
            res.on('data', function(chunk) {
                bodyChunks.push(chunk);
            }).on('end', function() {
                var body = Buffer.concat(bodyChunks);
                for (r in JSON.parse(body)) {
                    //console.log(JSON.parse(body)[r])
                    //console.log(`Cost: ${JSON.parse(body)[r].cost}`)
                    billTotal += JSON.parse(body)[r].cost
                }
                resolve(billTotal)
            })
        });
        
        getReadings.on('error', (err) => {
            console.log('ERROR: ' + err.message);
            resolve(-1)
        });
    })
}

async function getAuth(id, token) {
    return new Promise((resolve) => {
        var getAuthReq = http.request({
            hostname: 'localhost',
            port: 3002,
            method: "POST",
            path: `/authenticate`
        }, function(res) {        
            var bodyChunks = [];
            res.on('data', function(chunk) {
                bodyChunks.push(chunk);
            }).on('end', function() {
                var body = Buffer.concat(bodyChunks);
                //console.log(JSON.parse(body))
                resolve(JSON.parse(body))
            })
        });
        
        getAuthReq.on('error', (err) => {
            console.log('ERROR: ' + err.message);
            resolve(-1)
        });

        getAuthReq.write(JSON.stringify({
            "id": id,
            "token": token
        }))

        getAuthReq.end()
    })
}

async function DBLogReading(id, time, cost) {
    return new Promise((resolve) => {
        var logRead = http.request({
            hostname: 'localhost',
            port: 3002,
            method: "POST",
            path: `/logRead`
        }, function(res) {        
            var bodyChunks = [];
            res.on('data', function(chunk) {
                bodyChunks.push(chunk);
            }).on('end', function() {
                var body = Buffer.concat(bodyChunks);
                console.log(body)
                resolve(body)
            })
        });
        
        logRead.on('error', (err) => {
            console.log('ERROR: ' + err.message);
            resolve(-1)
        });

        logRead.write(JSON.stringify({
            "id": id,
            "time": time,
            "cost": cost
        }))

        logRead.end()
    })
}

gridSocket.on("connect", (socket) => {
    console.log("Connection established with power grid")

    server.listen(port)
    console.log(`Listening for connections on port ${port}`)
})

gridSocket.on("price", (data) => {
    console.log(`Energy price updated. ${energyCost} -> ${data}`)
    energyCost = data
})

gridSocket.on("disconnect", (reason) => {
    console.log("Connection to power grid lost")
    server.emit("warning", "Connection to power grid lost")
})

gridSocket.on("issue", (message) => {
    console.log(`Warning issued by grid: ${message}`)
    server.emit("warning", message)
})

gridSocket.on("issue_resolved", () => {
    console.log("Grid issue resolved")
    server.emit("resolved")
})
