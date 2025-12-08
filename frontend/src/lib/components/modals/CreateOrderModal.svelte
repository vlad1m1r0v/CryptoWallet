<script lang="ts">
    const {
        isOpen,
        close,
        productName,
        productId
    }: {
        isOpen: boolean,
        close: () => {},
        productName: string,
        productId: string
    } = $props();

    import {fade, scale} from "svelte/transition";

    import {createForm} from "felte";
    import {validator} from "@felte/validator-zod";
    import {reporter} from "@felte/reporter-svelte";

    import {z} from "zod";

    import {createOrderSchema} from "$lib/schemas/createOrder.ts";

    import {outsideClick} from "$lib/actions/outsideClick.ts";

    import OrderService from "$lib/services/orders.ts";
    import WalletService from "$lib/services/wallets.ts";

    import {wallets} from "$lib/stores/wallets.ts";

    type FormData = z.infer<typeof createOrderSchema>;

    const {form, errors, touched, isSubmitting, isValid, handleSubmit} = createForm<FormData>({
        onSubmit: async (values) => {
            await OrderService.createOrder({...values, product_id: productId});
            close();
        },
        extend: [
            validator({schema: createOrderSchema}),
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
                    <h5 class="modal-title" id="myModalLabel160">Ordering of product {productName}</h5>
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
                        <!--Wallet-->
                        <div class="form-group">
                            <label for="wallet_id" class="form-label">Wallet</label>
                            <select
                                    class="form-control"
                                    name="wallet_id"
                                    on:focus={async () => {await WalletService.getWallets()}}
                            >
                                {#each $wallets as wallet (wallet.id)}
                                    <option value={wallet.id}>
                                        {wallet.address} ({wallet.balance} {wallet.asset_symbol})
                                    </option>
                                {/each}
                            </select>
                            {#if $touched.wallet_id && $errors.wallet_id}
                                <div class="invalid-feedback">{$errors.wallet_id[0]}</div>
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
                            Create
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