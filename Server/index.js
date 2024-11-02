const { Server } = require("socket.io");

const io = new Server({ /* options */ });

io.on("connection", (socket) => {
    console.log(`Connection established (ID: ${socket.id})`)
    socket.emit("Hello", "Hi :)")
    
    socket.on("Hello World!", (data) => {
        console.log(`Socket ${socket.id} sent a reading!`)
        // Example usage
        const { id, time, usage } = JsonToVariables(data);
        console.log(`ID: ${id}`);
        console.log(`Time: ${time}`);
        console.log(`Usage: ${usage}`);
    })

    socket.on("Send_Reading", (data) => {
        console.log(`Socket ${socket.id} sent a reading!`)
        const { id, time, usage } = JsonToVariables(data);
        console.log(`ID: ${id}`);
        console.log(`Time: ${time}`);
        console.log(`Usage: ${usage}`);
    })
});

io.listen(3000);

// Function to convert JSON object into variables
function JsonToVariables(jsonObject) {
    const { id, time, usage } = jsonObject;
    return { id, time, usage };
}