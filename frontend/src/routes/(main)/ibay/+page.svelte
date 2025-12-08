<style>
    .address {
        display: inline-block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        vertical-align: middle;
    }

    .information__container {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .information__row p:first-child {
        min-width: 88px;
    }
</style>
<script lang="ts">
    import {onMount} from "svelte";

    import {modals} from "svelte-modals";

    import CreateProductModal from "$lib/components/modals/CreateProductModal.svelte";

    import ProductService from "$lib/services/products.ts";

    import {products} from "$lib/stores/products.ts";

    onMount(async () => {
        await ProductService.getProducts();
    });
</script>
<!--Products Header-->
<div class="content-header row align-items-center">
    <div class="col-md-6 col-6 mb-2">
        <h2 class="mb-0">Products</h2>
    </div>
    <div class="col-md-6 col-6 mb-2 text-right">
        <button
                class="btn btn-primary"
                onclick={() => modals.open(CreateProductModal)}
        >
            Add product
        </button>
    </div>
</div>
<!--Products-->
<div class="row">
    {#each $products as product (product.id)}
        <div class="col-12 col-md-6 col-lg-4">
            <div class="card">
                <img
                        class="img-fluid card-img-top"
                        src={product.photo_url}
                        alt={product.name}
                >
                <div class="card-body information__container">
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="card-title mb-0">{product.name}</h4>
                        <h4 class="font-weight-bold mb-0">{product.price} {product.asset_symbol}</h4>
                    </div>
                    <div class="information__row d-flex align-items-center">
                        <p class="font-weight-bold mb-0 mr-1">Address:</p>
                        <a
                                href={`https://sepolia.etherscan.io/address/${product.wallet_address}`}
                                class="address font-weight-light"
                        >
                            {product.wallet_address}
                        </a>
                    </div>
                    <div>
                        <button class="btn btn-primary btn-block">Buy</button>
                    </div>
                </div>
            </div>
        </div>
    {/each}
</div>
<!--Orders Header-->
<div class="content-header row">
    <div class="content-header-left col-md-9 col-12 mb-2">
        <h2 class="float-left mb-0">Orders</h2>
    </div>
</div>
<!--Orders-->
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <div class="card">
            <img
                    class="img-fluid card-img-top"
                    src="/vuexy/images/pages/eCommerce/6.png"
                    alt="order"
            >
            <div class="card-body information__container">
                <!--Name And Price-->
                <div class="d-flex justify-content-between align-items-center">
                    <h4 class="card-title mb-0">Switch Controller</h4>
                    <h4 class="font-weight-bold mb-0">0.2 ETH</h4>
                </div>
                <!--Payment Transaction-->
                <div class="information__row d-flex align-items-center">
                    <p class="font-weight-bold mb-0 mr-1">Transaction:</p>
                    <a
                            href="https://sepolia.etherscan.io/tx/0xb7be407a0e6351e90c6788832d0a43844d347602fe844e2300697613714b1b47"
                            class="address font-weight-light"
                    >
                        0xb7be407a0e6351e90c6788832d0a43844d347602fe844e2300697613714b1b47
                    </a>
                </div>
                <!--Date-->
                <div class="information__row d-flex align-items-center">
                    <p class="font-weight-bold mb-0 mr-1">Order date:</p>
                    <p class="font-weight-lighter mb-0 mr-1">15:00 24/09/25</p>
                </div>
                <!--Status-->
                <div class="information__row d-flex align-items-center">
                    <p class="font-weight-bold mb-0 mr-1">Status:</p>
                    <p class="font-weight-lighter text-danger mb-0 mr-1">Returned</p>
                </div>
                <!--Return Transaction-->
                <div class="information__row d-flex align-items-center">
                    <p class="font-weight-bold mb-0 mr-1">Return:</p>
                    <a
                            href="https://sepolia.etherscan.io/tx/0xb7be407a0e6351e90c6788832d0a43844d347602fe844e2300697613714b1b47"
                            class="address font-weight-light"
                    >
                        0xb7be407a0e6351e90c6788832d0a43844d347602fe844e2300697613714b1b47
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>