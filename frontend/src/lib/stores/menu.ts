import {writable} from "svelte/store";


export enum MenuState {
    SMALL_SCREEN_HIDE,
    SMALL_SCREEN_OVERLAY,
    LARGE_SCREEN_STATIC,
    LARGE_SCREEN_COLLAPSED,
    LARGE_SCREEN_COLLAPSED_EXPANDED
}


interface Menu {
    state: MenuState
}

export const menu = writable<Menu>({state: MenuState.LARGE_SCREEN_STATIC});


