import React from 'react';

export default function UserCard({ user }) {
  return (
    <article className="user-card">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </article>
  );
}
