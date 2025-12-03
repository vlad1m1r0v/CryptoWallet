<style>
    #container {
        display: grid;
        height: calc(100vh - 200px);
        grid-template-areas: "grid" "paginator";
        gap: 10px;
        grid-template-rows: 1fr max(25px, fitcontent);
        align-items: center;
    }

    #container #grid {
        grid-area: grid;
        width: 100%;
        height: 100%;
        overflow: auto;
    }

    #container #paginator {
        grid-area: paginator;
        overflow-x: auto;
    }
</style>
<script lang="ts">


    import {onMount} from "svelte";
    import {get, derived} from "svelte/store";

    const {walletId}: { walletId: string } = $props();

    import ColumnHeader from "$lib/components/datagrid/ColumnHeader.svelte";
    import Row from "$lib/components/datagrid/Row.svelte";
    import Paginator from "$lib/components/datagrid/Paginator.svelte";

    import {datagrid} from "$lib/stores/datagrid.ts";

    import TransactionService from "$lib/services/transactions.ts";

    import type {ColumnHeaderProps} from "$lib/components/datagrid/types.ts";

    onMount(async () => {
        datagrid.update((dg) => ({...dg,
            queryParams: {
                ...dg.queryParams,
                page: 1,
                per_page: 20,
                sort: "created_at",
                order: "desc",
                wallet_id: walletId
            }
        }));

        await TransactionService.getTransactions();
    })

    const onColumnClick = async (name: "created_at" | "transaction_fee" | "transaction_status") => {
        const state = get(datagrid);

        if (state.queryParams.sort === name) {
            if (state.queryParams.order === "desc") {
                datagrid.update((dg) => ({
                    ...dg,
                    queryParams: {...dg.queryParams, sort: name, order: "asc"}
                }))
            } else if (state.queryParams.order === "asc") {
                datagrid.update((dg) => ({
                    ...dg,
                    queryParams: {...dg.queryParams, sort: name, order: "desc"}
                }))
            }
        } else {
            datagrid.update((dg) => ({
                ...dg,
                queryParams: {...dg.queryParams, sort: name, order: "desc"}
            }))
        }

        await TransactionService.getTransactions();
    }

    const onPaginatorClick = async (page: number) => {
        datagrid.update((dg) => ({
            ...dg,
            queryParams: {...dg.queryParams, page}
        }));

        await TransactionService.getTransactions();
    }

    export const baseColumns: Omit<ColumnHeaderProps, "order">[] = [
        {title: "Transaction Hash", sort: false},
        {title: "From address", sort: false},
        {title: "To address", sort: false},
        {title: "Amount", sort: false},
        {title: "Created At", sort: true, sortName: "created_at", onClick: onColumnClick},
        {title: "Fee", sort: true, sortName: "transaction_fee", onClick: onColumnClick},
        {title: "Status", sort: true, sortName: "transaction_status", onClick: onColumnClick},
    ];

    export const columns = derived(datagrid, (dg) => {
        const {sort, order} = dg.queryParams;

        return baseColumns.map((col) => {
            if (!col.sort || !col.sortName) {
                return {
                    ...col,
                    order: undefined
                };
            }

            return {
                ...col,
                order: col.sortName === sort ? order : undefined
            };
        });
    });
</script>
<div class="modal-body" id="container">
    <div id="grid">
        <table class="table">
            <thead>
            <tr>
                {#each $columns as column (column.title)}
                    <ColumnHeader
                            title={column.title}
                            sort={column.sort}
                            order={column.order}
                            sortName={column.sortName}
                            onClick={column.onClick}
                    >

                    </ColumnHeader>
                {/each}
            </tr>
            </thead>
            <tbody>
            {#each $datagrid.data.items as row (row.id)}
                <Row row={row}></Row>
            {/each}
            </tbody>
        </table>
    </div>
    <div id="paginator">
        <Paginator
                page={$datagrid.data.page}
                totalPages={$datagrid.data.total_pages}
                onClick={onPaginatorClick}
        ></Paginator>
    </div>
</div>