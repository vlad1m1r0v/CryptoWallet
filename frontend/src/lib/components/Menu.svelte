<script lang="ts">
    import {onMount} from "svelte";
    import {MediaQuery} from 'svelte/reactivity';
    import {page} from '$app/state';
    import {
        hideOverlayMenu,
        showStaticMenu,
        hideStaticMenu,
    } from '$lib/utilities/menu.ts';
    import {outsideClick} from "$lib/actions/outsideClick.ts";

    const large = new MediaQuery('min-width: 1199px');

    $effect(() => {
        if (large.current) {
            showStaticMenu();
        } else {
            hideStaticMenu();
        }
    });

    onMount(() => {
        window.addEventListener('resize', hideOverlayMenu);

        return () => {
            window.removeEventListener('resize', hideOverlayMenu);
        };
    });
</script>

{#snippet vuexyLogo()}
    <svg viewBox="0 0 139 95" version="1.1" xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xlink" height="24">
        <defs>
            <linearGradient id="linearGradient-1" x1="100%" y1="10.5120544%" x2="50%" y2="89.4879456%">
                <stop stop-color="#000000" offset="0%"></stop>
                <stop stop-color="#FFFFFF" offset="100%"></stop>
            </linearGradient>
            <linearGradient id="linearGradient-2" x1="64.0437835%" y1="46.3276743%" x2="37.373316%" y2="100%">
                <stop stop-color="#EEEEEE" stop-opacity="0" offset="0%"></stop>
                <stop stop-color="#FFFFFF" offset="100%"></stop>
            </linearGradient>
        </defs>
        <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="Artboard" transform="translate(-400.000000, -178.000000)">
                <g id="Group" transform="translate(400.000000, 178.000000)">
                    <path class="text-primary" id="Path"
                          d="M-5.68434189e-14,2.84217094e-14 L39.1816085,2.84217094e-14 L69.3453773,32.2519224 L101.428699,2.84217094e-14 L138.784583,2.84217094e-14 L138.784199,29.8015838 C137.958931,37.3510206 135.784352,42.5567762 132.260463,45.4188507 C128.736573,48.2809251 112.33867,64.5239941 83.0667527,94.1480575 L56.2750821,94.1480575 L6.71554594,44.4188507 C2.46876683,39.9813776 0.345377275,35.1089553 0.345377275,29.8015838 C0.345377275,24.4942122 0.230251516,14.560351 -5.68434189e-14,2.84217094e-14 Z"
                          style="fill:currentColor"></path>
                    <path id="Path1"
                          d="M69.3453773,32.2519224 L101.428699,1.42108547e-14 L138.784583,1.42108547e-14 L138.784199,29.8015838 C137.958931,37.3510206 135.784352,42.5567762 132.260463,45.4188507 C128.736573,48.2809251 112.33867,64.5239941 83.0667527,94.1480575 L56.2750821,94.1480575 L32.8435758,70.5039241 L69.3453773,32.2519224 Z"
                          fill="url(#linearGradient-1)" opacity="0.2"></path>
                    <polygon id="Path-2" fill="#000000" opacity="0.049999997"
                             points="69.3922914 32.4202615 32.8435758 70.5039241 54.0490008 16.1851325"></polygon>
                    <polygon id="Path-21" fill="#000000" opacity="0.099999994"
                             points="69.3922914 32.4202615 32.8435758 70.5039241 58.3683556 20.7402338"></polygon>
                    <polygon id="Path-3" fill="url(#linearGradient-2)" opacity="0.099999994"
                             points="101.428699 0 83.0667527 94.1480575 130.378721 47.0740288"></polygon>
                </g>
            </g>
        </g>
    </svg>
{/snippet}


{#snippet closeMenuIcon()}
    <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="feather feather-x d-block d-xl-none text-primary toggle-icon font-medium-4"
    >
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
{/snippet}

{#snippet profilesIcon()}
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="feather feather-user">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
    </svg>

{/snippet}

{#snippet walletsIcon()}
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="feather feather-credit-card">
        <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
        <line x1="1" y1="10" x2="23" y2="10"></line>
    </svg>
{/snippet}

{#snippet storeIcon()}
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="feather feather-shopping-bag">
        <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <path d="M16 10a4 4 0 0 1-8 0"></path>
    </svg>
{/snippet}

{#snippet chatIcon()}
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="feather feather-message-circle">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
    </svg>
{/snippet}

<div
        class="main-menu menu-fixed menu-light menu-accordion menu-shadow"
        use:outsideClick={{ ignore: '.menu-toggle' }}
        on:outsideclick={hideOverlayMenu}
>
    <div class="navbar-header expanded">
        <ul class="nav navbar-nav flex-row">
            <li class="nav-item mr-auto">
                <a class="navbar-brand" href=" ">
                    <span class="brand-logo">
                        {@render vuexyLogo()}
                    </span>
                    <h2 class="brand-text">CryptoWallet</h2>
                </a>
            </li>
            <li class="nav-item nav-toggle">
                <a
                        class="nav-link modern-nav-toggle pr-0"
                        on:click={hideOverlayMenu}
                        href=" "
                >
                    {@render closeMenuIcon()}
                </a>
            </li>
        </ul>
    </div>
    <div class="main-menu-content">
        <ul class="navigation navigation-main">
            <!--Profile-->
            <li
                    class="nav-item"
                    class:active={page.url.pathname.startsWith('/profiles/')}
            >
                <a class="d-flex align-items-center" href="/profiles/me">
                    {@render profilesIcon()}
                    <span class="menu-title text-truncate">Profile</span></a>
            </li>
            <!--Wallets-->
            <li
                    class="nav-item"
                    class:active={page.url.pathname === "/wallets"}
            >
                <a class="d-flex align-items-center" href="/wallets">
                    {@render walletsIcon()}
                    <span class="menu-title text-truncate">Wallets</span></a>
            </li>
            <!--iBay-->
            <li
                    class="nav-item"
                    class:active={page.url.pathname === "/ibay"}
            >
                <a class="d-flex align-items-center" href="/ibay">
                    {@render storeIcon()}
                    <span class="menu-title text-truncate">iBay</span></a>
            </li>
            <!--Chat-->
            <li
                    class="nav-item"
                    class:active={page.url.pathname === "/chat"}
            >
                <a class="d-flex align-items-center" href="/chat">
                    {@render chatIcon()}
                    <span class="menu-title text-truncate">Chat</span></a>
            </li>
        </ul>
    </div>
</div>