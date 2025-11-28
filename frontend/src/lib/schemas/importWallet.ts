import { z } from 'zod';

export const importWalletSchema = z.object({
    private_key: z
        .string()
        .min(32, 'Private key must be at least 32 characters long')
        .max(128, 'Private key must be at most 128 characters long'),
});