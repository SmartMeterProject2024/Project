const BillByHistoricStrategy = require('../BillCalculationStrategy/billCalculateByHistoric');
const BillByNewReadingStrategy = require('../BillCalculationStrategy/billCalculateByNewReading');
const BillCalculator = require('../BillCalculationStrategy/billCalculator');

test('BillByHistoricStrategy calculates the sum of previous readings', () => {
  const strategy = new BillByHistoricStrategy();
  const previousCosts = [100, 200, 300];
  const result = strategy.calculate(previousCosts);
  expect(result).toBe(600);
});

test('BillByHistoricStrategy returns 0 for empty readings', () => {
  const strategy = new BillByHistoricStrategy();
  const previousCosts = [];
  const result = strategy.calculate(previousCosts);
  expect(result).toBe(0);
});

test('BillByNewReadingStrategy calculates the new bill', () => {
  const strategy = new BillByNewReadingStrategy();
  const usage = 50;
  const price = 10;
  const existingBill = 500;
  const newBill = strategy.calculate(usage, price, existingBill);
  expect(newBill).toBe(1000);
});

test('BillCalculator uses BillByHistoricStrategy', () => {
  const historicStrategy = new BillByHistoricStrategy();
  const calculator = new BillCalculator(historicStrategy);
  const previousCosts = [100, 200, 300];
  const result = calculator.calculateBill(previousCosts);
  expect(result).toBe(600);
  expect(calculator.strategy).toBe(historicStrategy);
});

test('BillCalculator uses BillByNewReadingStrategy', () => {
  const newReadingStrategy = new BillByNewReadingStrategy();
  const calculator = new BillCalculator(newReadingStrategy);
  const usage = 20;
  const price = 10;
  const existingBill = 500;
  const newBill = calculator.calculateBill(usage, price, existingBill);
  expect(newBill).toBe(700);
  expect(calculator.strategy).toBe(newReadingStrategy);
});

test('BillCalculator can switch strategies', () => {
  const historicStrategy = new BillByHistoricStrategy();
  const newReadingStrategy = new BillByNewReadingStrategy();
  const calculator = new BillCalculator(historicStrategy);
  
  // Test with historic strategy
  const previousReadings = [100, 200, 300];
  let result = calculator.calculateBill(previousReadings);
  expect(result).toBe(600);
  
  // Switch to new reading strategy
  calculator.setStrategy(newReadingStrategy);
  expect(calculator.strategy).toBe(newReadingStrategy);
  const usage = 50;
  const price = 10;
  const existingBill = 200;
  result = calculator.calculateBill(usage, price, existingBill);
  expect(result).toBe(700);

  // Switch back to historic strategy
  calculator.setStrategy(historicStrategy);
  expect(calculator.strategy).toBe(historicStrategy);
});