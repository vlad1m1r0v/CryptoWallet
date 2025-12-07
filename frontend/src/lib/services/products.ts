import HttpService from "$lib/services/http.ts";

import {products} from "$lib/stores/products.ts";

import type {
    ProductResponse
} from "$lib/types/api.ts";

export default class ProductService {
    static async getProducts(): Promise<void> {
        const response = await HttpService.request<ProductResponse[]>(
            '/products',
            {method: 'GET'},
            true
        );

        if (response) products.set(response);
    }
}