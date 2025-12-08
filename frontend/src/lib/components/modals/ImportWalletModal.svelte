<script lang="ts">
    const {
        isOpen,
        close,
    }: {
        isOpen: boolean,
        close: () => {},
    } = $props();

    import {fade, scale} from "svelte/transition";

    import {createForm} from "felte";
    import {validator} from "@felte/validator-zod";
    import {reporter} from "@felte/reporter-svelte";

    import {z} from "zod";

    import {outsideClick} from "$lib/actions/outsideClick.ts";

    import WalletService from "$lib/services/wallets.ts";

    import {importWalletSchema} from "$lib/schemas/importWallet.ts";

    type FormData = z.infer<typeof importWalletSchema>;

    const {form, errors, touched, isSubmitting, isValid, handleSubmit} = createForm<FormData>({
        onSubmit: async (values) => {
            await WalletService.importWallet(values);
            close();
        },
        extend: [
            validator({schema: importWalletSchema}),
            reporter()
        ]
    });
</script>
{#if isOpen}
    <div
            class="modal d-block text-left modal-primary"
            transition:fade|global={{duration: 200}}
            style="z-index: 3000"
    >
        <div class="modal-dialog modal-dialog-centered" role="document"
             transition:scale|global="{{ start: 0.8, duration: 200 }}">
            <div
                    class="modal-content"
                    use:outsideClick
                    on:outsideclick={close}
            >
                <div class="modal-header">
                    <h5 class="modal-title" id="myModalLabel160">Import ETH wallet</h5>
                    <button
                            type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            on:click={close}
                    >
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form use:form novalidate>
                        <div class="form-group">
                            <label for="private_key" class="form-label">Private key</label>
                            <input
                                    name="private_key"
                                    type="password"
                                    class="form-control"
                                    class:is-valid={!$errors.private_key && $touched.private_key}
                                    class:is-invalid={$errors.private_key && $touched.private_key}
                                    placeholder="Enter private key..."
                            />
                            {#if $touched.private_key && $errors.private_key}
                                <div class="invalid-feedback">{$errors.private_key[0]}</div>
                            {/if}
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <div class="flex flex-row">
                        <button
                                type="button"
                                disabled={$isSubmitting || !$isValid}
                                class="btn btn-primary waves-effect waves-float waves-light mr-1"
                                data-dismiss="modal"
                                on:click={handleSubmit}
                        >
                            Submit
                        </button>
                        <button
                                type="button"
                                class="btn btn-flat-primary waves-effect waves-float waves-light"
                                data-dismiss="modal"
                                on:click={close}
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}