import {z} from "zod";

export const createOrderSchema = z.object({
    wallet_id: z.string().uuid(),
});