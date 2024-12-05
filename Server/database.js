// Express used to host simple http server for database manager
// In this instance, we are mocking the database, randomly generating values "pulled" from db
const express = require(`express`)

// Start setting up express server
const app = express()
const port = 3002
app.use(express.json())

// Listen on given port for connections
app.listen(port, () => {
    console.log(`Listening on port ${port}`)
})

// Mock receiving, processing, and saving readings to database
app.post(`/logRead`, (req, res) => {
    console.log(`Request received on /logRead`)
})

// Mock receiving, and processing client auth details
app.post(`/authenticate/`, (req, res) => {
    // Mocks authentication using a secret
    console.log(`Request received on /authenticate`)
    res.json(true)
})

// Mock fetching stored readings associated with a user
app.get(`/readings/:id`, (req, res) => {
    console.log(`request received on /readings for id ${req.params.id}`)
    readings = []
    // Randomly generate readings
    for (x = 1; x < Math.floor(Math.random() * 30) + 1; x++) {
        cost = Math.floor(Math.random() * 80) / 100
        reading = {
            "id": req.params.id,
            "time": "r/a/n do:mT:im.e",
            "cost": cost,
            "usage": cost / 0.24
        }
        readings.push(reading)
    }

    // Return set of readings to the client
    console.log(readings)
    res.json(readings)
})