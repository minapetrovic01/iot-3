import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MongooseModule } from '@nestjs/mongoose';
import { SensorModule } from './sensor/sensor.module';
import { ScheduleModule } from '@nestjs/schedule';

@Module({
  imports: [
    MongooseModule.forRoot('mongodb://localhost:27017/pillowdb'),
    //MongooseModule.forRoot('mongodb://pillowdb3:27017/pillowdb'),
    ScheduleModule.forRoot(),
    SensorModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
