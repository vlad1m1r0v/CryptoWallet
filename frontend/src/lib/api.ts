import {PUBLIC_BACKEND_URL} from '$env/static/public';

import {goto} from "$app/navigation";

import {showToast} from "$lib/stores/toast.ts";
import {type LoginRequestData, type RegisterRequestData} from "$lib/types/api.ts";


const getAccessToken = () => localStorage.getItem("access_token") ?? sessionStorage.getItem("access_token");

export default class ApiClient {
    private static BACKEND_URL: string = PUBLIC_BACKEND_URL;

    private static async makeAuthorizedRequest(
        url: string,
        method: string,
        data?: Record<string | number | symbol, unknown> | null
    ) {
        const response = await fetch(url, {
            method,
            headers: {
                "Authorization": `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify(data)
        })

        const json = await response.json()

        if (!response.ok && response.status === 401) {
            showToast(json.description)
            return await goto("/login")
        }

        return json;
    }

    public static async register(data: RegisterRequestData) {
        return await fetch(`${this.BACKEND_URL}/auth/register`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
    }

    public static async login(data: LoginRequestData) {
        return await fetch(`${this.BACKEND_URL}/auth/login`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
    }

    public static async getMyProfile() {
        return await this.makeAuthorizedRequest(`${this.BACKEND_URL}/profiles/me`, "GET")
    }
}