const request = require('supertest');
const { app, server } = require('../database');

describe('GET readings', () => {
    let consoleLogSpy;
    let consoleErrorSpy;

    beforeEach(() => {
        // Mock console.log and console.error
        consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
        consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
        // Restore the original implementations
        consoleLogSpy.mockRestore();
        consoleErrorSpy.mockRestore();
    });

    afterAll((done) => {
      server.close(done);
  });

    it('should return a list of readings for the given id', async () => {
        const response = await request(app).get('/readings/123');

        expect(response.status).toBe(200);
        expect(response.body).toBeInstanceOf(Array);
        response.body.forEach(reading => {
            expect(reading).toHaveProperty('id', '123');
            expect(reading).toHaveProperty('time', 'randomTime');
            expect(reading).toHaveProperty('cost');
            expect(typeof reading.cost).toBe('number');
        });
    });

    it('should handle errors gracefully', async () => {
        // Mock Math.random to throw an error
        jest.spyOn(Math, 'random').mockImplementation(() => {
            throw new Error('Random error');
        });

        const response = await request(app).get('/readings/123');
        
        expect(response.status).toBe(500);
        expect(response.text).toBe('Internal Server Error');

        // Restore Math.random
        Math.random.mockRestore();
    });
});