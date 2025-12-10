<script lang="ts">
    import {Toaster} from "svelte-sonner";
    import {Jumper} from 'svelte-loading-spinners';

    import {Modals} from 'svelte-modals'

    import {loader} from "$lib/stores/loader.ts";

    let {children} = $props();
</script>

<svelte:head>
    <meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=0,minimal-ui">
    <meta name="description"
          content="Vuexy admin is super flexible, powerful, clean &amp; modern responsive bootstrap 4 admin template with unlimited possibilities.">
    <meta name="keywords"
          content="admin template, Vuexy admin template, dashboard template, flat admin template, responsive admin template, web app">
    <meta name="author" content="PIXINVENT">
    <link rel="apple-touch-icon" href="/vuexy/images/ico/apple-icon-120.png">
    <link rel="shortcut icon" type="image/x-icon" href="/vuexy/images/ico/favicon.ico">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;1,400;1,500;1,600"
          rel="stylesheet">

    <!-- BEGIN: Vendor CSS-->
    <link rel="stylesheet" type="text/css" href="/vuexy/vendors/css/vendors.min.css">
    <!-- END: Vendor CSS-->

    <!-- BEGIN: Theme CSS-->
    <link rel="stylesheet" type="text/css" href="/vuexy/css/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/bootstrap-extended.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/colors.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/components.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/themes/dark-layout.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/themes/bordered-layout.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/themes/semi-dark-layout.css">
    <!-- END: Theme CSS-->

    <!-- BEGIN: Feather Icons CSS-->
    <link rel="stylesheet" href="/vuexy/vendors/css/feather-icons/feather-icons.min.css">
    <!-- END: Feather Icons CSS-->

    <!--BEGIN: Loading overlay CSS-->
    <link rel="stylesheet" type="text/css" href="/custom/css/loading-overlay.css">
    <!--END: Loading overlay CSS-->

    <!--BEGIN: Page CSS-->
    <!--For auth pages-->
    <link rel="stylesheet" type="text/css" href="/vuexy/css/plugins/forms/form-validation.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/pages/page-auth.css">
    <!--For main pages-->
    <link rel="stylesheet" type="text/css" href="/vuexy/css/core/menu/menu-types/vertical-menu.css">
    <!--For chat-->
    <link rel="stylesheet" type="text/css" href="/vuexy/css/pages/app-chat.css">
    <link rel="stylesheet" type="text/css" href="/vuexy/css/pages/app-chat-list.css">
    <!--END: Page CSS-->
</svelte:head>
<Toaster/>
<Modals>
    {#snippet backdrop({close})}
        <div class="loader__overlay" onclick={() => close()}></div>
    {/snippet}
</Modals>
{#if $loader.isLoading}
    <div class="loader__overlay">
        <div class="loader__center">
            <Jumper size="60" color="#7367F0" unit="px" duration="1s"/>
        </div>
    </div>
{/if}
{@render children?.()}