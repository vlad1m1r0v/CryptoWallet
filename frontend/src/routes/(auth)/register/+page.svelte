<script lang="ts">
    import {createForm} from 'felte';
    import {validator} from '@felte/validator-zod';
    import {reporter} from '@felte/reporter-svelte';
    import {z} from 'zod';

    import {goto} from "$app/navigation";

    import ApiClient from "$lib/api.ts";
    import Vuexy from '$lib/components/icons/Vuexy.svelte';
    import {showToast} from "$lib/stores/toast.ts";

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])/;
    const schema = z.object({
        username: z.string().min(1, 'Username is required'),
        email: z.string().email('Invalid email address'),
        password: z
            .string()
            .min(8, 'Password must be at least 8 characters')
            .max(20, 'Password must be at most 20 characters')
            .regex(passwordRegex, 'Password must include lowercase, uppercase, digit and symbol'),
        repeat_password: z.string()
    }).refine((data) => data.password === data.repeat_password, {
        path: ['repeat_password'],
        message: 'Passwords do not match'
    });

    type FormData = z.infer<typeof schema>;

    const {form, errors, touched, isSubmitting, isValid} = createForm<FormData>({
        onSubmit: async (values) => {
            const response = await ApiClient.register(values);
            const json = await response.json();

            if (response.ok) {
                showToast("User registered successfully.");
                localStorage.setItem("access_token", json.access_token);
                await goto("profiles/me");
            } else {
                showToast(json.description);
            }
        },
        extend: [
            validator({schema}),
            reporter()
        ]
    });
</script>

<form use:form class="mt-2" novalidate>
    <a href=" " class="brand-logo d-flex align-items-center mb-3">
        <Vuexy/>
        <h2 class="brand-text text-primary ml-1 mb-0">CryptoWallet</h2>
    </a>

    <!-- Username -->
    <div class="form-group">
        <label for="username" class="form-label">Username</label>
        <input
                id="username"
                name="username"
                class="form-control"
                class:is-valid={!$errors.username && $touched.username}
                class:is-invalid={$errors.username && $touched.username}
                placeholder="johndoe"
                aria-describedby="username"
        />
        {#if $touched.username && $errors.username}
            <div class="invalid-feedback">{$errors.username[0]}</div>
        {/if}
    </div>

    <!-- Email -->
    <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
                id="email"
                name="email"
                class="form-control"
                class:is-valid={!$errors.email && $touched.email}
                class:is-invalid={$errors.email && $touched.email}
                placeholder="john@example.com"
                aria-describedby="email"
        />
        {#if $touched.email && $errors.email}
            <div class="invalid-feedback">{$errors.email[0]}</div>
        {/if}
    </div>

    <!-- Password -->
    <div class="form-group">
        <label for="password" class="form-label">Password</label>
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

    <!-- Repeat password -->
    <div class="form-group">
        <label for="repeat_password" class="form-label">Repeat password</label>
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

    <button
            type="submit"
            class="btn btn-primary btn-block waves-effect waves-float waves-light"
            disabled={$isSubmitting || !$isValid}
    >
        {#if $isSubmitting}Submitting...{:else}Sign up{/if}
    </button>
</form>

<p class="text-center mt-2">
    <span>Already have an account?</span>
    <a href="login"><span>Sign in instead</span></a>
</p>