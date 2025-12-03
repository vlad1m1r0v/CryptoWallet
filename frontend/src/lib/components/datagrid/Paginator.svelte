<script lang="ts">
    interface Props {
        page: number;
        totalPages: number;
        onClick: (page: number) => void;
    }

    const {
        page, totalPages, onClick
    }: Props = $props();

    // Обчислюємо список сторінок — реактивно через runes
    const pages = $derived.by(() => {
        const arr: number[] = [];
        for (let p = page - 2; p <= page + 2; p++) {
            if (p >= 1 && p <= totalPages) {
                arr.push(p);
            }
        }
        return arr;
    });
</script>

<ul class="pagination mt-2">
    <!-- Prev -->
    <li class="page-item" class:disabled={page === 1}>
        <a class="page-link" href="javascript:void(0);" on:click={() => onClick(page - 1)}>
            &lt;
        </a>
    </li>

    <!-- Page numbers -->
    {#each pages as p}
        <li class="page-item" class:active={page === p}>
            <a class="page-link" href="javascript:void(0);" on:click={() => onClick(p)}>
                {p}
            </a>
        </li>
    {/each}

    <!-- Next -->
    <li class="page-item" class:disabled={page === totalPages}>
        <a class="page-link" href="javascript:void(0);" on:click={() => onClick(page + 1)}>
            &gt;
        </a>
    </li>
</ul>