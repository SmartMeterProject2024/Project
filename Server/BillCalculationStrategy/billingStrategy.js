// Strategy interface
class BillingStrategy {
  execute(...args) {
    throw new Error("This method should be overridden!");
  }
}
module.exports = BillingStrategy;