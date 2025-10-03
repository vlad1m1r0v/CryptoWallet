<script lang="ts">
    import {toasts, removeToast} from "$lib/stores/toast.ts";
    import {fade} from "svelte/transition";
    import {flip} from "svelte/animate";
</script>

<div aria-live="polite" aria-atomic="true" style="position: relative">
    <div style="position: fixed; top: 1rem; right: 1rem; z-index: 1030">
        {#each $toasts as toast (toast.id)}
            <div
                    class="toast show toast-stacked mb-2"
                    role="alert" aria-live="assertive" aria-atomic="true"
                    animate:flip={{duration: 200}}
                    in:fade={{ duration: 200 }}
                    out:fade={{ duration: 200 }}
            >
                <div class="toast-header">
                    <img src="/vuexy/images/logo/logo.png" class="mr-1" alt="Toast Image" height="18" width="25">
                    <strong class="mr-auto">CryptoWallet</strong>
                    <small class="text-muted">just now</small>
                    <button type="button" class="ml-1 close" aria-label="Close" on:click={() => removeToast(toast.id)}>
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="toast-body">{toast.message}</div>
            </div>
        {/each}
    </div>
</div>