// Jest 30.5 example: stubbing a repository
const userRepo = {
  findById: jest.fn().mockReturnValue({ id: 1, name: 'Alice' })
};

const service = new UserService(userRepo);
const user = service.getUserById(1);

expect(user.name).toBe('Alice');
expect(userRepo.findById).toHaveBeenCalledWith(1);
