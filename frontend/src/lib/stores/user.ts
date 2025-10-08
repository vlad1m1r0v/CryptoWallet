import {writable} from "svelte/store";


interface User {
    username: string | null;
    email: string | null;
    avatar_url: string | null
}

export const initialUserState: User = {
    username: null,
    email: null,
    avatar_url: null
}

export const user = writable<User>(initialUserState);