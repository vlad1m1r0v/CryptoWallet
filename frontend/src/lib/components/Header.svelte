<script lang="ts">
    import {outsideClick} from "$lib/actions/outsideClick.ts";
    import Profile from "$lib/components/icons/Profile.svelte";
    import Logout from "$lib/components/icons/Logout.svelte";
    import Menu from "$lib/components/icons/Menu.svelte";

    import AuthService from "$lib/services/auth.ts";

    import {menu, MenuState} from "$lib/stores/menu.ts";
    import {user} from "$lib/stores/user.ts";

    let isDropdownMenuOpen = $state(false);

    const onLogoutClick = async () => {
        await AuthService.logout()
    }
</script>


<nav class="header-navbar navbar navbar-expand-lg align-items-center floating-nav navbar-light navbar-shadow">
    <div class="navbar-container d-flex content">
        <div class="bookmark-wrapper d-flex align-items-center">
            <ul class="nav navbar-nav d-xl-none">
                <li class="nav-item">
                    <a
                            class="nav-link menu-toggle"
                            on:click={() => {menu.set({state: MenuState.SMALL_SCREEN_OVERLAY})}}
                    >
                        <Menu/>
                    </a>
                </li>
            </ul>
        </div>
        <ul class="nav navbar-nav align-items-center ml-auto">
            <li class="nav-item dropdown dropdown-user"
                on:click={() => {isDropdownMenuOpen = !isDropdownMenuOpen}}
                use:outsideClick
                on:outsideclick={() => {isDropdownMenuOpen = false}}
            >
                <a class="nav-link dropdown-toggle dropdown-user-link"
                   id="dropdown-user"
                   href=" "
                   data-toggle="dropdown"
                   aria-haspopup="true"
                   aria-expanded="false"
                >
                    <div class="user-nav d-flex">
                        <span class="font-weight-bolder">{$user?.username}</span>
                    </div>
                    <span class="avatar">
                        <img
                                class="round"
                                src={$user?.avatar_url ?? "/vuexy/images/portrait/small/avatar-s-11.jpg"}
                                alt="avatar"
                                height="40"
                                width="40"
                        >
                        <span class="avatar-status-online"></span></span>
                </a>
                <div
                        class="dropdown-menu dropdown-menu-right"
                        class:show={isDropdownMenuOpen}
                        aria-labelledby="dropdown-user"
                >
                    <a class="dropdown-item" href="/profiles/me">
                        <Profile/>
                        Profile
                    </a>
                    <div class="dropdown-divider"></div>
                    <a
                            on:click|preventDefault={onLogoutClick}
                            class="dropdown-item"
                            role="button"
                    >
                        <Logout/>
                        Logout
                    </a>
                </div>
            </li>
        </ul>
    </div>
</nav>