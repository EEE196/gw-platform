//--------------------------wEBSOCKET----------------
import {Buffer} from 'node:buffer';
import WebSocket from 'ws';

const ws = new WebSocket('ws://localhost:8080');

ws.on('error', console.error);

ws.on('open', function open() {
  ws.send(Buffer.from('45', 'hex'));
});
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
// emits on new datagram msg
server.on('message',function(msg,info){
  try {
	msg = msg.subarray(12).toString('utf8');
	msg = JSON.parse(msg);
	if (msg.hasOwnProperty('rxpk') && Array.isArray(msg.rxpk) && msg.rxpk.length === 1) {
		msg = msg['rxpk'][0]['data']
	} else {
		msg = msg['rxpk'][1]['data']
	}
	const packet = lora_packet.fromWire(Buffer.from(msg, 'base64'));

	// check MIC
	console.log("MIC check=" + (lora_packet.verifyMIC(packet, NwkSKey) ? "OK" : "fail"));

	// calculate MIC based on contents
	console.log("calculated MIC=" + lora_packet.calculateMIC(packet, NwkSKey).toString("hex"));

	if (lora_packet.verifyMIC(packet, NwkSKey) ? true : false) {
		ws.send(lora_packet.decrypt(packet, AppSKey, NwkSKey))
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
