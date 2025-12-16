import type { Component } from 'svelte';
import type {UserResponse} from "$lib/types/api.ts";

export default interface MenuItemProps {
    checkIsActive: (currentUrl: URL) => boolean;
    permissionCheck: (user: UserResponse | null) => boolean;
    Icon: Component;
    title: string;
    href: string;
}