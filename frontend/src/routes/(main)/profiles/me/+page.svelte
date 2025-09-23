<script lang="ts">
    import PasswordInput from "$lib/components/PasswordInput.svelte";
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
                <!--Update Avatar-->
                <div class="media">
                    <a href=" " class="mr-25">
                        <img
                                src="/vuexy/images/portrait/small/avatar-s-11.jpg"
                                class="rounded mr-50"
                                alt="profile image"
                                height="80"
                                width="80"
                        >
                    </a>
                    <div class="media-body mt-75 ml-1">
                        <label for="account-upload"
                               class="btn btn-sm btn-primary mb-75 mr-75 waves-effect waves-float waves-light">Upload</label>
                        <input type="file" id="account-upload" hidden="" accept="image/*">
                        <button class="btn btn-sm btn-outline-secondary mb-75 waves-effect">Reset</button>
                        <p>Allowed JPG, GIF or PNG. Max size of 800kB</p>
                    </div>
                </div>
                <!--Form-->
                <form class="mt-2">
                    <div class="row">
                        <div class="col-12 col-sm-6">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input
                                        type="text"
                                        class="form-control"
                                        name="username"
                                        placeholder="Username"
                                        value="johndoe"
                                >
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
                                        value="johndoe@domain.com">
                            </div>
                        </div>
                        <div class="col-12 col-sm-6">
                            <PasswordInput label="Password"/>
                        </div>
                        <div class="col-12 col-sm-6">
                            <PasswordInput label="Repeat Password"/>
                        </div>
                        <div class="col-12">
                            <button
                                    type="submit"
                                    class="btn btn-primary waves-effect waves-float waves-light">Save changes
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
                    <span class="font-weight-light">100</span>
                </h4>
                <h4>
                    <span class="font-weight-bolder">Wallets:</span>
                    <span class="font-weight-light">5</span>
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
                <!--Wallet-->
                <div class="row mb-2">
                    <div class="d-inline-block text-truncate">
                        <img width="50" src="/vuexy/images/ethereum.png" alt="ethereum logo">
                        <span class="text-center font-weight-lighter">
                                0xf04555b42b45E5283F28737D6BA65AE16878D84B
                             </span>
                    </div>
                </div>
                <!--Wallet-->
                <div class="row mb-2">
                    <div class="d-inline-block text-truncate">
                        <img width="50" src="/vuexy/images/ethereum.png" alt="ethereum logo">
                        <span class="text-center font-weight-lighter">
                                0xf04555b42b45E5283F28737D6BA65AE16878D84B
                             </span>
                    </div>
                </div>
                <!--Wallet-->
                <div class="row mb-2">
                    <div class="d-inline-block text-truncate">
                        <img width="50" src="/vuexy/images/ethereum.png" alt="ethereum logo">
                        <span class="text-center font-weight-lighter">
                                0xf04555b42b45E5283F28737D6BA65AE16878D84B
                             </span>
                    </div>
                </div>
                <!--Wallet-->
                <div class="row mb-2">
                    <div class="d-inline-block text-truncate">
                        <img width="50" src="/vuexy/images/ethereum.png" alt="ethereum logo">
                        <span class="text-center font-weight-lighter">
                                0xf04555b42b45E5283F28737D6BA65AE16878D84B
                             </span>
                    </div>
                </div>
                <!--Wallet-->
                <div class="row mb-2">
                    <div class="d-inline-block text-truncate">
                        <img width="50" src="/vuexy/images/ethereum.png" alt="ethereum logo">
                        <span class="text-center font-weight-lighter">
                                0xf04555b42b45E5283F28737D6BA65AE16878D84B
                             </span>
                    </div>
                </div>
                <!--Import / Create Wallet Buttons-->
                <div class="d-flex flex-column d-md-inline-block">
                    <button
                            type="button"
                            class="mb-1 mb-md-0 btn btn-primary waves-effect waves-float waves-light"
                    >
                        Import ETH Wallet
                    </button>
                    <button type="button" class="btn btn-primary waves-effect waves-float waves-light">Create ETH
                        Wallet
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
<!--Modal For Wallet Import-->