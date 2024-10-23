const { Server } = require("socket.io");

const io = new Server({ /* options */ });

io.on("connection", (socket) => {
    console.log(`Connection established (ID: ${socket.id})`)
    socket.emit("Hello", "Hi :)")
});

io.on("Hello World!", (socket) => {
    console.log(`Socket ${socket.id} says hello!`)
})

io.listen(3000);