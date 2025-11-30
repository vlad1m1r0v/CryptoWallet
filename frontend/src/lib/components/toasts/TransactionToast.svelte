<script lang="ts">
    import {TransactionTypeEnum} from "$lib/types/api.ts";

    const {
        value,
        transactionFee,
        transactionType,
        walletAddress,
        transactionHash,
        assetSymbol
    }: {
        value: number,
        transactionFee: number,
        transactionType: TransactionTypeEnum,
        walletAddress: string,
        transactionHash: string,
        assetSymbol: string
    } = $props();


    console.log({
        value,
        transactionFee,
        transactionType,
        walletAddress,
        transactionHash,
        assetSymbol
    });
</script>
<div>
    {#if transactionType === TransactionTypeEnum.INCOME}
        <span>
            {value} {assetSymbol} received to the wallet {walletAddress}
        </span>
    {/if}
    {#if transactionType === TransactionTypeEnum.EXPENSE}
        <span>
            {value + transactionFee} {assetSymbol} taken from wallet {walletAddress}
        </span>
    {/if}
    <a href={`https://sepolia.etherscan.io/tx/${transactionHash}`}>
        Transaction link
    </a>
</div>