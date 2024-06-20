import { Module } from '@nestjs/common';
import { SensorService } from './sensor.service';
import { MongooseModule } from '@nestjs/mongoose';
import { Pillow, PillowSchema } from './pillow.model';

@Module({
  imports: [MongooseModule.forFeature([{ name: Pillow.name, schema: PillowSchema }])],
  // imports: [MongooseModule.forFeature([{ name: "pillowdb", schema: "pillow" }])],
  providers: [SensorService]
})
export class SensorModule {}
