import {z} from 'zod';

import {passwordRegex} from "$lib/schemas/patterns.ts";

export const registerSchema = z.object({
    username: z.string()
        .transform((val) => val.trim())
        .pipe(
            z.string()
                .min(5, 'Username must be at least 5 characters')
                .max(32, 'Username must be at most 32 characters')
        ),
    email: z.string().email('Invalid email address'),
    password: z
        .string()
        .min(8, 'Password must be at least 8 characters')
        .max(20, 'Password must be at most 20 characters')
        .regex(passwordRegex, 'Password must include lowercase, uppercase, digit and symbol'),
    repeat_password: z.string()
}).refine((data) => data.password === data.repeat_password, {
    path: ['repeat_password'],
    message: 'Passwords do not match'
});