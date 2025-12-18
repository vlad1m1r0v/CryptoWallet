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
    wallet_id: string;
    wallet_address: string;
    transaction_hash: string;
    from_address: string;
    to_address: string;
    value: number;
    transaction_fee: number;
    transaction_status: TransactionStatusEnum;
    asset_symbol: string;
    created_at?: string;
    transaction_type?: TransactionTypeEnum;
}

export interface PaginatedResponse<T> {
    items: T[];
    page: number;
    per_page: number;
    total_pages: number;
    total_records: number;
}

export interface ProductResponse {
    id: string;
    name: string;
    price: number;
    photo_url: string;
    created_at: string;
    asset_symbol: string;
    wallet_address: string;
}

export enum OrderStatusEnum {
    NEW = "new",
    FAILED = "failed",
    DELIVERING = "delivering",
    RETURNED = "returned",
    COMPLETED = "completed"
}

export interface OrderResponse {
    id: string;
    product_name: string;
    product_price: number;
    product_photo_url: string;
    asset_symbol: string;
    payment_transaction_hash?: string;
    return_transaction_hash?: string;
    status: OrderStatusEnum;
    created_at: string;
}

export interface CreateOrderRequest {
    wallet_id: string;
    product_id: string;
}

export interface PayOrderResponse {
    id: string;
    transaction_hash: string;
}

export interface UpdateOrderResponse {
    id: string;
    status?: OrderStatusEnum;
    payment_transaction_hash?: string;
    return_transaction_hash?: string;
}