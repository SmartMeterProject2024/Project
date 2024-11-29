const BillingStrategy = require('./billingStrategy.js')
class BillByNewReadingStrategy extends BillingStrategy {
  calculate(usage, price, existingBill) {
    // returns updated bill
    return existingBill + (usage * price);
  }
}
module.exports = BillByNewReadingStrategy;