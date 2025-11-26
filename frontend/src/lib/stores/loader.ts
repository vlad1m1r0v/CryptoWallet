import {writable} from "svelte/store";


interface Loader {
    isLoading: boolean
}

export const loader = writable<Loader>({isLoading: false});


