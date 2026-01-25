import {PUBLIC_BACKEND_URL} from '$env/static/public';

import {toast} from "svelte-sonner";

import {goto} from "$app/navigation";

import TokenService from "$lib/services/token.ts";

import {loader} from "$lib/stores/loader.ts";
import {user} from "$lib/stores/user.ts";


export default class HttpService {
    private static get baseUrl() {
        return PUBLIC_BACKEND_URL.replace(/\/$/, '');
    }

    public static async request<T>(
        endpoint: string,
        options: RequestInit = {},
        authorized = false
    ): Promise<T | void> {
        const headers: Record<string, string> = {
            ...(options.headers as Record<string, string>),
        };

        if (!(options.body instanceof FormData) && !headers['Content-Type']) {
            headers['Content-Type'] = 'application/json';
        }

        if (authorized) {
            const token = TokenService.getToken();
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }

        loader.set({isLoading: true});

        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            ...options,
            headers,
        });

        if (response.status === 204) {
            loader.set({isLoading: false});
            return;
        }

        const json = await response.json();

        loader.set({isLoading: false});

        if (!response.ok) {
            // Pydantic validation error
            if (response.status === 422) {
                Object.entries(json).forEach(([field, errors]) => {
                    if (Array.isArray(errors)) {
                        errors.forEach((msg) => toast.error(
                                field === "__model__" ? msg : `${field}: ${msg}`
                            )
                        )
                    }
                });

            // Access token not provided or is invalid
            } else if (response.status === 401) {
                toast.error(json?.description || 'Session expired');
                TokenService.clearToken();
                user.set(null);
                await goto('/login');

            } else {
                toast.error(json?.description ?? 'Unexpected error');
            }
            return;
        }

        return json as T;
    }
}