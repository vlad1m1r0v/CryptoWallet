import {goto} from "$app/navigation";

import {toast} from "svelte-sonner";

import TokenService from "$lib/services/token.ts";
import HttpService from "$lib/services/http.ts";

import {user} from "$lib/stores/user.ts";

import {
    type LoginRequest,
    type RegisterRequest,
    type JwtResponse
} from "$lib/types/api.ts";

export default class AuthService {
    static async register(data: RegisterRequest): Promise<void> {
        const response = await HttpService.request<JwtResponse>(
            '/auth/register',
            {method: 'POST', body: JSON.stringify(data)}
        );

        if (response) {
            TokenService.saveToken(response["access_token"], true);
            toast.success("User registered successfully.");
            await goto("/profiles/me");
        }
    }

    static async login(data: LoginRequest): Promise<void> {
        const response = await HttpService.request<JwtResponse>(
            '/auth/login',
            {method: 'POST', body: JSON.stringify(data)}
        );

        if (response) {
            TokenService.saveToken(response["access_token"], Boolean(data.remember_me));
            await goto("/profiles/me");

            toast.success("User logged in successfully.");
        }
    }

    static async logout(): Promise<void> {
        TokenService.clearToken();
        user.set(null);
        await goto('/login');

        toast.success("User logged out successfully.");
    }
}