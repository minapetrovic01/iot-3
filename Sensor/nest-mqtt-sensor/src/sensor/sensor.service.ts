import { Injectable, Logger, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Pillow } from './pillow.model';
import * as mqtt from 'mqtt';
import { Cron } from '@nestjs/schedule';


@Injectable()
export class SensorService implements OnModuleInit, OnModuleDestroy {
    private client: mqtt.MqttClient;
    private readonly logger = new Logger(SensorService.name);
    private currentIndex = 0;


    constructor(@InjectModel('Pillow') private readonly pillowModel: Model<Pillow>) { }
    onModuleInit() {
        // this.client = mqtt.connect('mqtt://localhost:1883');
        this.client = mqtt.connect('mqtt://mosquitto:1883');

        this.client.on('connect', () => {
            console.log('Connected to MQTT broker');
        });
        this.client.on('error', (error) => {
            this.logger.error(`MQTT connection error: ${error.message}`, error.stack);
        });
    }

    onModuleDestroy() {
        this.client.end();
    }

    subscribe(topic: string, callback: (message: string) => void) {
        this.client.subscribe(topic);
        this.client.on('message', (topic, message) => {
            callback(message.toString());
        });
    }

    publish(topic: string, message: string) {
        //this.client.publish(topic, message);
        this.client.publish(topic, message, {}, (err) => {
            if (err) {
                console.error('Publish error: ', err);
            } else {
                console.log(`Message "${message}" published to topic "${topic}"`);
            }
        });
    }

    // @Cron('*/10 * * * * *')
    // async handleCron() {
    //     //const data = await this.sensorModel.find().exec();
    //     console.log('Cron job is running...');
    //     this.publish('sensor/test/data', "Helllooo from cron jobbbb!");
    // }
    @Cron('*/10 * * * * *')
    async handleCron() {
        try {
            const count = await this.pillowModel.countDocuments().exec();
            if (count === 0) {
                this.logger.warn('No documents found in the Pillow collection');
                return;
            }

            const data = await this.pillowModel.findOne().skip(this.currentIndex).exec();
            if (data) {
                this.publish('sensor/test/data', JSON.stringify(data));
                // this.publish('sensor', JSON.stringify(data));
                this.logger.log('Cron job is running and data published');
            } else {
                this.logger.warn('No data found at the current index');
            }

            this.currentIndex = (this.currentIndex + 1) % count;
        } catch (error) {
            this.logger.error('Error reading data from MongoDB', error.stack);
        }
    }

}
