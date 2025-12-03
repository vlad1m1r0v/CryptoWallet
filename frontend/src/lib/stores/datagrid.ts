import {writable} from "svelte/store";

import type {
    PaginatedResponse,
    TransactionResponse
} from "$lib/types/api.ts";

interface QueryParams {
    wallet_id?: string,
    sort: "created_at" | "transaction_fee" | "transaction_status";
    order: "asc" | "desc";
    page: number;
    per_page: number;
}

interface Datagrid {
    isLoading: boolean;
    data: PaginatedResponse<TransactionResponse>;
    queryParams: QueryParams;
}

export const datagrid = writable<Datagrid>({
    isLoading: false,
    data: {
        total_pages: 0,
        total_records: 0,
        page: 1,
        per_page: 20,
        items: []
    },
    queryParams: {
        sort: "created_at",
        order: "desc",
        page: 1,
        per_page: 20
    }
});