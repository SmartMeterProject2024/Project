const express = require(`express`)
const app = express()
const port = 3002

app.use(express.json())

app.listen(port, () => {
    console.log(`Listening on port ${port}`)
})

app.post(`/logRead`, (req, res) => {
    console.log(`Request received on /logRead`)
})

app.post(`/authenticate/`, (req, res) => {
    // Mocks authentication using a secret
    console.log(`Requesr received on /authenticate`)
    res.json(true)
})

app.get(`/readings/:id`, (req, res) => {
    // Mocks a database fetching existing readings for a given user
    console.log(`request received on /readings for id ${req.params.id}`)
    readings = []
    for (x = 1; x <Math.floor(Math.random() * 10) + 1; x++) {
        reading = {
            "id": req.params.id,
            "time": "randomTime",
            "cost": (Math.floor(Math.random() * 150) / 100)
        }
        readings.push(reading)
    }

    console.log(readings)
    res.json(readings)
})