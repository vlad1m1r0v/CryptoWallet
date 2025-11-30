<style>
    .wallet {
        display: grid;
        grid-template-columns: 100px 1fr;
        grid-template-rows: auto auto auto;
        grid-template-areas:
        "icon address"
        "icon balance"
        "icon actions";
        align-items: center;
    }

    @media (max-width: 576px) {
        .wallet {
            grid-template-columns: 1fr;
            grid-template-rows: auto;
            grid-template-areas:
            "icon"
            "address"
            "balance"
            "actions";
            row-gap: 8px;
        }
    }

    .wallet__icon {
        grid-area: icon;
        max-width: 100px;
        margin: 0 auto;
        aspect-ratio: auto;
    }

    .wallet__address {
        grid-area: address;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .wallet__balance {
        grid-area: balance;
    }

    .wallet__actions {
        grid-area: actions;
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }

    .wallet__actions > * {
        flex: 1 1 150px;
    }

    @media (max-width: 576px) {
        .wallet__actions {
            flex-direction: column;
            flex-wrap: nowrap;
        }

        .wallet__actions > * {
            flex: 1 1 100%;
        }
    }
</style>

<script>
    import {onMount} from "svelte";

    import {modals} from 'svelte-modals'

    import WalletService from "$lib/services/wallets.ts";

    import {wallets} from "$lib/stores/wallets.ts";

    import SendTransactionModal from "$lib/components/modals/SendTransactionModal.svelte";

    onMount(async () => {
        await WalletService.getWallets();
    })
</script>
<!--Wallets Header-->
<div class="content-header row">
    <div class="content-header-left col-md-9 col-12 mb-2">
        <h2 class="float-left mb-0">Wallets</h2>
    </div>
</div>
<!--Wallets-->
<div class="row">
    {#each $wallets as wallet (wallet.id)}
        <div class="col-sm-12 col-md-6">
            <div class="card">
                <div class="card-body p-1 wallet">
                    <img
                            src="/custom/images/ethereum.png"
                            alt="Ethereum"
                            class="wallet__icon"
                    >
                    <span class="wallet__address">
                    <span class="font-weight-bold">Address:</span>
                    <a
                            href={`https://sepolia.etherscan.io/address/${wallet.address}`}
                            class="font-weight-light"
                    >
                        {wallet.address}
                    </a>
                </span>
                    <span class="wallet__balance">
                    <span class="font-weight-bold">Balance:</span>
                    <span class="font-weight-light">{wallet.balance} {wallet.asset_symbol}</span>
                </span>
                    <div class="wallet__actions">
                        <button
                                type="button"
                                class="btn btn-sm btn-primary"
                        >
                            Watch transactions
                        </button>
                        <button
                                onclick={() => modals.open(SendTransactionModal, {fromAddress: wallet.address})}
                                type="button"
                                class="btn btn-sm btn-primary"
                        >
                            Send transaction
                        </button>
                        <button
                                onclick={async () => await WalletService.requestFreeETH({"wallet_id": wallet.id})}
                                type="button"
                                class="btn btn-sm btn-primary"
                        >
                            Get free ETH
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/each}
</div>