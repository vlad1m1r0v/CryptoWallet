import {z} from "zod";
import {productNameRegex} from "$lib/schemas/patterns.ts";

export const createProductSchema = z.object({
    wallet_id: z.string().uuid(),

    name: z.string()
        .transform((val) => val.trim())
        .pipe(
            z.string()
                .min(3, "Name must be at least 3 characters")
                .max(50, "Name must be at most 50 characters")
                .regex(
                    productNameRegex,
                    "Product name must consist of words starting with a capital letter, optionally followed by digits. Example: 'iPhone 15', 'New Product'"
                )
        ),
    price: z.coerce.number()
        .gt(0.0002, "Price must be greater than 0.0002"),

    photo: z.any().refine(
        (file) => file instanceof File,
        "Product photo is required"
    ),
});