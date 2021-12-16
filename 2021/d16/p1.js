// https://adventofcode.com/2021/day/16

const _ = require('underscore');
const fs = require('fs');

FILE = '2021/d16/input'

TYPES = {
  SUM: 0,
  PRODUCT: 1,
  MINIMUM: 2,
  MAXIMUM: 3,
  LITERAL: 4,
  GREATER: 5,
  LESS: 6,
  EQUAL: 7,
}

const h2b = (h) => _.map(h, i => parseInt(i, 16).toString(2).padStart(4, '0')).join('');
const ss = (s, i) => [s.substring(0, i), s.substring(i)]

const parseLiteral = (stream) => {
  let version = -1, type = -1, payload = 0;
  [version, stream] = ss(stream, 3);
  [type, stream] = ss(stream, 3);
  for ([chunk, stream] = ss(stream, 5); chunk[0] == '1'; [chunk, stream] = ss(stream, 5))
    payload = 16 * payload + parseInt(chunk.substring(1), 2);
  payload = 16 * payload + parseInt(chunk.substring(1), 2);
  return [
    {
      type: parseInt(type, 2),
      version: parseInt(version, 2),
      payload: payload
    },
    stream];
}

const parseOperator = (stream) => {
  let version = -1, type = -1, payload = null;
  [version, stream] = ss(stream, 3);
  [type, stream] = ss(stream, 3);
  if (stream[0] == '0') { // We know the length of the subsequent packets
    length = parseInt(stream.substring(1, 16), 2);
    stream = stream.substring(16);
    [packets, stream] = ss(stream, length);
    [payload, ignored] = decodePackets(packets, Number.MAX_SAFE_INTEGER);
  } else { // We know the number of the subsequent packets
    packetCount = parseInt(stream.substring(1, 12), 2);
    stream = stream.substring(12);
    [payload, stream] = decodePackets(stream, packetCount);
  }
  return [
    {
      type: parseInt(type, 2),
      version: parseInt(version, 2),
      payload: payload
    },
    stream];
}

const decodePackets = (stream, packetCount = 1) => {
  let packets = []
  while (stream.length > 10 && packetCount-- > 0) { // No packet length can be less than 11
    type = parseInt(stream.substring(3, 6), 2);
    [packet, stream] = type == TYPES.LITERAL ? parseLiteral(stream) : parseOperator(stream);
    packets.push(packet);
  }
  return [packets, stream];
}

const sumVersion = (packet) => {
  return packet.type == TYPES.LITERAL ?
    packet.version :
    packet.version + _.map(packet.payload, p => sumVersion(p)).reduce((a, b) => a + b, 0);
}

const calculateValue = (packet) => {
  switch (packet.type) {
    case TYPES.LITERAL:
      return packet.payload;
    case TYPES.SUM:
      return packet.payload.map(p => calculateValue(p)).reduce((a, b) => a + b, 0);
    case TYPES.PRODUCT:
      return packet.payload.map(p => calculateValue(p)).reduce((a, b) => a * b, 1);
    case TYPES.MINIMUM:
      return packet.payload.map(p => calculateValue(p)).reduce((a, b) => a < b ? a : b, Number.MAX_SAFE_INTEGER);
    case TYPES.MAXIMUM:
      return packet.payload.map(p => calculateValue(p)).reduce((a, b) => a > b ? a : b, 0);
    case TYPES.LESS:
      return calculateValue(packet.payload[0]) < calculateValue(packet.payload[1]) ? 1 : 0;
    case TYPES.GREATER:
      return calculateValue(packet.payload[0]) > calculateValue(packet.payload[1]) ? 1 : 0;
    case TYPES.EQUAL:
      return calculateValue(packet.payload[0]) == calculateValue(packet.payload[1]) ? 1 : 0;
  }
}

const raw_data = fs.readFileSync(FILE, 'utf8');
packet = decodePackets(h2b(raw_data))[0][0];

// Part 1
console.log(sumVersion(packet));

// Part 2
console.log(calculateValue(packet));

