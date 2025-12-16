<script lang="ts">
    import {get} from "svelte/store";

    import type {UserResponse} from "$lib/types/api.ts";

    import {outsideClick} from "$lib/actions/outsideClick.ts";

    import type MenuItemProps from "$lib/components/menu/types.ts";

    import Vuexy from "$lib/components/icons/Vuexy.svelte";
    import CloseMenu from "$lib/components/icons/CloseMenu.svelte";
    import Profile from "$lib/components/icons/Profile.svelte";
    import Wallets from "$lib/components/icons/Wallets.svelte";
    import Store from "$lib/components/icons/Store.svelte";
    import Chat from "$lib/components/icons/Chat.svelte";
    import CollapsedMenu from "$lib/components/icons/CollapsedMenu.svelte";
    import ExpandedMenu from "$lib/components/icons/ExpandedMenu.svelte";

    import MenuItem from "$lib/components/menu/MenuItem.svelte";

    import {menu, MenuState} from "$lib/stores/menu.ts";
    import {user} from "$lib/stores/user.ts";

    const onMouseEnter = () => {
        const current = get(menu);
        if (current.state === MenuState.LARGE_SCREEN_COLLAPSED) {
            menu.set({state: MenuState.LARGE_SCREEN_COLLAPSED_EXPANDED});
        }
    };

    const onMouseLeave = () => {
        const current = get(menu);
        if (current.state === MenuState.LARGE_SCREEN_COLLAPSED_EXPANDED) {
            menu.set({state: MenuState.LARGE_SCREEN_COLLAPSED});
        }
    };

    const onToggleIconClick = () => {
        const current = get(menu);

        if (current.state === MenuState.SMALL_SCREEN_OVERLAY) {
            menu.set({state: MenuState.SMALL_SCREEN_HIDE});
        }

        if (current.state === MenuState.LARGE_SCREEN_STATIC) {
            menu.set({state: MenuState.LARGE_SCREEN_COLLAPSED_EXPANDED});
        }

        if ([MenuState.LARGE_SCREEN_COLLAPSED, MenuState.LARGE_SCREEN_COLLAPSED_EXPANDED].includes(current.state)) {
            menu.set({state: MenuState.LARGE_SCREEN_STATIC});
        }
    }

    const onOutsideClick = () => {
        const current = get(menu);

        if (current.state === MenuState.SMALL_SCREEN_OVERLAY) {
            menu.set({state: MenuState.SMALL_SCREEN_HIDE});
        }
    };

    const initialMenuItems: MenuItemProps[] = [
        {
            Icon: Profile,
            checkIsActive: (currentUrl: URL) => currentUrl.pathname.startsWith('/profiles/'),
            permissionCheck: () => true,
            title: "Profile",
            href: "/profiles/me"
        },
        {
            Icon: Wallets,
            checkIsActive: (currentUrl: URL) => currentUrl.pathname === "/wallets",
            permissionCheck: () => true,
            title: "Wallets",
            href: "/wallets"
        },
        {
            Icon: Store,
            checkIsActive: (currentUrl: URL) => currentUrl.pathname === "/ibay",
            permissionCheck: () => true,
            title: "iBay",
            href: "/ibay"
        },
        {
            Icon: Chat,
            checkIsActive: (currentUrl: URL) => currentUrl.pathname === "/chat",
            permissionCheck: (u: UserResponse | null) => Boolean(u?.permissions.has_chat_access),
            title: "Chat",
            href: "/chat"
        }
    ];

    let menuItems = $state<MenuItemProps[]>(initialMenuItems);

    user.subscribe((u) => {
        menuItems = initialMenuItems.filter(item => item.permissionCheck(u));
    });
</script>
<div
        class="main-menu menu-fixed menu-light menu-accordion menu-shadow"
        class:expanded={$menu.state === MenuState.LARGE_SCREEN_COLLAPSED_EXPANDED}
        on:mouseenter={onMouseEnter}
        on:mouseleave={onMouseLeave}
        use:outsideClick={{ignore: ".bookmark-wrapper"}}
        on:outsideclick={onOutsideClick}
>
    <div class="navbar-header expanded">
        <ul class="nav navbar-nav flex-row">
            <li class="nav-item mr-auto">
                <a
                        class="navbar-brand"
                        href=" "
                >
                    <span class="brand-logo">
                        <Vuexy/>
                    </span>
                    <h2 class="brand-text">Vuexy</h2>
                </a>
            </li>
            <li class="nav-item nav-toggle">
                <a
                        class="nav-link modern-nav-toggle pr-0"
                        href=" "
                        on:click|preventDefault={onToggleIconClick}
                >
                    <CloseMenu/>
                    {#if $menu.state === MenuState.LARGE_SCREEN_STATIC}
                        <ExpandedMenu/>
                    {:else if [MenuState.LARGE_SCREEN_COLLAPSED, MenuState.LARGE_SCREEN_COLLAPSED_EXPANDED].includes($menu.state)}
                        <CollapsedMenu/>
                    {/if}
                </a>
            </li>
        </ul>
    </div>
    <div class="main-menu-content">
        <ul class="navigation navigation-main">
            {#each menuItems as item (item.href)}
                <MenuItem {...item}/>
            {/each}
        </ul>
    </div>
</div>