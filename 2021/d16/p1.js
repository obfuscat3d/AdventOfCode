// https://adventofcode.com/2021/day/15

const _ = require('underscore');
const fs = require('fs');
const util = require('util');

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

HEX_BIN_MAP = _.range(16).reduce((a, b) => { return { [b.toString(16)]: b.toString(2).padStart(4, '0'), ...a }; }, {})
const h2b = (h) => _.map(h.toLowerCase(), i => HEX_BIN_MAP[i]).join('');
const ss = (s, ...i) => [s.substring(0, i), s.substring(i)]

const parseLiteral = (stream) => {
  let version = -1, type = -1, payload = 0;
  [version, stream] = ss(stream, 3);
  [type, stream] = ss(stream, 3);
  [chunk, stream] = ss(stream, 5);
  while (chunk[0] == '1') {
    payload = 16 * payload + parseInt(chunk.substring(1), 2);
    [chunk, stream] = ss(stream, 5);
  }
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
    if (type == TYPES.LITERAL) {
      [packet, stream] = parseLiteral(stream);
      packets.push(packet);
    } else {
      [packet, stream] = parseOperator(stream);
      packets.push(packet);
    }
  }
  return [packets, stream];
}

const sumVersions = (packets) => {
  return _.map(packets, p => sumVersion(p)).reduce((a, b) => a + b, 0);
}

const sumVersion = (packet) => {
  if (packet.type == TYPES.LITERAL) {
    return packet.version;
  } else {
    return packet.version + sumVersions(packet.payload);
  }
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
packet = decodePackets(h2b(raw_data))[0];

// Part 1
console.log(
  sumVersions(packet)
);

// Part 2
console.log(
  calculateValue(packet[0])
);

