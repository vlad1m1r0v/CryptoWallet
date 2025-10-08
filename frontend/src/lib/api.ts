import {PUBLIC_BACKEND_URL} from '$env/static/public';

import {type LoginRequestData, type RegisterRequestData} from "$lib/types/api.ts";

export default class ApiClient {
    private static BACKEND_URL: string = PUBLIC_BACKEND_URL;

    public static async register(data: RegisterRequestData) {
        return await fetch(`${this.BACKEND_URL}/auth/register`, {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
    }

    public static async login(data: LoginRequestData) {
        return await fetch(`${this.BACKEND_URL}/auth/login`, {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
    }
}