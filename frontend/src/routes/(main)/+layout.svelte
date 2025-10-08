<script lang="ts">
    import {onMount} from "svelte";
    import {get} from 'svelte/store';
    import {MediaQuery} from "svelte/reactivity";

    import ApiClient from "$lib/api.ts";

    import Header from "$lib/components/Header.svelte";
    import Menu from "$lib/components/Menu.svelte";
    import Footer from "$lib/components/Footer.svelte";
    import ToastContainer from "$lib/components/ToastContainer.svelte";

    import {menu, State} from "$lib/stores/menu.ts";
    import {user} from "$lib/stores/user.ts";


    let {children} = $props();
    // Responsive appbar
    const BASE_MENU_CLASSES = "vertical-layout navbar-floating footer-static pace-done"

    type CSSClasses = Record<State, string>;

    const CSS_CLASSES: CSSClasses = {
        [State.SMALL_SCREEN_HIDE]: `${BASE_MENU_CLASSES} vertical-overlay-menu menu-hide`,
        [State.SMALL_SCREEN_OVERLAY]: `${BASE_MENU_CLASSES} vertical-overlay-menu menu-open`,
        [State.LARGE_SCREEN_STATIC]: `${BASE_MENU_CLASSES} vertical-menu-modern menu-expanded`,
        [State.LARGE_SCREEN_COLLAPSED]: `${BASE_MENU_CLASSES} vertical-menu-modern menu-collapsed`,
        [State.LARGE_SCREEN_COLLAPSED_EXPANDED]: `${BASE_MENU_CLASSES} vertical-menu-modern menu-collapsed content-left-sidebar`,
    };

    $effect(() => {
        const current = $menu.state;
        document.body.className = CSS_CLASSES[current];
    });

    const large = new MediaQuery('min-width: 1199px');

    $effect(() => {
        if (large.current) {
            menu.set({state: State.LARGE_SCREEN_STATIC});
        } else {
            menu.set({state: State.SMALL_SCREEN_HIDE});
        }
    });

    const hideOverlayMenu = () => {
        const current = get(menu);
        if (current.state === State.SMALL_SCREEN_OVERLAY) {
            menu.set({state: State.SMALL_SCREEN_HIDE});
        }
    };

    onMount(() => {
        window.addEventListener('resize', hideOverlayMenu);

        return () => {
            window.removeEventListener('resize', hideOverlayMenu);
        };
    });

    onMount(async () => {
        const response = await ApiClient.getMyProfile();
        user.set({...response});
    })
</script>
<svelte:head>
    <title>CryptoWallet</title>
</svelte:head>

<Header/>
<Menu/>
<div class="app-content content">
    <div class="content-overlay"></div>
    <div class="header-navbar-shadow"></div>
    <div class="content-wrapper">
        <div class="content-body">
            {@render children?.()}
        </div>
        <ToastContainer/>
    </div>
</div>
<div
        class="sidenav-overlay"
        class:show={$menu.state === State.SMALL_SCREEN_OVERLAY}
        style="touch-action: pan-y; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);"
>
</div>
<Footer/>