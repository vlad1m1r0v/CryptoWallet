<script lang="ts">
    import {type ColumnHeaderProps} from "$lib/components/datagrid/types.ts";

    import ChevronUp from "$lib/components/icons/ChevronUp.svelte";
    import ChevronDown from "$lib/components/icons/ChevronDown.svelte";

    const {
        sort,
        title,
        sortName,
        order,
        onClick
    }: ColumnHeaderProps = $props();
</script>
<th scope="col" onclick={() => {
        if (sortName && onClick) onClick(sortName);
    }}>
    <div class="d-flex align-items-center justify-content-between">
        <span>{title}</span>
        {#if sort}
            {#if order === "asc"}
                <ChevronUp></ChevronUp>
            {/if}
            {#if order === "desc"}
                <ChevronDown></ChevronDown>
            {/if}
        {/if}
    </div>
</th>
