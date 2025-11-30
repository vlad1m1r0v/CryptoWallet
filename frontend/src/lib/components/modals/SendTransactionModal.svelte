<script lang="ts">
    const {
        isOpen,
        close,
        fromAddress
    }: {
        isOpen: boolean,
        close: () => {},
        fromAddress: string
    } = $props();

    import {fade, scale} from "svelte/transition";

    import {createForm} from "felte";
    import {validator} from "@felte/validator-zod";
    import {reporter} from "@felte/reporter-svelte";

    import {z} from "zod";

    import TransactionService from "$lib/services/transactions.ts";

    import {outsideClick} from "$lib/actions/outsideClick.ts";

    import {sendTransactionSchema} from "$lib/schemas/sendTransaction.ts";

    type FormData = z.infer<typeof sendTransactionSchema>;

    const {form, errors, touched, isSubmitting, isValid, handleSubmit} = createForm<FormData>({
        onSubmit: async (amounts) => {
            await TransactionService.createTransaction({...amounts, from_address: fromAddress});
            close();
        },
        extend: [
            validator({schema: sendTransactionSchema}),
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
        <div
                class="modal-dialog modal-dialog-centered" role="document"
                transition:scale|global="{{ start: 0.8, duration: 200 }}"
        >
            <div
                    class="modal-content"
                    use:outsideClick
                    on:outsideclick={close}
            >
                <div class="modal-header">
                    <h5 class="modal-title" id="myModalLabel160">Send ETH</h5>
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
                    <form use:form>
                        <!--To Address-->
                        <div class="form-group">
                            <label for="to_address" class="form-label">To address</label>
                            <input
                                    name="to_address"
                                    type="text"
                                    class="form-control"
                                    class:is-valid={!$errors.to_address && $touched.to_address}
                                    class:is-invalid={$errors.to_address && $touched.to_address}
                                    placeholder="Enter address..."
                            />
                            {#if $touched.to_address && $errors.to_address}
                                <div class="invalid-feedback">{$errors.to_address[0]}</div>
                            {/if}
                        </div>
                        <!--Value-->
                        <div class="form-group">
                            <label for="amount" class="form-label">Value</label>
                            <input
                                    name="amount"
                                    type="number"
                                    class="form-control"
                                    class:is-valid={!$errors.amount && $touched.amount}
                                    class:is-invalid={$errors.amount && $touched.amount}
                                    placeholder="Enter amount..."
                            />
                            {#if $touched.amount && $errors.amount}
                                <div class="invalid-feedback">{$errors.amount[0]}</div>
                            {/if}
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <div class="flex flex-row">
                        <button
                                type="button"
                                disabled={$isSubmitting || !$isValid}
                                id="import-eth-wallet__button"
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