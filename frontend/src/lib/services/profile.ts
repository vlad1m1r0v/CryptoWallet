import {toast} from "svelte-sonner";

import HttpService from "$lib/services/http.ts";

import {user} from "$lib/stores/user.ts";
import {profile} from "$lib/stores/profile.ts";

import {
    type UserResponse
} from "$lib/types/api.ts";

export default class ProfileService {
    static async getMyProfile(): Promise<void> {
        const response = await HttpService.request<UserResponse>(
            '/profiles/me', {method: 'GET'}, true
        );

        if (response) {
            user.set(response);
        }
    }

    static async getProfile(userId: string): Promise<void> {
        const response = await HttpService.request<UserResponse>(
            `/profiles/${userId}`, {method: 'GET'}, true
        );

        if (response) {
            profile.set(response);
        }
    }

    static async updateProfile(data: FormData): Promise<void> {
        const response = await HttpService.request<UserResponse>('/profiles/me', {
            method: 'PATCH',
            body: data
        }, true);

        if (response) {
            user.set({...response});
            toast.success("User profile was successfully updated.")
        }
    }

    static async deleteAvatar(): Promise<void> {
        const response = await HttpService.request<UserResponse>(
            '/profiles/me/avatar',
            {method: 'DELETE'},
            true
        );

        if (response) {
            user.set({...response});
            toast.success("Avatar was removed successfully.")
        }
    }
}