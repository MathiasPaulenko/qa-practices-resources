// Insomnia 8.3 response test — gRPC InventoryService.GetStock
// Insomnia imports inventory.proto; this test runs on the response.
const json = insomnia.response.json()
insomnia.test('Stock is non-negative', () => {
  insomnia.expect(json.stock).to.be.at.least(0)
})
