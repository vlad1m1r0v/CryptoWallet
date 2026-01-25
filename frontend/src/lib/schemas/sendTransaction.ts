import {z} from "zod";

import {TRANSACTION_FEE} from "$lib/contstants.ts";

export const createSendTransactionSchema = (balance: number) => {
    const maxAmount = balance - TRANSACTION_FEE;

    return z.object({
        to_address: z
            .string()
            .transform((v) => v.replace(/\s+/g, "")).pipe(
                z
                    .string()
                    .length(42, "Address must be exactly 42 characters long")
                    .refine((v) => v.startsWith("0x"), {message: "Address must start with '0x'"})
            ),

        amount: z
            .number({
                invalid_type_error: "Value must be a number",
            })
            .positive("Value must be positive")
            .max(maxAmount, `Value can't be bigger than ${maxAmount}`)
    });
}