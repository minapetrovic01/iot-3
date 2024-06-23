// mqtt_subscriber.js

const mqtt = require('mqtt');
const WebSocket = require('ws');

// MQTT connection
const mqttClient = mqtt.connect('mqtt://mosquitto:1883'); // Replace with your MQTT broker URL
// const mqttClient = mqtt.connect('mqtt://localhost:1883');
// WebSocket server
const wss = new WebSocket.Server({ port: 8080 }); // WebSocket server port

mqttClient.on('connect', () => {
    console.log('Connected to MQTT broker');
    mqttClient.subscribe('filtered'); // Replace with your MQTT topic
});

mqttClient.on('message', (topic, message) => {
    console.log('Received message:', message.toString());
    sendToClients(message.toString());
});

wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

function sendToClients(message) {
    console.log('Sending message to all clients:', message);
    wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(message);
        }
    });
}
