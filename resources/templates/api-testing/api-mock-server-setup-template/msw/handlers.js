import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params;
    if (id === '99999') {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    }
    return HttpResponse.json({
      id: Number(id),
      name: 'John Doe',
      email: 'john@example.com',
      role: 'user',
      createdAt: '2026-01-15T10:00:00Z',
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    if (!body.email) {
      return HttpResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }
    return HttpResponse.json(
      { id: 2, ...body },
      { status: 201 }
    );
  }),
];
