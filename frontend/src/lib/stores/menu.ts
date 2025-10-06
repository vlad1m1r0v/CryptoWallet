import {writable} from "svelte/store";


export enum State {
    SMALL_SCREEN_HIDE,
    SMALL_SCREEN_OVERLAY,
    LARGE_SCREEN_STATIC,
    LARGE_SCREEN_COLLAPSED,
    LARGE_SCREEN_COLLAPSED_EXPANDED
}


interface Menu {
    state: State
}

export const menu = writable<Menu>({state: State.LARGE_SCREEN_STATIC});


