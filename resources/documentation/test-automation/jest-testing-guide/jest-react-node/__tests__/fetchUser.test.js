const { fetchUser } = require('../src/fetchUser');

describe('fetchUser', () => {
  it('resolves with user data', async () => {
    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, name: 'Jane' }),
    });

    const user = await fetchUser(1);
    expect(user).toEqual({ id: 1, name: 'Jane' });
    expect(global.fetch).toHaveBeenCalledWith('/api/users/1');
  });

  it('rejects when the API fails', async () => {
    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: false,
    });

    await expect(fetchUser(99)).rejects.toThrow('User not found');
  });
});
