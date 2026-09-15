// Jest 30.5 example: mocking a logger
const logger = { error: jest.fn() };
const service = new PaymentService(logger);

service.processPayment(null);

expect(logger.error).toHaveBeenCalledWith(
  expect.stringContaining('Invalid payment')
);
