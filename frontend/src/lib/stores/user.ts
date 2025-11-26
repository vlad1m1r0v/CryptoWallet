import {writable} from "svelte/store";

import type {UserResponse} from "$lib/types/api.ts";

export const user = writable<UserResponse | null>(null);