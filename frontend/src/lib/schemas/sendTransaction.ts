import {z} from "zod";

export const sendTransactionSchema = z.object({
    to_address: z
        .string()
        .trim()
        .length(42, "Address must be exactly 42 characters long")
        .refine((v) => v.startsWith("0x"), {
            message: "Address must start with '0x'",
        }),

    amount: z
        .number({
            invalid_type_error: "Value must be a number",
        })
        .min(0.00001, "Value must be at least 0.00001")
        .max(1, "Value must be at most 1"),
});