// Strategy Pattern - Concrete
const BillingStrategy = require('./billingStrategy.js')
class BillByNewReadingStrategy extends BillingStrategy {
  calculate(usage, price, existingBill) {
    // returns running bill plus new bill
    return existingBill + (usage * price);
  }
}
module.exports = BillByNewReadingStrategy;