import HttpService from "$lib/services/http.ts";
import type {WalletResponse} from "$lib/types/api.ts";
import {wallets} from "$lib/stores/wallets.ts";

export default class WalletService {
    static async createWallet(): Promise<void> {
        await HttpService.request<null>('/wallets', {method: 'POST'}, true);
    }

    static async getWallets(): Promise<void> {
        const response = await HttpService.request<WalletResponse[]>(
            '/wallets',
            {method: 'GET'},
            true
        );

        if (response) wallets.set(response);
    }

}