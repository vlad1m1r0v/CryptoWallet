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
</script>
<div>
    <Info/>
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
    <a href={`https://sepolia.etherscan.io/tx/${transactionHash}`}>
        Transaction link
    </a>
</div>