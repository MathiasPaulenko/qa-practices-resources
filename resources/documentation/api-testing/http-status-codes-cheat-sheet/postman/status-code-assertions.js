// Postman v11 / Newman 6.x — Tests tab snippets for status code assertions.
// Paste each block into the Tests tab of the matching request.

// Happy path: 200 with schema check
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Body is not empty", () => {
    const body = pm.response.json();
    pm.expect(body).to.not.be.empty;
});

// Created: 201 plus Location header contract
pm.test("Status is 201", () => pm.response.to.have.status(201));
pm.test("Location header points to new resource", () => {
    pm.expect(pm.response.headers.get("Location")).to.include("/users/");
});

// No content: 204 with empty body
pm.test("Status is 204", () => pm.response.to.have.status(204));
pm.test("Body is empty", () => pm.expect(pm.response.text()).to.be.empty);

// Auth boundaries
pm.test("Missing token returns 401", () => pm.response.to.have.status(401));
pm.test("WWW-Authenticate present", () =>
    pm.expect(pm.response.headers.get("WWW-Authenticate")).to.exist);
pm.test("Wrong role returns 403", () => pm.response.to.have.status(403));

// Validation: 4xx range and error body
pm.test("Status is 4xx", () =>
    pm.expect(pm.response.code).to.be.within(400, 499));
pm.test("Error body identifies the problem", () => {
    const body = pm.response.json();
    pm.expect(body).to.satisfy((b) => b.error || b.errors || b.title);
});

// Rate limiting: 429 with Retry-After
pm.test("Status is 429", () => pm.response.to.have.status(429));
pm.test("Retry-After present", () =>
    pm.expect(pm.response.headers.get("Retry-After")).to.exist);

// Server errors must not leak internals
pm.test("5xx body is sanitized", () => {
    const text = pm.response.text();
    pm.expect(text).to.not.match(/stack|trace|exception|at\s+[\w.]+\(/i);
});
