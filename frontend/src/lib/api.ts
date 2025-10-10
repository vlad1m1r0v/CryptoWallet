import {PUBLIC_BACKEND_URL} from '$env/static/public';

import {goto} from "$app/navigation";

import {user, initialUserState} from "$lib/stores/user.ts";
import {showToast} from "$lib/stores/toast.ts";

import {
    type AccessTokenResponse,
    type ProfileResponse,
    type LoginRequest,
    type RegisterRequest,
    type UpdateProfileRequest,
} from "$lib/types/api.ts";

const getAccessToken = () => localStorage.getItem("access_token") ?? sessionStorage.getItem("access_token");

export default class ApiClient {
    private static get baseUrl() {
        return PUBLIC_BACKEND_URL.replace(/\/$/, '');
    }

    private static async request<T>(
        endpoint: string,
        options: RequestInit = {},
        authorized = false
    ): Promise<T | void> {
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            ...(options.headers as Record<string, string>),
        };

        if (authorized) {
            const token = getAccessToken();
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            ...options,
            headers,
        });

        const json = await response.json().catch(() => ({}));

        if (!response.ok) {
            showToast(json?.description ?? 'Unexpected error');
            if (response.status === 401) await this.logout();
            return;
        }

        return json as T;
    }

    public static async register(data: RegisterRequest): Promise<void> {
        const response = await this.request(
            '/auth/register',
            {method: 'POST', body: JSON.stringify(data)}
        );

        if (response) {
            localStorage.setItem("access_token", (response as AccessTokenResponse)["access_token"]);
        }

        showToast("User registered successfully.");

        await goto("/profiles/me");
    }

    public static async login(data: LoginRequest): Promise<void> {
        const response = await this.request(
            '/auth/login',
            {method: 'POST', body: JSON.stringify(data)}
        );

        if (response) {
            if (data.remember_me) {
                localStorage.setItem("access_token", (response as AccessTokenResponse)["access_token"])
            } else {
                sessionStorage.setItem("access_token", (response as AccessTokenResponse)["access_token"])
            }
        }

        showToast("User logged in successfully.");


        await goto("/profiles/me");
    }

    public static async getMyProfile(): Promise<void> {
        const response: ProfileResponse | void = await this.request('/profiles/me', {method: 'GET'}, true);

        if (response) {
            user.set({...response});
        }
    }

    public static async updateMyProfile(data: UpdateProfileRequest): Promise<void | ProfileResponse> {
        const response: ProfileResponse | void = await this.request('/profiles/me', {
            method: 'PATCH',
            body: JSON.stringify(data)
        }, true);

        if (response) {
            user.set({...response});
        }

        showToast("User profile was successfully updated.")
    }

    public static async logout(): Promise<void> {
        localStorage.removeItem('access_token');
        sessionStorage.removeItem('access_token');

        user.set({...initialUserState});

        await goto('/login');
    }
}