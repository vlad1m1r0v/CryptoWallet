class TokenService {
    static getToken() {
        return localStorage.getItem("access_token");
    }

    static saveToken(token: string) {
        localStorage.setItem("access_token", token)
    }

    static clearToken() {
        localStorage.removeItem("access_token");
    }
}

export default TokenService;