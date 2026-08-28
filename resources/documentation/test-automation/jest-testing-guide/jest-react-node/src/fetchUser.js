async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error('User not found');
  return res.json();
}

module.exports = { fetchUser };
