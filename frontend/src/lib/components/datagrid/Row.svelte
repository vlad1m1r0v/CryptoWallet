<script lang="ts">
    import {type TransactionResponse} from "$lib/types/api.ts";

    const {row}: { row: TransactionResponse } = $props();
</script>
<tr>
    <!--Hash-->
    <td>
        <a href={`https://sepolia.etherscan.io/tx/${row.transaction_hash}`}>
            {row.transaction_hash}
        </a>
    </td>
    <!--From-->
    <td>
        <a href={`https://sepolia.etherscan.io/address/${row.from_address}`}>
            {row.from_address}
        </a>
    </td>
    <!--To-->
    <td>
        <a href={`https://sepolia.etherscan.io/address/${row.to_address}`}>
            {row.to_address}
        </a>
    </td>
    <!--Value-->
    <td>{row.value} {row.asset_symbol}</td>
    <!--Created at-->
    <td>{row.created_at ?? ''}</td>
    <!--Fee-->
    <td>{row.transaction_fee} {row.asset_symbol}</td>
    <!--Status-->
    <td>
        <span
                class:text-success={row.transaction_status === "successful"}
                class:text-danger={row.transaction_status === "failed"}
                class:text-info={row.transaction_status === "pending"}
        >
            {row.transaction_status.toUpperCase()}
        </span>

    </td>
</tr>