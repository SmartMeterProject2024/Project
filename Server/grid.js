// Mock a third party electricity grid program, giving price updates and warnings about the network
const { Server } = require("socket.io");
const io = new Server({ /* options */ });
const port = 3001

// Initial energy cost per kWh
var energyCost = 0.24
var grid_errored = false
// Handle connections
io.on("connection", (socket) => {
    console.log(`Connection established (ID: ${socket.id})`)
    // Push energy price to new connections
    socket.emit("price", energyCost)
    
    // Log disconnects
    socket.on("disconnect", (reason) => {
        console.log(`Socket ${socket.id} disconnected`)
    })

    socket.on('check_status', (callback) => {
      callback(grid_errored);
  });
});


// Define loop for adjusting energy prices
const timer = ms => new Promise(res => setTimeout(res, ms))

// For the duration of the program, have energy price fluctuate at random times within given intervals
async function priceLoop () {
  while (true) {
    // Randomly generate either 0.01 or -0.01
    try {
      newPrice = energyCost + ((Math.floor(Math.random() * 2) * 2) - 1)/100
      newPrice = Math.round(newPrice * 100) / 100 // Round to 2 decimal places, stops x.xx999999999
      if (newPrice > 0.27) { // set upper price limit to 0.27
          console.log("Fluctiated too high, price correction")
          newPrice = 0.26
      }
      if (newPrice < 0.21) { // set lower price limit to 0.21
          console.log("Fluctuated too low, price correction")
          newPrice = 0.22
      }

    // Log price changed to console
      console.log(`Price updated from ${energyCost} to ${newPrice}`)

    // Push new energy price to clients
      energyCost = newPrice
      io.emit("price", energyCost)

    // wait 1-3 minutes between price changes
    } catch (error) {
      console.error(`Failed to update new energy price: ${error}`);
    }
    await timer((Math.floor(Math.random() * 120) +60) * 1000)
  }
}

// Define a list of possible issues to occur in the energy grid
issueList = ["Substation shut down", "Heavy load on power grid", "Powerline maintenance"]

// Loop randomly selecting an issue to occur
async function issueLoop () {
    while (true) {
        await timer((Math.floor(Math.random() * 180) + 60) * 1000) // wait 1-4 minutes between issues
        try {
          chosenIssue = issueList[Math.floor(Math.random() * issueList.length)] // randomly choose an issue
        // Log issue selected and push to connections
          console.log(`Issue detected: ${chosenIssue}`)
          console.log(`Broadcasting issue`)
          grid_errored = true
          io.emit(`issue`, chosenIssue)
          await timer(Math.floor(Math.random() * 15000) + 15000) // error for 15-30 seconds
          grid_errored = false
          io.emit(`issue_resolved`)
          console.log(`Issue resolved`)
        } catch (error) {
          console.error(`A problem occured when generating a Grid error: ${error}`)
        }       
    }
}

// Start both loops
issueLoop()
priceLoop()


// Open port, listen for connections
io.listen(port)
console.log(`Listening for connections on port ${port}`)