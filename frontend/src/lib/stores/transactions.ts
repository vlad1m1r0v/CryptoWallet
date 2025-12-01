import {writable} from "svelte/store";

import type {
    PaginatedResponse,
    TransactionResponse
} from "$lib/types/api.ts";

export const transactions = writable<PaginatedResponse<TransactionResponse> | null>(null);