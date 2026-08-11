from behave_kit import fixture, skip_if_env, when_if


@fixture("database")
def database_fixture(context):
    def setup(ctx):
        import sqlite3
        ctx.db = sqlite3.connect(":memory:")
        ctx.db.execute("CREATE TABLE users (name TEXT, email TEXT)")
    def teardown(ctx):
        if hasattr(ctx, "db"):
            ctx.db.close()
    return (setup, teardown)


@skip_if_env("production")
@when("I reset the test database")
def step_reset_db(context):
    if hasattr(context, "db"):
        context.db.execute("DELETE FROM users")


@when_if(lambda ctx: hasattr(ctx, "db"))
@when("I seed a default user")
def step_seed_user(context):
    context.db.execute("INSERT INTO users VALUES ('Alice', 'alice@qapractices.com')")
