<style>
    input {
        cursor: not-allowed;
    }

    #wallets__container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
</style>
<script lang="ts">
    import {onMount} from "svelte";

    import {page} from '$app/state';

    import ProfileService from "$lib/services/profile.ts";

    import {profile} from "$lib/stores/profile.ts";

    onMount(async () => {
        const profileId = page.params.profileId;

        if (profileId) {
            await ProfileService.getProfile(profileId);
        }
    })
</script>
<!--Profile Header-->
<div class="content-header row">
    <div class="content-header-left col-md-9 col-12 mb-2">
        <h2 class="float-left mb-0">Profile</h2>
    </div>
</div>
<!--Profile Card-->
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <!--Form-->
                <form>
                    <!--Update Avatar-->
                    <div class="media">
                        <a href=" " class="mr-25">
                            <img
                                    src={$profile?.avatar_url?? "/vuexy/images/portrait/small/avatar-s-11.jpg"}
                                    class="rounded mr-50"
                                    alt="profile image"
                                    height="80"
                                    width="80"
                            >
                        </a>
                    </div>
                    <div class="row mt-1">
                        <div class="col-12">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input
                                        disabled
                                        type="text"
                                        class="form-control"
                                        name="username"
                                        placeholder="Username"
                                        value="{$profile?.username}"
                                >
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
<!--Statistics Header-->
<div class="content-header row">
    <div class="content-header-left col-md-9 col-12 mb-2">
        <h2 class="float-left mb-0">Statistics</h2>
    </div>
</div>
<!--Statistics Card-->
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <h4>
                    <span class="font-weight-bolder">Messages in chat:</span>
                    <span class="font-weight-light">{$profile?.total_messages}</span>
                </h4>
            </div>
        </div>
    </div>
</div>