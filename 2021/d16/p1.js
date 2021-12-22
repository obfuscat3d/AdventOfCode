// https://adventofcode.com/2021/day/16

const _ = require('underscore');
const fs = require('fs');

FILE = '2021/d16/input'

const h2b = (h) => _.map(h, i => parseInt(i, 16).toString(2).padStart(4, '0')).join('');
const ss = (s, ...lengths) => [...lengths.map(i => { t = s.substr(0, i); s = s.substr(i); return t; }), s];

const parseLiteral = (stream) => {
  [version, type, stream] = ss(stream, 3, 3);
  payload = stream.match(/(1\d{4})*0\d{4}/)[0];
  return [{
    type: parseInt(type, 2),
    version: parseInt(version, 2),
    payload: parseInt(_.filter(payload, (a, i) => i % 5).join(''), 2)
  }, stream.substr(payload.length)];
}

const parseOperator = (stream) => {
  let version = -1, type = -1, payload = null;
  [version, type, stream] = ss(stream, 3, 3);
  if (stream[0] == '0') { // We know the length of the subsequent packets
    [, length, stream] = ss(stream, 1, 15);
    [packets, stream] = ss(stream, parseInt(length, 2));
    [payload,] = decodePackets(packets, Number.MAX_SAFE_INTEGER);
  } else { // We know the number of the subsequent packets
    [, packetCount, stream] = ss(stream, 1, 11);
    [payload, stream] = decodePackets(stream, parseInt(packetCount, 2));
  }
  return [{
    type: parseInt(type, 2),
    version: parseInt(version, 2),
    payload: payload
  }, stream];
}

const decodePackets = (stream, packetCount = 1) => {
  let packets = []
  while (stream.length > 10 && packetCount-- > 0) { // Packet length can't be less than 11
    [packet, stream] = stream.substr(3, 3) == '100' ? parseLiteral(stream) : parseOperator(stream);
    packets.push(packet);
  }
  return [packets, stream];
}

const sumVersion = (packet) =>
  packet.version + (packet.type != 4 ? _.map(packet.payload, p => sumVersion(p)).reduce((a, b) => a + b, 0) : 0);

const calc = (packet) => {
  switch (packet.type) {
    case 0: return packet.payload.map(p => calc(p)).reduce((a, b) => a + b, 0);
    case 1: return packet.payload.map(p => calc(p)).reduce((a, b) => a * b, 1);
    case 2: return packet.payload.map(p => calc(p)).reduce((a, b) => a < b ? a : b, Number.MAX_SAFE_INTEGER);
    case 3: return packet.payload.map(p => calc(p)).reduce((a, b) => a > b ? a : b, 0);
    case 4: return packet.payload;
    case 5: return calc(packet.payload[0]) > calc(packet.payload[1]) ? 1 : 0;
    case 6: return calc(packet.payload[0]) < calc(packet.payload[1]) ? 1 : 0;
    case 7: return calc(packet.payload[0]) == calc(packet.payload[1]) ? 1 : 0;
  }
}

const raw_data = fs.readFileSync(FILE, 'utf8');
packet = decodePackets(h2b(raw_data))[0][0];

console.log(sumVersion(packet));
console.log(calc(packet));