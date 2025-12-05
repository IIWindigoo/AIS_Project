// Authentication utilities
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.listeners = [];
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.currentUser));
    }

    async checkAuth() {
        try {
            this.currentUser = await api.getCurrentUser();
            console.log('Current user:', this.currentUser); // DEBUG
            this.notify();
            return true;
        } catch (error) {
            this.currentUser = null;
            this.notify();
            return false;
        }
    }

    async login(email, password) {
        try {
            const response = await api.login(email, password);
            await this.checkAuth();
            return { success: true, message: response.message };
        } catch (error) {
            return { success: false, message: error.message };
        }
    }

    async register(email, password, confirmPassword, name, surname) {
        try {
            const response = await api.register(email, password, confirmPassword, name, surname);
            return { success: true, message: response.message };
        } catch (error) {
            return { success: false, message: error.message };
        }
    }

    async logout() {
        try {
            await api.logout();
            this.currentUser = null;
            this.notify();
            return { success: true };
        } catch (error) {
            return { success: false, message: error.message };
        }
    }

    isAuthenticated() {
        return this.currentUser !== null;
    }

    getUser() {
        return this.currentUser;
    }

    hasRole(role) {
        const userRole = this.currentUser?.role?.name || this.currentUser?.role_name;
        return userRole === role;
    }

    isAdmin() {
        return this.hasRole('admin');
    }

    isTrainer() {
        return this.hasRole('trainer');
    }

    isClient() {
        return this.hasRole('client');
    }
}

const authManager = new AuthManager();
