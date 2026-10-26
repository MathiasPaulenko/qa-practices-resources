// Jest 29 suite — run `npm start` in another terminal first.
const WebSocket = require('ws');
const { spawn } = require('child_process');

const URL = 'ws://localhost:8080/ws';
let server;

beforeAll((done) => {
  server = spawn('node', ['server.js'], { stdio: 'ignore' });
  setTimeout(done, 800);
});

afterAll(() => server.kill());

const connect = () => new WebSocket(URL);

test('connects and receives subscribe ack', (done) => {
  const ws = connect();
  ws.on('open', () => ws.send(JSON.stringify({ type: 'subscribe', channel: 'updates' })));
  ws.on('message', (data) => {
    const m = JSON.parse(data);
    expect(m.type).toBe('subscribed');
    expect(m.channel).toBe('updates');
    ws.close();
    done();
  });
  ws.on('error', done);
});

test('echo returns the same text', (done) => {
  const ws = connect();
  ws.on('open', () => ws.send(JSON.stringify({ type: 'echo', text: 'Hello, World!' })));
  ws.on('message', (data) => {
    expect(JSON.parse(data).text).toBe('Hello, World!');
    ws.close();
    done();
  });
});

test('broadcast reaches a second client', (done) => {
  const ws1 = connect();
  const ws2 = connect();
  ws2.on('message', (data) => {
    const m = JSON.parse(data);
    if (m.type === 'broadcast') {
      expect(m.text).toBe('Hello everyone!');
      ws1.close(); ws2.close(); done();
    }
  });
  ws2.on('open', () => ws1.send(JSON.stringify({ type: 'broadcast', text: 'Hello everyone!' })));
});

test('close reports code 1000 and reason', (done) => {
  const ws = connect();
  ws.on('open', () => ws.close(1000, 'Normal closure'));
  ws.on('close', (code, reason) => {
    expect(code).toBe(1000);
    expect(reason.toString()).toBe('Normal closure');
    done();
  });
});

test('invalid JSON gets a validation error, not a crash', (done) => {
  const ws = connect();
  ws.on('open', () => ws.send('{not json'));
  ws.on('message', (data) => {
    expect(JSON.parse(data).type).toBe('error');
    ws.close();
    done();
  });
});

test('reconnect succeeds after server-side drop', async () => {
  const first = connect();
  await new Promise((r) => first.on('open', r));
  first.close();
  const second = connect();
  await new Promise((r) => second.on('open', r));
  expect(second.readyState).toBe(WebSocket.OPEN);
  second.close();
});
