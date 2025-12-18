import {PUBLIC_SOCKET_URL} from '$env/static/public';

import {get} from "svelte/store";

import {io, Socket} from "socket.io-client";

import {toast} from "svelte-sonner";
import {modals} from "svelte-modals";

import TokenService from "$lib/services/token.ts";
import TransactionService from "$lib/services/transactions.ts";

import {user} from "$lib/stores/user.ts";
import {wallets} from "$lib/stores/wallets.ts";
import {products} from "$lib/stores/products.ts";
import {orders} from "$lib/stores/orders.ts";

import TransactionToast from "$lib/components/toasts/TransactionToast.svelte";
import PaymentSucceedModal from "$lib/components/modals/PaymentSucceedModal.svelte";

import {
    type TransactionResponse,
    type UpdateWalletResponse,
    type WalletResponse,
    type ProductResponse,
    type PayOrderResponse,
    type UpdateOrderResponse,
} from "$lib/types/api.ts";
import {datagrid} from "$lib/stores/datagrid.ts";

export function createSocket(): Socket {
    return io(PUBLIC_SOCKET_URL, {
        transports: ["websocket"],
        auth: {token: TokenService.getToken()},
        autoConnect: false
    });
}

export function bindSocketHandlers(socket: Socket) {
    socket.on("connect", () => {
        console.log("🔌 Socket connected", socket.id);
    });

    socket.on("disconnect", (reason) => {
        console.log("❌ Socket disconnected:", reason);
    });

    socket.on("error", (error) => {
        console.error("⚠️ Socket error:", error);
    });

    socket.on("save_wallet", (data: WalletResponse) => {
        toast.success("Wallet successfully added.");

        user.update(u => u ? {
            ...u,
            total_wallets: u.total_wallets + 1,
            wallets: [{id: data.id, address: data.address}, ...u.wallets]
        } : u);

        wallets.update(w => w ? [...w, data] : w);
    });

    socket.on("update_wallet", (data: UpdateWalletResponse) => {
        wallets.update(w => w ? (
            w.map(wallet => wallet.id === data.id ? {
                ...wallet,
                balance: data.balance
            } : wallet)
        ) : w)
    });

    socket.on("complete_transaction", (data: TransactionResponse) => {
        toast(TransactionToast,
            {
                componentProps: {
                    value: data.value,
                    transactionFee: data.transaction_fee,
                    transactionType: data.transaction_type!,
                    address: data.wallet_address!,
                    transactionHash: data.transaction_hash,
                    assetSymbol: data.asset_symbol
                }
            })
    });

    const onTransaction = async (data: TransactionResponse) => {
        const store = get(datagrid);

        if (store.queryParams.wallet_id === data.wallet_id) {
            datagrid.update((dg) => (
                    {
                        ...dg,
                        queryParams: {...dg.queryParams, page: 1, per_page: 20, sort: "created_at", order: "desc"}
                    }
                )
            )

            await TransactionService.getTransactions();
        }
    };

    socket.on("complete_transaction", async (data: TransactionResponse) => await onTransaction(data));
    socket.on("save_pending_transaction", async (data: TransactionResponse) => await onTransaction(data));

    socket.on("request_free_eth", () => {
        toast.success("You have successfully send request for receiving free ETH.")
    })

    socket.on("save_product", (product: ProductResponse) => {
        products.update((list) => [product, ...(list ?? [])]);
    })

    socket.on("pay_order", async (data: PayOrderResponse) => {
        await modals.open(PaymentSucceedModal, {transactionHash: data.transaction_hash})
    })

    socket.on("update_order", async (data: UpdateOrderResponse) => {
        console.log(`Received update order event: ${data}`);

        orders.update(o => o ? (
            o.map(o => o.id === data.id ? {
                ...o,
                ...data
            } : o)
        ) : o)
    })

    socket.on("give_chat_access", async () => {
        toast.success("You are given chat access.");
        user.update(u => u ? {...u, permissions: {...u.permissions, has_chat_access: true}} : u);
    })
}
