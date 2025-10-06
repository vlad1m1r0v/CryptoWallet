import {writable} from "svelte/store";

export interface Toast {
    id: string;
    message: string;
}

export const toasts = writable<Toast[]>([]);

export function showToast(message: string, timeout = 5000) {
    const id = crypto.randomUUID();
    toasts.update((all) => [...all, {id, message}]);

    if (timeout) {
        setTimeout(() => removeToast(id), timeout);
    }
}

export function removeToast(id: string) {
    toasts.update((all) => all.filter((t) => t.id !== id));
}

export function clearToasts() {
    toasts.set([]);
}