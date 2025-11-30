import HttpService from "$lib/services/http.ts";

import type {
    CreateTransactionRequest,
} from "$lib/types/api.ts";

export default class TransactionService {
    static async createTransaction(data: CreateTransactionRequest): Promise<void> {
        await HttpService.request<null>(
            '/transactions',
            {method: 'POST', body: JSON.stringify(data)},
            true
        );
    }
}