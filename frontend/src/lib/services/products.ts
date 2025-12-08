import HttpService from "$lib/services/http.ts";

import {products} from "$lib/stores/products.ts";

import type {
    ProductResponse
} from "$lib/types/api.ts";

import {toast} from "svelte-sonner";

export default class ProductService {
    static async getProducts(): Promise<void> {
        const response = await HttpService.request<ProductResponse[]>(
            '/products',
            {method: 'GET'},
            true
        );

        if (response) products.set(response);
    }

    static async createProduct(data: FormData): Promise<void> {
        const response = await HttpService.request<ProductResponse>('/products', {
            method: 'POST',
            body: data
        }, true);

        if (response) {
            toast.success("Product was created successfully.")
        }
    }
}