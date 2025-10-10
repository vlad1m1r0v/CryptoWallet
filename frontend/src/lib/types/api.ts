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

export interface UpdateProfileRequest {
    username: string
    password?: string | null
    repeat_password?: string | null
}

export interface AccessTokenResponse {
    access_token: string
}

export interface ProfileResponse {
    username: string
    email: string
    avatar_url: string | null
}