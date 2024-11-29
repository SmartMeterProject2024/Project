const BillingStrategy = require('./billingStrategy.js')
class BillByHistoricStrategy extends BillingStrategy {
  calculate(previousReadings) {
    // return sum of costs in array
    return previousReadings.reduce((total, cost) => total + cost, 0.00);
  }
}
module.exports = BillByHistoricStrategy;