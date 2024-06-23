import { Injectable, Logger } from '@nestjs/common';
import e from 'express';
import * as mqtt from 'mqtt';
import { WebsocketGateway } from 'src/websocket/websocket.gateway';
import { Server, WebSocket } from 'ws';    

@Injectable()
export class MqttService {
    private client: mqtt.MqttClient;
    private readonly logger = new Logger(MqttService.name);

    constructor(private readonly webSocketgateway: WebsocketGateway) {
        this.client = mqtt.connect('mqtt://localhost:1883');
        this.client.on('connect', () => {
            console.log('Connected to MQTT broker');
            this.client.subscribe('filtered');
        });
        this.client.on('error', (error) => {
            this.logger.error(`MQTT connection error: ${error.message}`, error.stack);
        });

        this.client.on('message', (topic, message) => {
            this.logger.log(`Received message from topic ${topic}`);
            const event = JSON.parse(message.toString());
            if(event && typeof event === 'object' && 'stresState' in event && event.stresState > 1){
                console.log('Stress state is above 1');
                this.webSocketgateway.server.emit('StressHigh', event);
            }
            else{
                console.log('Stress state is below 1');
                this.webSocketgateway.server.emit('StressLow', event);
            }
          });
    }

    
}
