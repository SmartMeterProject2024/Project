const {checkAuth, connections, closeGridSocket} = require('../index');

describe('checkAuth', () => {
    let originalConnections;

    beforeEach(() => {
      // Save the original connections object
      originalConnections = { ...connections };

      // Mock the connections object
      Object.assign(connections, {
          '123': {},
          '456': {},
          '789': {}
      });
  });

    afterEach(() => {
      // Restore the original connections object
      Object.keys(connections).forEach(key => delete connections[key]);
      Object.assign(connections, originalConnections);
  });

    test('should return true if id is in connections', () => {
        expect(checkAuth('123')).toBe(true);
        expect(checkAuth('456')).toBe(true);
        expect(checkAuth('789')).toBe(true);
    });

    test('should return false if id is not in connections', () => {
        expect(checkAuth('000')).toBe(false);
        expect(checkAuth('999')).toBe(false);
    });

    afterAll(() => {
        closeGridSocket();
    });
});