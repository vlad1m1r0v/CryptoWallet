import {z} from "zod";
import {ACCEPTED_IMAGE_TYPES, MAX_FILE_SIZE} from "$lib/contstants.ts";

export const createMessageSchema = z
    .object({
        text: z
            .string()
            .transform((val) => val.trim())
            .transform((val) => (val === "" ? undefined : val))
            .pipe(
                z
                    .string()
                    .min(3, "Message must be at least 3 characters")
                    .max(200, "Message must be at most 200 characters")
            )
            .optional()
            .or(z.literal('')),
        image: z
            .any()
            .refine((file) => file instanceof File, "Product photo is required")
            .refine(
                (file) => file?.size <= MAX_FILE_SIZE,
                (file) => ({
                    message: `Max image size is 2MB. Your file is ${(
                        file?.size /
                        (1024 * 1024)
                    ).toFixed(2)}MB`,
                })
            )
            .refine(
                (file) => ACCEPTED_IMAGE_TYPES.includes(file?.type),
                "Only .jpg, .jpeg, .png and .webp formats are supported"
            )
    })
    .partial()
    .refine((data) => data.text || data.image, {
        message: "You must provide either a text message or an image.",
        path: ["text"],
    });