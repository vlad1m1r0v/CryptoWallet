export interface RegisterRequestData {
    username: string
    email: string
    password: string
    repeat_password: string
}

export interface LoginRequestData  {
    email: string
    password: string
    remember_me?: boolean
}