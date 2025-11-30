<script lang="ts">
    import {createForm} from 'felte';
    import {validator} from '@felte/validator-zod';
    import {reporter} from '@felte/reporter-svelte';

    import {z} from 'zod';

    import {modals} from 'svelte-modals'

    import ImportWalletModal from '$lib/components/modals/ImportWalletModal.svelte';

    import ProfileService from "$lib/services/profile.ts";
    import WalletService from "$lib/services/wallets.ts";

    import {user} from "$lib/stores/user.ts";

    import {profileSchema} from "$lib/schemas/profile.ts";


    type FormData = z.infer<typeof profileSchema>;

    const {form, setData, errors, touched, isSubmitting, isValid} = createForm<FormData>({
        onSubmit: async (values, context) => {
            touched.set({username: false, password: false, repeat_password: false});

            const formEl = context.form;
            const formData = new FormData();

            if (values.username) formData.set("username", values.username);

            if (values.password) formData.set("password", values.password);

            if (values.repeat_password) formData.set("repeat_password", values.repeat_password);

            const avatarInput = formEl?.querySelector<HTMLInputElement>('#avatar');
            if (avatarInput?.files?.length) {
                formData.set("avatar", avatarInput.files[0]);
            }

            await ProfileService.updateProfile(formData);
        },
        extend: [
            validator({schema: profileSchema}),
            reporter()
        ]
    });

    user.subscribe((state) => {
        if (state?.username) setData("username", state.username);
    });
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
                <form use:form>
                    <!--Update Avatar-->
                    <div class="media">
                        <a href=" " class="mr-25">
                            <img
                                    src={$user?.avatar_url?? "/vuexy/images/portrait/small/avatar-s-11.jpg"}
                                    class="rounded mr-50"
                                    alt="profile image"
                                    height="80"
                                    width="80"
                            >
                        </a>
                        <div class="media-body mt-75 ml-1 d-flex flex-column flex-sm-row align-items-sm-center">
                            <div class="mr-sm-1 mb-1 mb-sm-0">
                                <input name="avatar" class="form-control" type="file" id="avatar">
                            </div>

                            <button
                                    type="button"
                                    class="btn btn-danger waves-effect"
                                    onclick={async () => await ProfileService.deleteAvatar()}
                            >
                                Remove
                            </button>
                        </div>
                    </div>
                    <div class="row mt-1">
                        <div class="col-12 col-sm-6">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input
                                        type="text"
                                        class="form-control"
                                        name="username"
                                        class:is-valid={!$errors.username && $touched.username}
                                        class:is-invalid={$errors.username && $touched.username}
                                        placeholder="Username"
                                        value="{$user?.username}"
                                >
                                {#if $touched.username && $errors.username}
                                    <div class="invalid-feedback">{$errors.username[0]}</div>
                                {/if}
                            </div>
                        </div>
                        <div class="col-12 col-sm-6">
                            <div class="form-group">
                                <label for="email">E-mail</label>
                                <input
                                        disabled
                                        type="email"
                                        class="form-control"
                                        name="email"
                                        placeholder="Email"
                                        value="{$user?.email}">
                            </div>
                        </div>
                        <div class="col-12 col-sm-6">
                            <label for="password">Password</label>
                            <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    class="form-control"
                                    class:is-valid={!$errors.password && $touched.password}
                                    class:is-invalid={$errors.password && $touched.password}
                                    placeholder="············"
                                    aria-describedby="password"
                            />
                            {#if $touched.password && $errors.password}
                                <div class="invalid-feedback">{$errors.password[0]}</div>
                            {/if}
                        </div>
                        <div class="col-12 col-sm-6">
                            <label for="repeat_password">Repeat password</label>
                            <input
                                    id="repeat_password"
                                    name="repeat_password"
                                    type="password"
                                    class="form-control"
                                    class:is-valid={!$errors.repeat_password && $touched.repeat_password}
                                    class:is-invalid={$errors.repeat_password && $touched.repeat_password}
                                    placeholder="············"
                                    aria-describedby="repeat_password"
                            />
                            {#if $touched.repeat_password && $errors.repeat_password}
                                <div class="invalid-feedback">{$errors.repeat_password[0]}</div>
                            {/if}
                        </div>
                        <div class="col-12">
                            <button
                                    type="submit"
                                    class="btn btn-primary waves-effect waves-float waves-light mt-1"
                                    disabled={$isSubmitting || !$isValid}
                            >
                                {#if $isSubmitting}Submitting...{:else}Save changes{/if}
                            </button>
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
                    <span class="font-weight-light">{$user?.total_messages}</span>
                </h4>
                <h4>
                    <span class="font-weight-bolder">Wallets:</span>
                    <span class="font-weight-light">{$user?.total_wallets}</span>
                </h4>
            </div>
        </div>
    </div>
</div>
<!--Wallets Management Header-->
<div class="content-header row">
    <div class="content-header-left col-md-9 col-12 mb-2">
        <h2 class="float-left mb-0">Wallets Management</h2>
    </div>
</div>
<!--Wallets Management Card-->
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                {#each $user?.wallets as wallet (wallet.id)}
                    <!--Wallet-->
                    <div class="row mb-2">
                        <div class="d-inline-block text-truncate">
                            <img width="50" src="/custom/images/ethereum.png" alt="ethereum logo">
                            <span class="text-center font-weight-lighter">
                                {wallet.address}
                             </span>
                        </div>
                    </div>
                {/each}
                <!--Import / Create Wallet Buttons-->
                <div class="d-flex flex-column d-md-inline-block">
                    <button
                            type="button"
                            class="mb-1 mb-md-0 btn btn-primary waves-effect waves-float waves-light"
                            onclick={() => modals.open(ImportWalletModal)}
                    >
                        Import ETH Wallet
                    </button>
                    <button
                            type="button"
                            class="btn btn-primary waves-effect waves-float waves-light"
                            onclick={async () => await WalletService.createWallet()}
                    >
                        Create ETH Wallet
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>