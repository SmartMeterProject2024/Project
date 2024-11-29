const BillByHistoricStrategy = require("./billCalculateByHistoric");
const BillByNewReadingStrategy = require("./billCalculateByNewReading");

// Context
class BillCalculator {
  constructor(strategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy) {
    this.strategy = strategy;
  }

  calculateBill(...args) {
    if (this.strategy instanceof BillByHistoricStrategy && args.length !== 1) {
      throw new Error("SumTotalStrategy requires exactly 1 argument.");
    }
    if (this.strategy instanceof BillByNewReadingStrategy && args.length !== 3) {
      throw new Error("NewReadingStrategy requires exactly 3 arguments.");
    }
    return this.strategy.calculate(...args);
  }
}
module.exports = BillCalculator;