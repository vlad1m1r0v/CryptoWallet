class TokenService {
    static getToken() {
        return localStorage.getItem("access_token") ??
            sessionStorage.getItem("access_token");
    }

    static saveToken(token: string, remember: boolean) {
        if (remember) {
            localStorage.setItem("access_token", token)
        } else {
            sessionStorage.setItem("access_token", token)
        }
    }

    static clearToken() {
        localStorage.removeItem("access_token");
        sessionStorage.removeItem("access_token");
    }
}

export default TokenService;