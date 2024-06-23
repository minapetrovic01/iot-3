import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as socketio from 'socket.io';
import * as http from 'http';
import { IoAdapter } from '@nestjs/platform-socket.io';


async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors();

  const server = http.createServer(app.getHttpAdapter().getInstance());
  const io = new socketio.Server(server, { 
    cors: {
      origin: '*',
      methods: ['GET', 'POST'],
    },
  });
  app.useWebSocketAdapter(new IoAdapter(io));

  await app.listen(3003);
}
bootstrap();
