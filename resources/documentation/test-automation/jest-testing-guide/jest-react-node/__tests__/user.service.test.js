jest.mock('../src/api');

const { getUser } = require('../src/api');
const { loadDashboard } = require('../src/user.service');

describe('user.service', () => {
  it('returns the user from the API', async () => {
    getUser.mockResolvedValueOnce({ id: 1, name: 'Jane' });

    const result = await loadDashboard(1);
    expect(result).toEqual({ user: { id: 1, name: 'Jane' } });
    expect(getUser).toHaveBeenCalledWith(1);
  });

  it('propagates API errors', async () => {
    getUser.mockRejectedValueOnce(new Error('Network error'));

    await expect(loadDashboard(1)).rejects.toThrow('Network error');
  });
});
