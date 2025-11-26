import {z} from 'zod';

import {passwordRegex} from "$lib/schemas/patterns.ts";

export const profileSchema = z.object({
    username: z.string()
        .transform((val) => val.trim())
        .pipe(
            z.string()
                .min(5, 'Username must be at least 5 characters')
                .max(32, 'Username must be at most 32 characters')
        ),
    password: z.preprocess((val) => (val === '' ? undefined : val),
        z.string()
            .min(8, 'Password must be at least 8 characters')
            .max(20, 'Password must be at most 20 characters')
            .regex(passwordRegex, 'Password must include lowercase, uppercase, digit and symbol')
            .optional()
    ),
    repeat_password: z.preprocess((val) => (val === '' ? undefined : val),
        z.string()
            .optional()),
}).refine((data) => data.password === data.repeat_password, {
    path: ['repeat_password'],
    message: 'Passwords do not match'
});