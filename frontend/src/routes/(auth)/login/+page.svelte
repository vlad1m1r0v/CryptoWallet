<script lang="ts">
    import {createForm} from "felte";
    import {validator} from "@felte/validator-zod";
    import {reporter} from "@felte/reporter-svelte";
    import {z} from "zod";
    import Vuexy from "$lib/components/icons/Vuexy.svelte";

    // Валідація
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])/;
    const schema = z.object({
        email: z.string().email("Invalid email address"),
        password: z
            .string()
            .min(8, 'Password must be at least 8 characters')
            .max(20, 'Password must be at most 20 characters')
            .regex(passwordRegex, 'Password must include lowercase, uppercase, digit and symbol'),
        remember_me: z.boolean().optional()
    });

    type FormData = z.infer<typeof schema>;

    const {form, errors, touched, isSubmitting, isValid} = createForm<FormData>({
        onSubmit: (values) => {
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

    <!-- Email -->
    <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
                id="email"
                name="email"
                type="text"
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

    <!-- Remember me -->
    <div class="form-group">
        <div class="custom-control custom-checkbox">
            <input
                    id="remember_me"
                    name="remember_me"
                    type="checkbox"
                    class="custom-control-input"
            />
            <label class="custom-control-label" for="remember_me">
                Remember Me
            </label>
        </div>
    </div>

    <!-- Submit -->
    <button
            type="submit"
            class="btn btn-primary btn-block waves-effect waves-float waves-light"
            disabled={$isSubmitting || !$isValid}
    >
        {#if $isSubmitting}Signing in...{:else}Sign in{/if}
    </button>
</form>

<p class="text-center mt-2">
    <span>New on our platform?</span>
    <a href="register"><span>Create an account</span></a>
</p>