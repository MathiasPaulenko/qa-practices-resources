// Simple in-memory fake repository (TypeScript)
class FakeUserRepository implements UserRepository {
  private users = new Map<number, User>();

  save(user: User): void {
    this.users.set(user.id, user);
  }

  findById(id: number): User | null {
    return this.users.get(id) ?? null;
  }
}
