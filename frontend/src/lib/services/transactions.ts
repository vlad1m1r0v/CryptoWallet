import {PUBLIC_BACKEND_URL} from '$env/static/public';

import qs from "qs";

import {get} from "svelte/store";

import {datagrid} from "$lib/stores/datagrid.ts";

import HttpService from "$lib/services/http.ts";
import TokenService from "$lib/services/token.ts";

import type {
    CreateTransactionRequest,
    PaginatedResponse,
    TransactionResponse
} from "$lib/types/api.ts";

export default class TransactionService {
    static async createTransaction(data: CreateTransactionRequest): Promise<void> {
        await HttpService.request<null>(
            '/transactions',
            {method: 'POST', body: JSON.stringify(data)},
            true
        );
    }

    static async getTransactions() {
        const state = get(datagrid);

        datagrid.update((dg) => ({...dg, isLoading: true}));

        const response = await fetch(
            `${PUBLIC_BACKEND_URL}/transactions?${qs.stringify(state.queryParams)}`,
            {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${TokenService.getToken()}`
                }
            }
        );

        datagrid.update((dg) => ({...dg, isLoading: false}));

        if (response) {
            const result: PaginatedResponse<TransactionResponse> = await response.json();
            datagrid.update((dg) => ({...dg, data: result}));
        }
    }
}