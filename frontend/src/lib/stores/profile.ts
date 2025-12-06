import {writable} from "svelte/store";

import type {UserResponse} from "$lib/types/api.ts";

export const profile = writable<UserResponse | null>(null);