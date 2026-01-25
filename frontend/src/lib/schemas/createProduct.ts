import {z} from "zod";
import {productNameRegex} from "$lib/schemas/patterns.ts";
import {MAX_FILE_SIZE, ACCEPTED_IMAGE_TYPES} from "$lib/contstants.ts";

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
                    "Product name can contain letters, digits, and spaces. Example: 'iPhone 15', 'Чорний капітан'"
                )
        ),
    price: z.coerce.number()
        .gt(0.0002, "Price must be greater than 0.0002"),

    photo: z.any()
        .refine((file) => file instanceof File, "Product photo is required")
        .refine((file) => file?.size <= MAX_FILE_SIZE,
            (file) => ({
                message: `Max image size is 2MB. Your file is ${(file?.size / (1024 * 1024)).toFixed(2)}MB`
            })
        )
        .refine(
            (file) => ACCEPTED_IMAGE_TYPES.includes(file?.type),
            "Only .jpg, .jpeg, .png and .webp formats are supported"
        ),
});