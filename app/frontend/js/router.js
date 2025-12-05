// Simple client-side router
class Router {
    constructor() {
        this.routes = {};
        this.currentRoute = null;
        this.beforeEachHooks = [];

        window.addEventListener('popstate', () => this.handleRoute());

        // Intercept all link clicks
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-link]')) {
                e.preventDefault();
                this.navigate(e.target.getAttribute('href'));
            }
        });
    }

    addRoute(path, handler) {
        this.routes[path] = handler;
    }

    beforeEach(hook) {
        this.beforeEachHooks.push(hook);
    }

    async navigate(path) {
        // Run beforeEach hooks
        for (const hook of this.beforeEachHooks) {
            const result = await hook(path, this.currentRoute);
            if (result === false) return; // Navigation cancelled
            if (typeof result === 'string') {
                path = result; // Redirect to different path
            }
        }

        window.history.pushState({}, '', path);
        await this.handleRoute();
    }

    async handleRoute() {
        const path = window.location.pathname;
        this.currentRoute = path;

        const handler = this.routes[path] || this.routes['/404'];

        if (handler) {
            try {
                await handler();
            } catch (error) {
                console.error('Route handler error:', error);
                this.showError(error.message);
            }
        }
    }

    showError(message) {
        const app = document.getElementById('app');
        if (app) {
            app.innerHTML = `
                <div class="error-page">
                    <h1>Error</h1>
                    <p>${message}</p>
                    <button onclick="router.navigate('/')">Go Home</button>
                </div>
            `;
        }
    }

    start() {
        this.handleRoute();
    }
}

const router = new Router();
