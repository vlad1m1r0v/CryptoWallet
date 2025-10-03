<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    import Menu from "$lib/components/Menu.svelte";
    import Footer from "$lib/components/Footer.svelte";

    let {children} = $props();

</script>
<svelte:head>
    <!-- BEGIN: Page CSS-->
    <link rel="stylesheet" type="text/css" href="/vuexy/css/core/menu/menu-types/vertical-menu.css">
    <!-- END: Page CSS-->
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
    </div>
</div>
<div
        class="sidenav-overlay"
        style="touch-action: pan-y; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);"
>
</div>
<Footer/>