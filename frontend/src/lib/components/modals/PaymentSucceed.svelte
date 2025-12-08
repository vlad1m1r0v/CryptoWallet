<script lang="ts">
    const {
        isOpen,
        close,
        transactionHash
    }: {
        isOpen: boolean,
        close: () => {},
        transactionHash: string
    } = $props();

    import {fade, scale} from "svelte/transition";

    import {outsideClick} from "$lib/actions/outsideClick.ts";
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
                    <h5 class="modal-title" id="myModalLabel160">Payment transaction is sent</h5>
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
                    <p>Payment transaction is sent.</p>
                    <a href={`https://sepolia.etherscan.io/tx/${transactionHash}`}>Transaction link</a>
                </div>
                <div class="modal-footer">
                    <div class="flex flex-row">
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