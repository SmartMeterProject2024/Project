const { Server } = require("socket.io");
const io = new Server({ /* options */ });
const port = 3001

var energyCost = 0.08
var grid_errored = false

io.on("connection", (socket) => {
    console.log(`Connection established (ID: ${socket.id})`)
    socket.emit("price", energyCost)
    
    socket.on("disconnect", (reason) => {
        console.log(`Socket ${socket.id} disconnected`)
    })

    socket.on('check_status', (callback) => {
      callback(grid_errored);
  });
});

const timer = ms => new Promise(res => setTimeout(res, ms))

async function priceLoop () {
  while (true) {
    newPrice = energyCost + ((Math.floor(Math.random() * 2) * 2) - 1)/100
    newPrice = Math.round(newPrice * 100) / 100 // Round to 2 decimal places, stops x.xx999999999
    if (newPrice > 0.13) { // set upper price limit to 0.13
        console.log("price correction")
        newPrice = 0.12
    }
    if (newPrice < 0.05) { // set lower price limit to 0.05
        console.log("price correction")
        newPrice = 0.06
    }
    console.log(`Price updated from ${energyCost} to ${newPrice}`)
    energyCost = newPrice
    io.emit("price", energyCost)
    await timer((Math.floor(Math.random() * 120) +60) * 1000) // wait 1-3 minutes between price changes
  }
}

issueList = ["issue 1", "issue 2", "issue 3"]
async function issueLoop () {
    while (true) {
        await timer((Math.floor(Math.random() * 180) + 60) * 1000) // wait 1-4 minutes between issues
        chosenIssue = issueList[Math.floor(Math.random() * issueList.length)]
        console.log(`Issue detected: ${chosenIssue}`)
        console.log(`Broadcasting issue`)
        grid_errored = true
        io.emit(`issue`, chosenIssue)
        await timer(Math.floor(Math.random() * 15000) + 15000) // error for 15-30 seconds
        grid_errored = false
        io.emit(`issue_resolved`)
        console.log(`Issue resolved`)
    }
  }

issueLoop()
priceLoop()

io.listen(port)
console.log(`Listening for connections on port ${port}`)