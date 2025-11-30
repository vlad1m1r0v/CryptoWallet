import HttpService from "$lib/services/http.ts";

import {wallets} from "$lib/stores/wallets.ts";

import type {
    ImportWalletRequest,
    FreeETHRequest,
    WalletResponse
} from "$lib/types/api.ts";
import {toast} from "svelte-sonner";

export default class WalletService {
    static async createWallet(): Promise<void> {
        await HttpService.request<null>('/wallets', {method: 'POST'}, true);
    }

    static async importWallet(data: ImportWalletRequest): Promise<void> {
        await HttpService.request<null>(
            '/wallets/import',
            {method: 'POST', body: JSON.stringify(data)},
            true
        );
    }

    static async getWallets(): Promise<void> {
        const response = await HttpService.request<WalletResponse[]>(
            '/wallets',
            {method: 'GET'},
            true
        );

        if (response) wallets.set(response);
    }

    static async requestFreeETH(data: FreeETHRequest): Promise<void> {
        await HttpService.request<null>(
            '/wallets/request-free-eth',
            {method: 'POST', body: JSON.stringify(data)},
            true
        );

        toast.info("You have successfully send request for retrieving free ETH.")
    }
}