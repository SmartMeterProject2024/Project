const ioClient = require('socket.io-client');
const { server, closeGridSocket } = require('../index');

jest.mock('socket.io-client', () => {
  const mSocket = {
    on: jest.fn(),
    emit: jest.fn(),
    disconnect: jest.fn()
  };
  return {
    connect: jest.fn(() => mSocket)
  };
});

describe('Grid socket events', () => {
  let gridSocket;
  const port = 3000;
  let energyCost = 0;

  beforeAll(() => {
    // Mock the gridSocket connection
    gridSocket = ioClient.connect('http://localhost:3001');
    console.log = jest.fn();
  });

  afterAll(() => {
    closeGridSocket();
  });

  test('should start server listening on port when gridSocket connects', (done) => {
    const listenSpy = jest.spyOn(server, 'listen').mockImplementation((port, callback) => {
      if (callback) callback();
    });

    const connectHandler = gridSocket.on.mock.calls.find(call => call[0] === 'connect')[1];
    connectHandler();

    setTimeout(() => {
      expect(listenSpy).toHaveBeenCalledWith(port);
      listenSpy.mockRestore();
      done();
    }, 100);
  });

  test('should update energy cost on price event', (done) => {
    const newPrice = 100;
    const priceHandler = gridSocket.on.mock.calls.find(call => call[0] === 'price')[1];
    priceHandler(newPrice);

    setTimeout(() => {
      expect(console.log).toHaveBeenCalledWith(`Energy price updated. undefined -> ${newPrice}`);
      energyCost = newPrice;
      done();
    }, 100);
  });

  test('should emit warning on disconnect event', (done) => {
    const emitSpy = jest.spyOn(server, 'emit');
    const disconnectHandler = gridSocket.on.mock.calls.find(call => call[0] === 'disconnect')[1];
    disconnectHandler('some reason');

    setTimeout(() => {
      expect(console.log).toHaveBeenCalledWith('Connection to power grid lost');
      expect(emitSpy).toHaveBeenCalledWith('warning', 'Connection to power grid lost');
      emitSpy.mockRestore();
      done();
    }, 100);
  });

  test('should emit warning on issue event', (done) => {
    const emitSpy = jest.spyOn(server, 'emit');
    const issueMessage = 'Some issue';
    const issueHandler = gridSocket.on.mock.calls.find(call => call[0] === 'issue')[1];
    issueHandler(issueMessage);

    setTimeout(() => {
      expect(console.log).toHaveBeenCalledWith(`Warning issued by grid: ${issueMessage}`);
      expect(emitSpy).toHaveBeenCalledWith('warning', issueMessage);
      emitSpy.mockRestore();
      done();
    }, 100);
  });

  test('should emit resolved on issue_resolved event', (done) => {
    const emitSpy = jest.spyOn(server, 'emit');
    const issueResolvedHandler = gridSocket.on.mock.calls.find(call => call[0] === 'issue_resolved')[1];
    issueResolvedHandler();

    setTimeout(() => {
      expect(console.log).toHaveBeenCalledWith('Grid issue resolved');
      expect(emitSpy).toHaveBeenCalledWith('resolved');
      emitSpy.mockRestore();
      done();
    }, 100);
  });
});