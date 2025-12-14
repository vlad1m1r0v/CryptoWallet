import {z} from "zod";

export const createMessageSchema = z.object({
    text: z.string()
        .transform((val) => val.trim())
        .pipe(
            z.string()
                .min(2, "Message must be at least 3 characters")
                .max(200, "Message must be at most 200 characters")
        ),
    image: z
        .any()
        .refine(
            (file) => file instanceof File,
            "Invalid file uploaded."
        )
        .optional()
});