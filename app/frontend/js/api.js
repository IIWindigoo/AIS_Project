// API client for backend communication
// Use the same origin as the current page to avoid CORS issues
const API_BASE_URL = window.location.origin;

class ApiClient {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            credentials: 'include', // Include cookies for authentication
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
                console.error('API Error:', error);

                // Handle validation errors (422)
                if (response.status === 422 && error.detail) {
                    if (Array.isArray(error.detail)) {
                        const messages = error.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join('; ');
                        throw new Error(messages);
                    }
                }

                throw new Error(error.detail || `HTTP error! status: ${response.status}`);
            }

            // Handle 204 No Content
            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Auth endpoints
    async register(email, password, confirmPassword, name, surname, phoneNumber) {
        return this.request('/users/register/', {
            method: 'POST',
            body: JSON.stringify({
                email,
                password,
                confirm_password: confirmPassword,
                first_name: name,
                last_name: surname,
                phone_number: phoneNumber
            }),
        });
    }

    async login(email, password) {
        return this.request('/users/login/', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
    }

    async logout() {
        return this.request('/users/logout', {
            method: 'POST',
        });
    }

    async getCurrentUser() {
        return this.request('/users/me/');
    }

    async refreshToken() {
        return this.request('/users/refresh', {
            method: 'POST',
        });
    }

    // Trainings endpoints
    async getAllTrainings() {
        return this.request('/trainings/');
    }

    async createTraining(data) {
        return this.request('/trainings/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateTraining(trainingId, data) {
        return this.request(`/trainings/${trainingId}/`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async deleteTraining(trainingId) {
        return this.request(`/trainings/${trainingId}/`, {
            method: 'DELETE',
        });
    }

    async getMyTrainings() {
        return this.request('/trainings/my/');
    }

    // Bookings endpoints
    async createBooking(trainingId) {
        return this.request('/bookings/', {
            method: 'POST',
            body: JSON.stringify({ training_id: trainingId }),
        });
    }

    async getUserBookings() {
        return this.request('/bookings/');
    }

    async cancelBooking(trainingId) {
        return this.request('/bookings/', {
            method: 'DELETE',
            body: JSON.stringify({ training_id: trainingId }),
        });
    }

    // Rooms endpoints
    async getAllRooms() {
        return this.request('/rooms/');
    }

    // Subscriptions endpoints
    async getAllSubscriptions() {
        return this.request('/subscriptions/');
    }

    async createSubscription(data) {
        return this.request('/subscriptions/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateSubscription(subId, data) {
        return this.request(`/subscriptions/${subId}/`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async deleteSubscription(subId) {
        return this.request(`/subscriptions/${subId}/`, {
            method: 'DELETE',
        });
    }

    // Memberships endpoints
    async createSubscriptionRequest(subscriptionId) {
        return this.request('/memberships/request/', {
            method: 'POST',
            body: JSON.stringify({ subscription_id: subscriptionId }),
        });
    }

    async getMyMembership() {
        return this.request('/memberships/my/');
    }

    async getAllRequests() {
        return this.request('/memberships/request/');
    }

    async updateRequestStatus(requestId, status) {
        return this.request(`/memberships/request/${requestId}/`, {
            method: 'PATCH',
            body: JSON.stringify({ status }),
        });
    }

    async getAllMemberships() {
        return this.request('/memberships/all/');
    }

    // Admin endpoints
    async getAllUsers() {
        return this.request('/users/all_users/');
    }

    // Rooms endpoints
    async getRooms() {
        return this.request('/rooms/');
    }

    async createRoom(data) {
        return this.request('/rooms/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateRoom(roomId, data) {
        return this.request(`/rooms/${roomId}/`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async deleteRoom(roomId) {
        return this.request(`/rooms/${roomId}/`, {
            method: 'DELETE',
        });
    }
}

const api = new ApiClient();
