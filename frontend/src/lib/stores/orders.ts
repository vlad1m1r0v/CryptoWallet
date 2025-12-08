import {writable} from "svelte/store";

import type {OrderResponse} from "$lib/types/api.ts";

export const orders = writable<OrderResponse[] | null>(null);