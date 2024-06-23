import { OnGatewayConnection, OnGatewayDisconnect, SubscribeMessage, WebSocketGateway, WebSocketServer } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway()
export class WebsocketGateway implements OnGatewayConnection, OnGatewayDisconnect{
  @WebSocketServer() server:Server;
  private connectedClients: WebSocket[] = [];

  handleConnection(client: WebSocket, ...args: any[]) {
    console.log(`Client connected: ${client}`);
    this.connectedClients.push(client);
  }

  handleDisconnect(client: WebSocket) {
    console.log(`Client disconnected: ${client}`);
    this.connectedClients = this.connectedClients.filter(connectedClient => connectedClient !== client);
  }

  @SubscribeMessage('events')
  handleEvent(client: Socket, payload: string): string {
    console.log(payload);
    // const event = 'events';
    // this.server.emit(event, payload);
    return payload;
  }
}
