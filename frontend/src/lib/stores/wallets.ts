import {writable} from "svelte/store";

import type {WalletResponse} from "$lib/types/api.ts";

export const wallets = writable<WalletResponse[] | null>(null);