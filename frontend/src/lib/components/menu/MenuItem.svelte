<script lang="ts">
    import {page} from '$app/state';

    import {get} from "svelte/store";

    import {menu, MenuState} from '$lib/stores/menu.ts';
    import type MenuItemProps from "$lib/components/menu/types.ts";


    let {
        checkIsActive,
        Icon,
        title,
        href
    }: MenuItemProps = $props();

    let isActive = $derived(checkIsActive(page.url));

    const onClick = () => {
        const current = get(menu);

        if (current.state === MenuState.SMALL_SCREEN_OVERLAY) {
            menu.set({state: MenuState.SMALL_SCREEN_HIDE})
        }
    }

</script>

<li class="nav-item" class:active={isActive}>
    <a
            onclick={onClick}
            class="d-flex align-items-center"
            href={href}
    >
        <Icon/>
        <span class="menu-title text-truncate">{title}</span>
    </a>
</li>