import {io, Socket} from "socket.io-client";

import {toast} from "svelte-sonner";


import TokenService from "$lib/services/token.ts";

import {user} from "$lib/stores/user.ts";
import {wallets} from "$lib/stores/wallets.ts";

import TransactionToast from "$lib/components/toasts/TransactionToast.svelte";

import {
    type CompleteTransactionResponse,
    type UpdateWalletResponse,
    type WalletResponse
} from "$lib/types/api.ts";

export function createSocket(): Socket {
    return io("ws://localhost:9000", {
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
            wallets: [...u.wallets, {id: data.id, address: data.address}]
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

    socket.on("complete_transaction", (data: CompleteTransactionResponse) => {
        toast(TransactionToast,
            {
                componentProps: {
                    value: data.value,
                    transactionFee: data.transaction_fee,
                    transactionType: data.transaction_type!,
                    walletAddress: data.wallet_address!,
                    transactionHash: data.transaction_hash,
                    assetSymbol: data.asset_symbol
                }
            })
    })
}
