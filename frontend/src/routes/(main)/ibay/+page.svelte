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

    import {formatDate} from "$lib/utils/date.ts";

    import CreateProductModal from "$lib/components/modals/CreateProductModal.svelte";
    import CreateOrderModal from "$lib/components/modals/CreateOrderModal.svelte";

    import ProductService from "$lib/services/products.ts";
    import OrderService from "$lib/services/orders.ts";

    import {products} from "$lib/stores/products.ts";
    import {orders} from "$lib/stores/orders.ts";

    onMount(async () => {
        await ProductService.getProducts();
        await OrderService.getOrders();
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
                        <button
                                class="btn btn-primary btn-block"
                                onclick={() => modals.open(CreateOrderModal, {product})}
                        >
                            Buy
                        </button>
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
    {#each $orders as order (order.id)}
        <div class="col-12 col-md-6 col-lg-4">
            <div class="card">
                <img
                        class="img-fluid card-img-top"
                        src={order.product_photo_url}
                        alt={order.product_name}
                >
                <div class="card-body information__container">
                    <!--Name And Price-->
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="card-title mb-0">{order.product_name}</h4>
                        <h4 class="font-weight-bold mb-0">{order.product_price} {order.asset_symbol}</h4>
                    </div>
                    <!--Payment Transaction-->
                    <div class="information__row d-flex align-items-center">
                        <p class="font-weight-bold mb-0 mr-1">Transaction:</p>
                        {#if order.payment_transaction_hash}
                            <a
                                    href={`https://sepolia.etherscan.io/tx/${order.payment_transaction_hash}`}
                                    class="address font-weight-light"
                            >
                                {order.payment_transaction_hash}
                            </a>
                        {/if}
                    </div>
                    <!--Date-->
                    <div class="information__row d-flex align-items-center">
                        <p class="font-weight-bold mb-0 mr-1">Order date:</p>
                        <p class="font-weight-lighter mb-0 mr-1">{formatDate(order.created_at)}</p>
                    </div>
                    <!--Status-->
                    <div class="information__row d-flex align-items-center">
                        <p class="font-weight-bold mb-0 mr-1">Status:</p>
                        <p
                                class="font-weight-lighter mb-0 mr-1"
                                class:text-danger={order.status === "failed"}
                                class:text-success={order.status === "completed"}
                                class:text-warning={order.status === "returned"}
                                class:text-info={order.status === "delivering"}
                                class:text-primary={order.status === "new"}
                        >{order.status.toUpperCase()}</p>
                    </div>
                    <!--Return Transaction-->
                    <div class="information__row d-flex align-items-center">
                        <p class="font-weight-bold mb-0 mr-1">Return:</p>
                        {#if order.return_transaction_hash}
                            <a
                                    href={`https://sepolia.etherscan.io/tx/${order.return_transaction_hash}`}
                                    class="address font-weight-light"
                            >
                                {order.return_transaction_hash}
                            </a>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    {/each}
</div>