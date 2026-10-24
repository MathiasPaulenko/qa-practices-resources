// Shared registration schema — the same rules validate the API payload and
// feed the demo form's client-side checks. Mirrors the Automation Examples
// section of the resource.
import { z } from 'zod';

export const registrationSchema = z.object({
  name: z.string().trim().min(1, 'required').max(120),
  email: z.string().trim().email().max(254),
  password: z.string().min(12, 'at least 12 characters').max(128),
  age: z.number().int().min(18).max(120),
  phone: z.string().regex(/^\+[1-9]\d{7,14}$/, 'Expected E.164 format'),
  startDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Expected ISO 8601 date')
});

export const loginSchema = registrationSchema.pick({ email: true, password: true });
