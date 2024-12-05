// Needed to host connections with clients
const { Server } = require("socket.io");
const server = new Server({ /* options */ });
// Needed to connect with grid for price updates and warnings of issues
const io = require('socket.io-client')
const BillCalculator = require('./BillCalculationStrategy/billCalculator.js');
const BillByHistoricStrategy = require('./BillCalculationStrategy/billCalculateByHistoric.js');
const BillByNewReadingStrategy = require('./BillCalculationStrategy/billCalculateByNewReading.js');
const gridURL = "http://localhost:3001";
let gridSocket = io.connect(gridURL)
// Needed for requests to database manager
const http = require(`http`)
// Define port to listen on for client connections
const port = 3000
// Define timer function for later use
const timer = ms => new Promise(res => setTimeout(res, ms))

// Keep a dictionary of all active clients
const connections = {}

// Store locally the current energy price per kWh with initial value in line with uk average
var energyCost = 0.24
const billByHistoricStrategy = new BillByHistoricStrategy()
const billByNewReadingStrategy = new BillByNewReadingStrategy()
const billCalculator = new BillCalculator(billByHistoricStrategy);

// Given a client ID, check they have authenticated. Used to block unauthorised use of the application
function checkAuth(id) {
    found = false
    for (conn in connections) {
        if (conn == id) {
            found = true
        }
    }
    return found
}

// Set up socket with Clients
server.on("connection", (socket) => {
    console.log(`Connection established (ID: ${socket.id})`)

    // Handle authentication with the client
    socket.on("authenticate", async (data, callback) => {
        try {
            // AUTHENTICATE ID AND TOKEN WITH DATABASE
            authenticated = await getAuth(data.id, data.token)

            // Contact database, fetch existing readings and calculate total bill and total usage
            console.log(`Fetching readings for user ${data.id}`);
            results = await getReadingValues(data.id)
            if (authenticated) {
                connections[data.id] = {
                    "bill": results.billTotal,
                    "socket": socket.id
                }
                // Feed values to client
                console.log(`Socket ${socket.id} authenticated with ID ${data.id}. Existing bill of £${formatPrice(results.billTotal)} (${results.usageTotal}kWh)`)
                socket.emit("updateBill", results.billTotal)
                socket.emit("updateUsage", results.usageTotal)
            } else {
                // Remove connection on authentication failure
                socket.disconnect()
            }
            callback(authenticated)
        } catch (error) {
            console.error(`Authentication error: ${error}`)
        }
    })

    // Receive a reading from a client and log it to database
    socket.on("reading", (data) => {
        // Check for invalid readings
        if (data.usage < 0) {
            console.log(`CLIENT ${data.id} INVALID READING ${data.usage}kWh. CLOSING CONNECTION`)
            socket.emit("warning", "Invalid reading provided. Closing connection.")
            socket.disconnect()
            return
        }
        // Check for readings from unauthenticated connections
        if (!checkAuth(data.id)) {
            socket.emit("warning", "Authentication failed")
            return 
        }

        // Calculate cost from reading usage
        try {
            // Calculate updated bill
            billCalculator.setStrategy(billByNewReadingStrategy)
            connections[data.id].bill = billCalculator.calculateBill(data.usage, energyCost, connections[data.id].bill)
            // Log reading to the database
            DBLogReading(data.id, data.time, data.usage * energyCost)
            console.log(`Reading from ${data.id}: ${data.usage}kWh (Reading cost £${formatPrice(data.usage * energyCost)}, Bill total £${formatPrice(connections[data.id].bill)})`)
            socket.emit("updateBill", connections[data.id].bill)
        } catch (error) {
            console.error(error.message)
        }
    })
    
    // On client disconnect, remove connection from authenticated clients list
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

    socket.on("check_grid_status", (callback) => {
        socket.emit("grid_status", (response) => {
            callback(response)
        })
    })
});

// Helper function for getting historic readings
async function getReadingValues(id) {
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
                // Process response
                var body = Buffer.concat(bodyChunks);
                billTotal = 0
                usageTotal = 0
                // JSON to array filtered by costs
                const costs = JSON.parse(body).map(reading => reading.cost);
                const usages = JSON.parse(body).map(reading => reading.usage);
                try {
                    billCalculator.setStrategy(billByHistoricStrategy)
                    billTotal = billCalculator.calculateBill(costs)
                    usageTotal = billCalculator.calculateBill(usages) // same functionality, just adds a series of numbers
                } catch (error) {
                    console.log(error.message)
                } // don't amend bill if error
                resolve({billTotal, usageTotal})
            })
        });
        // Error handling on failed request and retry after 30s
        getReadings.on('error', (err) => {
            console.log(`Unable to complete request to /readings. Retrying in 30s`);
            setTimeout(() => {
                getReadingValues(id)
            }, 30000)
            resolve(-1)
        });
    })
}

// Helper function with authenticating clients
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
                resolve(JSON.parse(body))
            })
        });
        
        // Error handling on failed request and retry in 30s
        getAuthReq.on('error', (err) => {
            console.log(`Unable to complete request to /authenticate. Retrying in 30s`);
            setTimeout(() => {
                getAuth(id, token)
            }, 30000)
            resolve(-1)
        });

        // Set request body
        getAuthReq.write(JSON.stringify({
            "id": id,
            "token": token
        }))

        // Send request
        getAuthReq.end()
    })
}

// Helper function with logging a database reading
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
                resolve(body)
            })
        });
        
        // Error handling on request failure and retry in 30s
        logRead.on('error', (err) => {
            console.log(`Unable to complete request to /logRead. Retrying in 30s`);
            setTimeout(() => {
                DBLogReading(id, time, cost)
            }, 30000)
            resolve(-1)
        });

        // Set request body
        logRead.write(JSON.stringify({
            "id": id,
            "time": time,
            "cost": cost
        }))

        // Send request
        logRead.end()
    })
}

// Handle connection with the power grid
gridSocket.on("connect", (socket) => {
    console.log("Connection established with power grid")
})

// Update locally stored energy price in accordance with power grid
gridSocket.on("price", (data) => {
    console.log(`Energy price updated. £${energyCost} -> £${data}`)
    energyCost = data
})

// Alert clients to disconnection from power grid
gridSocket.on("disconnect", (reason) => {
    console.log("Connection to power grid lost")
    server.emit("warning", "Connection to power grid lost")
})

// Alert clients when there are issues broadcast by the power grid
gridSocket.on("issue", (message) => {
    console.log(`Warning issued by grid: ${message}`)
    server.emit("warning", message)
})

// Inform clients that grid issue is resolved
gridSocket.on("issue_resolved", () => {
    console.log("Grid issue resolved")
    server.emit("resolved")
})

// Check database is online before accepting client connections
async function startProgram() {
    foundDB = false
    while (!foundDB) {
        if (await getAuth(1,1) > 0) {
            console.log(`Database online, starting server`)
            foundDB = true
            // Accept client connections
            server.listen(port)
            console.log(`Listening for connections on port ${port}`)
        } else {
            console.log(`Database not online, retrying in 1s`)
            await timer(1000)
        }
    }
}

// Helper function to limit length of numbers
function formatPrice(price) {
    return Math.round(price * 100)/100
}

startProgram()

function closeGridSocket() {
    if (gridSocket) {
        gridSocket.disconnect();
    }
}

module.exports = { checkAuth, connections, server, closeGridSocket}