import {z} from 'zod';

import {passwordRegex} from "$lib/schemas/patterns.ts";

export const loginSchema = z.object({
    email: z.string().email("Invalid email address"),
    password: z
        .string()
        .min(8, 'Password must be at least 8 characters')
        .max(20, 'Password must be at most 20 characters')
        .regex(passwordRegex, 'Password must include lowercase, uppercase, digit and symbol'),
    remember_me: z.boolean().optional()
});