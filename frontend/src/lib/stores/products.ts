import {writable} from "svelte/store";

import type {ProductResponse} from "$lib/types/api.ts";

export const products = writable<ProductResponse[] | null>(null);