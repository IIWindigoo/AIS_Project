// Reusable components
const components = {
    navbar(user) {
        // Safe access to user role - handle both formats
        const userRole = user?.role?.name || user?.role_name;

        return `
            <nav class="navbar">
                <div class="navbar-container">
                    <a href="/" class="navbar-brand" data-link>
                        <span class="brand-icon">💪</span>
                        <span class="brand-text">СпортКлуб</span>
                    </a>

                    <div class="navbar-menu">
                        ${user ? `
                            <a href="/trainings" class="navbar-link" data-link>Тренировки</a>
                            <a href="/subscriptions" class="navbar-link" data-link>Абонементы</a>
                            ${userRole === 'client' ? `
                                <a href="/my-bookings" class="navbar-link" data-link>Мои записи</a>
                            ` : ''}
                            ${userRole === 'trainer' ? `
                                <a href="/my-trainings" class="navbar-link" data-link>Мои тренировки</a>
                            ` : ''}
                            ${userRole === 'admin' ? `
                                <a href="/admin" class="navbar-link" data-link>Админ панель</a>
                            ` : ''}
                            <div class="navbar-user">
                                <a href="/profile" class="user-profile-link" data-link>
                                    <span class="user-name">${user.first_name || user.name || ''} ${user.last_name || user.surname || ''}</span>
                                    <span class="user-role">(${this.getRoleText(userRole)})</span>
                                </a>
                            </div>
                            <button class="btn btn-secondary" onclick="handleLogout()">Выйти</button>
                        ` : `
                            <a href="/login" class="navbar-link" data-link>Войти</a>
                            <a href="/register" class="btn btn-primary" data-link>Регистрация</a>
                        `}
                    </div>
                </div>
            </nav>
        `;
    },

    getRoleText(role) {
        const roles = {
            'client': 'Клиент',
            'trainer': 'Тренер',
            'admin': 'Администратор'
        };
        return roles[role] || role;
    },

    layout(content, user = null) {
        return `
            ${this.navbar(user)}
            <main class="main-content">
                ${content}
            </main>
            <footer class="footer">
                <div class="container">
                    <p>&copy; 2025 СпортКлуб. Все права защищены.</p>
                </div>
            </footer>
        `;
    },

    trainingCard(training, actions = []) {
        const bookingCount = training.booking_count || 0;
        const capacity = training.room?.capacity || 0;
        const isFull = bookingCount >= capacity;

        return `
            <div class="training-card" data-training-id="${training.id}">
                <div class="training-header">
                    <h3 class="training-title">${training.title}</h3>
                    <span class="training-time">${training.start_time?.slice(0, 5)} - ${training.end_time?.slice(0, 5)}</span>
                </div>
                <div class="training-body">
                    <div class="training-info">
                        <div class="info-item">
                            <span class="info-label">📅 Дата:</span>
                            <span class="info-value">${utils.formatDate(training.date)}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">⏰ Время:</span>
                            <span class="info-value">${training.start_time?.slice(0, 5)} - ${training.end_time?.slice(0, 5)}</span>
                        </div>
                        ${training.trainer ? `
                            <div class="info-item">
                                <span class="info-label">👤 Тренер:</span>
                                <span class="info-value">${training.trainer.first_name || training.trainer.name} ${training.trainer.last_name || training.trainer.surname}</span>
                            </div>
                        ` : ''}
                        ${training.room ? `
                            <div class="info-item">
                                <span class="info-label">🏠 Помещение:</span>
                                <span class="info-value">${training.room.title}</span>
                            </div>
                        ` : ''}
                        ${capacity > 0 ? `
                            <div class="info-item">
                                <span class="info-label">👥 Записалось:</span>
                                <span class="info-value ${isFull ? 'text-danger' : ''}">${bookingCount} / ${capacity} ${isFull ? '(мест нет)' : ''}</span>
                            </div>
                        ` : ''}
                        ${training.description ? `
                            <div class="info-item">
                                <span class="info-label">📝 Описание:</span>
                                <span class="info-value">${training.description}</span>
                            </div>
                        ` : ''}
                    </div>
                </div>
                ${actions.length > 0 ? `
                    <div class="training-actions">
                        ${actions.map(action => `
                            <button class="btn btn-${action.type}"
                                    onclick="${action.onclick}"
                                    ${action.disabled || (action.checkFull && isFull) ? 'disabled' : ''}>
                                ${action.text}
                            </button>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    },

    bookingCard(booking, showCancel = true) {
        return `
            <div class="booking-card" data-booking-id="${booking.id}">
                <div class="booking-header">
                    <h3>${booking.training.title}</h3>
                </div>
                <div class="booking-body">
                    <div class="booking-info">
                        <div class="info-item">
                            <span class="info-label">📅 Дата:</span>
                            <span class="info-value">${utils.formatDate(booking.training.date)}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">⏰ Время:</span>
                            <span class="info-value">${booking.training.start_time?.slice(0, 5)} - ${booking.training.end_time?.slice(0, 5)}</span>
                        </div>
                        ${booking.training.room ? `
                            <div class="info-item">
                                <span class="info-label">🏠 Помещение:</span>
                                <span class="info-value">${booking.training.room.title}</span>
                            </div>
                        ` : ''}
                    </div>
                </div>
                ${showCancel ? `
                    <div class="booking-actions">
                        <button class="btn btn-danger"
                                onclick="handleCancelBooking(${booking.training.id})">
                            Отменить запись
                        </button>
                    </div>
                ` : ''}
            </div>
        `;
    },

    formInput(type, name, label, required = true, placeholder = '') {
        return `
            <div class="form-group">
                <label for="${name}" class="form-label">
                    ${label}${required ? ' *' : ''}
                </label>
                <input
                    type="${type}"
                    id="${name}"
                    name="${name}"
                    class="form-input"
                    ${required ? 'required' : ''}
                    placeholder="${placeholder}">
            </div>
        `;
    },

    emptyState(icon, title, message) {
        return `
            <div class="empty-state">
                <div class="empty-icon">${icon}</div>
                <h2 class="empty-title">${title}</h2>
                <p class="empty-message">${message}</p>
            </div>
        `;
    },

    subscriptionCard(subscription, actions = []) {
        return `
            <div class="subscription-card" data-subscription-id="${subscription.id}">
                <div class="subscription-header">
                    <h3 class="subscription-title">${subscription.title}</h3>
                    <div class="subscription-price">${subscription.price} ₽</div>
                </div>
                <div class="subscription-body">
                    <div class="subscription-info">
                        <div class="info-item">
                            <span class="info-label">⏳ Длительность:</span>
                            <span class="info-value">${subscription.duration_days} дней</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">💰 Цена:</span>
                            <span class="info-value">${subscription.price} рублей</span>
                        </div>
                    </div>
                </div>
                ${actions.length > 0 ? `
                    <div class="subscription-actions">
                        ${actions.map(action => `
                            <button class="btn btn-${action.type}"
                                    onclick="${action.onclick}"
                                    ${action.disabled ? 'disabled' : ''}>
                                ${action.text}
                            </button>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    },

    loader() {
        return `
            <div class="loader">
                <div class="spinner"></div>
                <p>Загрузка...</p>
            </div>
        `;
    },

    pagination(currentPage, totalPages, onPageChange) {
        if (totalPages <= 1) return '';

        const pages = [];
        const maxVisible = 5;
        let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
        let endPage = Math.min(totalPages, startPage + maxVisible - 1);

        if (endPage - startPage < maxVisible - 1) {
            startPage = Math.max(1, endPage - maxVisible + 1);
        }

        return `
            <div class="pagination">
                <button class="pagination-btn"
                        onclick="${onPageChange}(${currentPage - 1})"
                        ${currentPage === 1 ? 'disabled' : ''}>
                    ← Назад
                </button>

                ${startPage > 1 ? `
                    <button class="pagination-btn" onclick="${onPageChange}(1)">1</button>
                    ${startPage > 2 ? '<span class="pagination-dots">...</span>' : ''}
                ` : ''}

                ${Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i).map(page => `
                    <button class="pagination-btn ${page === currentPage ? 'active' : ''}"
                            onclick="${onPageChange}(${page})">
                        ${page}
                    </button>
                `).join('')}

                ${endPage < totalPages ? `
                    ${endPage < totalPages - 1 ? '<span class="pagination-dots">...</span>' : ''}
                    <button class="pagination-btn" onclick="${onPageChange}(${totalPages})">${totalPages}</button>
                ` : ''}

                <button class="pagination-btn"
                        onclick="${onPageChange}(${currentPage + 1})"
                        ${currentPage === totalPages ? 'disabled' : ''}>
                    Вперед →
                </button>
            </div>
        `;
    }
};
