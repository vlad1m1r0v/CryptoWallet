<script lang="ts">
    import {get} from 'svelte/store';

    import {createForm} from 'felte';
    import {validator} from '@felte/validator-zod';
    import {reporter} from '@felte/reporter-svelte';
    import {z} from 'zod';

    import ApiClient from "$lib/api.ts";

    import {user} from "$lib/stores/user.ts";

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,20}$/;
    const schema = z.object({
        username: z.string()
            .transform((val) => val.trim())
            .pipe(
                z.string()
                    .min(5, 'Username must be at least 5 characters')
                    .max(32, 'Username must be at most 32 characters')
            ),
        password: z.preprocess((val) => (val === '' ? undefined : val),
            z.string()
                .min(8, 'Password must be at least 8 characters')
                .max(20, 'Password must be at most 20 characters')
                .regex(passwordRegex, 'Password must include lowercase, uppercase, digit and symbol')
                .optional()
        ),
        repeat_password: z.preprocess((val) => (val === '' ? undefined : val),
            z.string()
                .optional()),
    }).refine((data) => data.password === data.repeat_password, {
        path: ['repeat_password'],
        message: 'Passwords do not match'
    });

    type FormData = z.infer<typeof schema>;

    const {form, setData, errors, touched, isSubmitting, isValid} = createForm<FormData>({
        onSubmit: async (values) => {
            touched.set({username: false, password: false, repeat_password: false});
            await ApiClient.updateMyProfile({...values, avatar: avatarFile});
        },
        extend: [
            validator({schema}),
            reporter()
        ]
    });

    let avatarFile: File | null = $state(null);
    let avatarPreview: string | null = $state("/vuexy/images/portrait/small/avatar-s-11.jpg");

    user.subscribe((state) => {
        if (state.username) setData("username", state.username);
        if (state.avatar_url) avatarPreview = state.avatar_url;
    });

    const onImageUpload = (e: Event) => {
        const file = (e.target as HTMLInputElement).files?.[0];
        if (!file) return;

        avatarFile = file;
        avatarPreview = URL.createObjectURL(file);
    };

    const resetAvatar = () => {
        if (avatarPreview) {
            URL.revokeObjectURL(avatarPreview);
            avatarPreview = get(user).avatar_url;
            avatarFile = null;
        }
    }
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
                                    src={avatarPreview}
                                    class="rounded mr-50"
                                    alt="profile image"
                                    height="80"
                                    width="80"
                            >
                        </a>
                        <div class="media-body mt-75 ml-1">
                            <label for="account-upload"
                                   class="btn btn-sm btn-primary mb-75 mr-75 waves-effect waves-float waves-light">Upload</label>
                            <input
                                    onchange={onImageUpload}
                                    type="file"
                                    id="account-upload"
                                    hidden=""
                                    accept="image/*"
                            >
                            <button
                                    type="button"
                                    class="btn btn-sm btn-outline-secondary mb-75 waves-effect"
                                    onclick={resetAvatar}
                            >
                                Reset
                            </button>
                            <p>Allowed JPG, GIF or PNG. Max size of 800kB</p>
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
                                        value="{$user.username}"
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
                                        value="{$user.email}">
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