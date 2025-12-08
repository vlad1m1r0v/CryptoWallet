import HttpService from "$lib/services/http.ts";

import {orders} from "$lib/stores/orders.ts";

import type {
    OrderResponse,
    CreateOrderRequest
} from "$lib/types/api.ts";

import {toast} from "svelte-sonner";

export default class OrderService {
    static async getOrders(): Promise<void> {
        const response = await HttpService.request<OrderResponse[]>(
            '/orders',
            {method: 'GET'},
            true
        );

        if (response) orders.set(response);
    }

    static async createOrder(data: CreateOrderRequest): Promise<void> {
        const response = await HttpService.request<OrderResponse>('/orders', {
            method: 'POST',
            body: JSON.stringify(data)
        }, true);

        if (response) {
            toast.success("Order was created successfully.");
            orders.update((list) => [response, ...(list ?? [])])
        }
    }
}