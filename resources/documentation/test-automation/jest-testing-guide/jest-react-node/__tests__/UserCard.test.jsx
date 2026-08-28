import React from 'react';
import { render, screen } from '@testing-library/react';
import UserCard from '../src/components/UserCard';

const user = {
  name: 'Jane Doe',
  email: 'jane@example.com',
};

describe('UserCard', () => {
  it('renders the user name', () => {
    render(<UserCard user={user} />);
    expect(screen.getByText('Jane Doe')).toBeInTheDocument();
  });

  it('matches the snapshot', () => {
    const { asFragment } = render(<UserCard user={user} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
