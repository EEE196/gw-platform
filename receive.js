//--------------------------wEBSOCKET----------------
import { WebSocketServer } from 'ws';
const socket = new WebSocketServer({ port: 8080 });

socket.onopen = function() {
  console.log('WebSocket connection established.');
  
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed with code:', event.code);
};

//--------------------------------lora/udp code
import dgram from 'node:dgram';
import lora_packet from 'lora-packet'

const NwkSKey = Buffer.from("00000000000000000000000000000000", "hex");
const AppSKey = Buffer.from("00000000000000000000000000000000", "hex");

// --------------------creating a udp server --------------------

// creating a udp server
var server = dgram.createSocket('udp4');

// emits when any error occurs
server.on('error',function(error){
  console.log('Error: ' + error);
  server.close();
});
clent.send("packet");
// emits on new datagram msg
server.on('message',function(msg,info){
  try {
	msg = msg.subarray(12).toString('utf8');
	msg = JSON.parse(msg);
	msg = msg['rxpk'][0]['data']
	const packet = lora.fromWire(msg);

	console.log("packet.toString()=\n" + packet);

	// e.g. retrieve payload elements
	console.log("packet MIC=" + packet.MIC.toString("hex"));
	console.log("FRMPayload=" + packet.FRMPayload.toString("hex"));

	// check MIC
	console.log("MIC check=" + (lora_packet.verifyMIC(packet, NwkSKey) ? "OK" : "fail"));

	// calculate MIC based on contents
	console.log("calculated MIC=" + lora_packet.calculateMIC(packet, NwkSKey).toString("hex"));

	// decrypt payload
	console.log("Decrypted (ASCII)='" + lora_packet.decrypt(packet, AppSKey, NwkSKey).toString() + "'");
	console.log("Decrypted (hex)='0x" + lora_packet.decrypt(packet, AppSKey, NwkSKey).toString("hex") + "'");
	if (lora_packt.verifyMIC(packet, NwkSKey) ? true : false) {
		socket.send(lora_packet.decrypt(packet, AppSKey, NwkSKey))
		wss.clients.forEach(function each(client) {
		      if (client !== ws && client.readyState === WebSocket.OPEN) {
			client.send(packet, {compress: false});
		      }
		    });
	}
	  } catch {};
});

//emits when socket is ready and listening for datagram msgs
server.on('listening',function(){
  var address = server.address();
  var port = address.port;
  var family = address.family;
  var ipaddr = address.address;
  console.log('Server is listening at port' + port);
  console.log('Server ip :' + ipaddr);
  console.log('Server is IP4/IP6 : ' + family);
});


server.bind(2000);
