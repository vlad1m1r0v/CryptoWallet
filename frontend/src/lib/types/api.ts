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
    balance: number;
    asset_symbol: string;
}

export interface ImportWalletRequest {
    private_key: string;
}

export interface CreateTransactionRequest {
    from_address: string;
    to_address: string;
    amount: number;
}

export interface FreeETHRequest {
    wallet_id: string;
}

export interface UpdateWalletResponse {
    id: string;
    balance: number;
}

export enum TransactionStatusEnum {
    SUCCESSFUL = "successful",
    PENDING = "pending",
    FAILED = "failed",
}

export enum TransactionTypeEnum {
    INCOME = "income",
    EXPENSE = "expense"
}

export interface TransactionResponse {
    id: string;
    transaction_hash: string;
    from_address: string;
    to_address: string;
    value: number;
    transaction_fee: number;
    transaction_status: TransactionStatusEnum;
    asset_symbol: string;
    created_at?: string;
    transaction_type?: TransactionTypeEnum;
    wallet_address?: string;
}

export interface PaginatedResponse<T> {
    items: T[];
    page: number;
    per_page: number;
    total_pages: number;
    total_records: number;
}