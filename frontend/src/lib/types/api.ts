export interface RegisterRequest {
    username: string
    email: string
    password: string
    repeat_password: string
}

export interface LoginRequest {
    email: string
    password: string
    remember_me?: boolean
}

export interface JwtResponse {
    access_token: string
}

export interface UserResponsePermissions {
    has_chat_access: boolean;
}

export interface UserResponseWallet {
    id: string;
    address: string;
}

export interface UserResponse {
    id: string;
    username: string;
    email: string;
    avatar_url?: string | null;
    total_messages: number;
    permissions: UserResponsePermissions;
    wallets: UserResponseWallet[];
    total_wallets: number;
}

export interface WalletResponse {
    id: string;
    address: string;
    balance: string;
    asset_symbol: string;
}

export interface ImportWalletRequest {
    private_key: string;
}
