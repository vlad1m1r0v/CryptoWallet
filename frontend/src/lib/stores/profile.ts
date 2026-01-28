import {writable} from "svelte/store";

import type {OtherProfileResponse} from "$lib/types/api.ts";

export const profile = writable<OtherProfileResponse | null>(null);