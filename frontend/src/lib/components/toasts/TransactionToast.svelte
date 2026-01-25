<script lang="ts">
    import {TransactionTypeEnum} from "$lib/types/api.ts";

    import Info from "$lib/components/icons/Info.svelte";

    const {
        value,
        transactionFee,
        transactionType,
        address,
        transactionHash,
        assetSymbol
    }: {
        value: number,
        transactionFee: number,
        transactionType: TransactionTypeEnum,
        address: string,
        transactionHash: string,
        assetSymbol: string
    } = $props();

    const now = new Date();

    const hhmm = now.toLocaleString('en-GB', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: false
    });
</script>
<div class="d-flex align-items-start">
    <div class="mr-1">
        <Info/>
    </div>

    <div class="flex-grow-1">
        <div class="d-flex justify-content-between align-items-center" style="margin-bottom: 5px">
            <span class="font-weight-bold">New transaction</span>
            <span class="text-muted small">{hhmm}</span>
        </div>

        <div class="d-block" style="margin-bottom: 5px">
            {#if transactionType === TransactionTypeEnum.INCOME}
                <span>
                    {value} {assetSymbol} received to the wallet {address}
                </span>
            {/if}
            {#if transactionType === TransactionTypeEnum.EXPENSE}
                <span>
                    {value + transactionFee} {assetSymbol} taken from wallet {address}
                </span>
            {/if}
        </div>

        <a href={`https://sepolia.etherscan.io/tx/${transactionHash}`} class="d-block small">
            Transaction link
        </a>
    </div>
</div>