// Postman pm.* test script — checkout smoke test (Postman v11)
// Attach to the POST /orders request in the shopnext-checkout collection.
pm.test('Status is 201', () => {
  pm.response.to.have.status(201)
})

pm.test('Order has an id', () => {
  const json = pm.response.json()
  pm.expect(json).to.have.property('orderId')
  pm.collectionVariables.set('orderId', json.orderId)
})

pm.test('Response time is under 400ms', () => {
  pm.expect(pm.response.responseTime).to.be.below(400)
})
