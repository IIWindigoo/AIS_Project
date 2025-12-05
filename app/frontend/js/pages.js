// Page components
const pages = {
    home() {
        const user = authManager.getUser();
        const content = `
            <div class="home-page">
                <!-- Hero Section -->
                <section class="hero-section">
                    <div class="hero-overlay"></div>
                    <div class="hero-content">
                        <h1 class="hero-main-title">СПОРТКЛУБ</h1>
                        <p class="hero-tagline">Твой путь к совершенству начинается здесь</p>
                        <div class="hero-stats">
                            <div class="stat-item">
                                <div class="stat-number">5+</div>
                                <div class="stat-label">Лет опыта</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">1000+</div>
                                <div class="stat-label">Довольных клиентов</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">50+</div>
                                <div class="stat-label">Видов тренировок</div>
                            </div>
                        </div>
                        ${!user ? `
                            <div class="hero-cta">
                                <a href="/register" class="btn-hero btn-hero-primary" data-link>
                                    Начать тренировки
                                </a>
                                <a href="/trainings" class="btn-hero btn-hero-secondary" data-link>
                                    Расписание
                                </a>
                            </div>
                        ` : `
                            <div class="hero-cta">
                                <a href="/trainings" class="btn-hero btn-hero-primary" data-link>
                                    Перейти к тренировкам
                                </a>
                            </div>
                        `}
                    </div>
                </section>

                <!-- About Section -->
                <section class="about-section">
                    <div class="container">
                        <div class="section-header">
                            <h2 class="section-title">О нас</h2>
                            <div class="section-divider"></div>
                        </div>
                        <div class="about-content">
                            <p class="about-text">
                                <strong>СпортКлуб</strong> - это современный фитнес-центр, где каждый найдет идеальную программу тренировок.
                                Мы предлагаем профессиональный подход, новейшее оборудование и команду опытных тренеров,
                                готовых помочь вам достичь ваших целей.
                            </p>
                        </div>
                    </div>
                </section>

                <!-- Services Section -->
                <section class="services-section">
                    <div class="container">
                        <div class="section-header">
                            <h2 class="section-title">Наши услуги</h2>
                            <div class="section-divider"></div>
                        </div>
                        <div class="services-grid">
                            <div class="service-card">
                                <div class="service-icon">💪</div>
                                <h3 class="service-title">Тренажерный зал</h3>
                                <p class="service-description">
                                    Современное оборудование для силовых и кардио тренировок
                                </p>
                            </div>
                            <div class="service-card">
                                <div class="service-icon">🧘</div>
                                <h3 class="service-title">Групповые занятия</h3>
                                <p class="service-description">
                                    Йога, пилатес, зумба и другие направления
                                </p>
                            </div>
                            <div class="service-card">
                                <div class="service-icon">🥊</div>
                                <h3 class="service-title">Единоборства</h3>
                                <p class="service-description">
                                    Бокс, кикбоксинг, MMA с профессиональными тренерами
                                </p>
                            </div>
                            <div class="service-card">
                                <div class="service-icon">🏊</div>
                                <h3 class="service-title">Бассейн</h3>
                                <p class="service-description">
                                    Плавание для всех уровней подготовки
                                </p>
                            </div>
                            <div class="service-card">
                                <div class="service-icon">👤</div>
                                <h3 class="service-title">Персональные тренировки</h3>
                                <p class="service-description">
                                    Индивидуальный подход и программа под ваши цели
                                </p>
                            </div>
                            <div class="service-card">
                                <div class="service-icon">🍎</div>
                                <h3 class="service-title">Консультация диетолога</h3>
                                <p class="service-description">
                                    Разработка индивидуального плана питания
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Why Choose Us Section -->
                <section class="advantages-section">
                    <div class="container">
                        <div class="section-header">
                            <h2 class="section-title">Почему выбирают нас</h2>
                            <div class="section-divider"></div>
                        </div>
                        <div class="advantages-grid">
                            <div class="advantage-item">
                                <div class="advantage-number">01</div>
                                <h4 class="advantage-title">Профессиональные тренеры</h4>
                                <p class="advantage-text">Сертифицированные специалисты с большим опытом</p>
                            </div>
                            <div class="advantage-item">
                                <div class="advantage-number">02</div>
                                <h4 class="advantage-title">Современное оборудование</h4>
                                <p class="advantage-text">Новейшие тренажеры от ведущих производителей</p>
                            </div>
                            <div class="advantage-item">
                                <div class="advantage-number">03</div>
                                <h4 class="advantage-title">Удобное расписание</h4>
                                <p class="advantage-text">Работаем с 6:00 до 23:00 без выходных</p>
                            </div>
                            <div class="advantage-item">
                                <div class="advantage-number">04</div>
                                <h4 class="advantage-title">Доступные цены</h4>
                                <p class="advantage-text">Гибкая система абонементов и акции</p>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- CTA Section -->
                ${!user ? `
                    <section class="cta-section">
                        <div class="container">
                            <div class="cta-content">
                                <h2 class="cta-title">Готовы начать?</h2>
                                <p class="cta-text">Присоединяйтесь к нам и начните свой путь к здоровью и красоте уже сегодня!</p>
                                <a href="/register" class="btn-cta" data-link>Записаться на тренировку</a>
                            </div>
                        </div>
                    </section>
                ` : ''}
            </div>
        `;

        document.getElementById('app').innerHTML = components.layout(content, user);
    },

    login() {
        const content = `
            <div class="container container-sm">
                <div class="auth-card">
                    <h1 class="auth-title">Вход в систему</h1>
                    <form id="loginForm" class="auth-form">
                        ${components.formInput('email', 'email', 'Email', true, 'example@email.com')}
                        ${components.formInput('password', 'password', 'Пароль', true, '••••••••')}

                        <button type="submit" class="btn btn-primary btn-block">
                            Войти
                        </button>
                    </form>
                    <p class="auth-footer">
                        Нет аккаунта? <a href="/register" data-link>Зарегистрироваться</a>
                    </p>
                </div>
            </div>
        `;

        document.getElementById('app').innerHTML = components.layout(content);

        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            utils.clearFormError(e.target);

            const formData = new FormData(e.target);
            const email = formData.get('email');
            const password = formData.get('password');

            const result = await authManager.login(email, password);

            if (result.success) {
                utils.showNotification('Вход выполнен успешно!', 'success');
                router.navigate('/trainings');
            } else {
                utils.handleFormError(e.target, result.message);
            }
        });
    },

    register() {
        const content = `
            <div class="container container-sm">
                <div class="auth-card">
                    <h1 class="auth-title">Регистрация</h1>
                    <form id="registerForm" class="auth-form">
                        ${components.formInput('text', 'name', 'Имя', true, 'Иван')}
                        ${components.formInput('text', 'surname', 'Фамилия', true, 'Иванов')}
                        ${components.formInput('email', 'email', 'Email', true, 'example@email.com')}
                        ${components.formInput('password', 'password', 'Пароль', true, '••••••••')}
                        ${components.formInput('password', 'confirm_password', 'Подтвердите пароль', true, '••••••••')}

                        <button type="submit" class="btn btn-primary btn-block">
                            Зарегистрироваться
                        </button>
                    </form>
                    <p class="auth-footer">
                        Уже есть аккаунт? <a href="/login" data-link>Войти</a>
                    </p>
                </div>
            </div>
        `;

        document.getElementById('app').innerHTML = components.layout(content);

        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            utils.clearFormError(e.target);

            const formData = new FormData(e.target);
            const email = formData.get('email');
            const password = formData.get('password');
            const confirmPassword = formData.get('confirm_password');
            const name = formData.get('name');
            const surname = formData.get('surname');

            if (password !== confirmPassword) {
                utils.handleFormError(e.target, 'Пароли не совпадают');
                return;
            }

            const result = await authManager.register(email, password, confirmPassword, name, surname);

            if (result.success) {
                utils.showNotification('Регистрация успешна! Войдите в систему.', 'success');
                router.navigate('/login');
            } else {
                utils.handleFormError(e.target, result.message);
            }
        });
    },

    async trainings() {
        const user = authManager.getUser();
        const userRole = user?.role?.name || user?.role_name;

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${components.loader()}</div>`,
            user
        );

        try {
            const trainings = await api.getAllTrainings();
            const userBookings = user && userRole === 'client'
                ? await api.getUserBookings()
                : [];

            const bookedTrainingIds = new Set(userBookings.map(b => b.training.id));

            const content = `
                <div class="container">
                    <div class="page-header">
                        <h1>Доступные тренировки</h1>
                        ${user && (userRole === 'trainer' || userRole === 'admin') ? `
                            <button class="btn btn-primary" onclick="showCreateTrainingModal()">
                                Создать тренировку
                            </button>
                        ` : ''}
                    </div>

                    ${trainings.length === 0 ?
                        components.emptyState('📅', 'Нет тренировок', 'Пока не добавлено ни одной тренировки')
                    : `
                        <div class="trainings-grid">
                            ${trainings.map(training => {
                                const isBooked = bookedTrainingIds.has(training.id);
                                const actions = [];

                                if (user && userRole === 'client') {
                                    actions.push({
                                        type: isBooked ? 'secondary' : 'primary',
                                        text: isBooked ? '✓ Вы записаны' : 'Записаться',
                                        onclick: `handleBookTraining(${training.id})`,
                                        disabled: isBooked
                                    });
                                }

                                if (user && (userRole === 'trainer' || userRole === 'admin')) {
                                    actions.push({
                                        type: 'secondary',
                                        text: 'Редактировать',
                                        onclick: `showEditTrainingModal(${training.id})`
                                    });
                                    actions.push({
                                        type: 'danger',
                                        text: 'Удалить',
                                        onclick: `handleDeleteTraining(${training.id})`
                                    });
                                }

                                return components.trainingCard(training, actions);
                            }).join('')}
                        </div>
                    `}
                </div>
            `;

            document.getElementById('app').innerHTML = components.layout(content, user);
        } catch (error) {
            utils.showNotification('Ошибка загрузки тренировок: ' + error.message, 'error');
        }
    },

    async myBookings() {
        const user = authManager.getUser();
        const userRole = user?.role?.name || user?.role_name;

        if (!user || userRole !== 'client') {
            router.navigate('/');
            return;
        }

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${components.loader()}</div>`,
            user
        );

        try {
            const bookings = await api.getUserBookings();

            const content = `
                <div class="container">
                    <div class="page-header">
                        <h1>Мои записи</h1>
                    </div>

                    ${bookings.length === 0 ?
                        components.emptyState('📅', 'Нет записей', 'Вы еще не записались ни на одну тренировку')
                    : `
                        <div class="bookings-grid">
                            ${bookings.map(booking => components.bookingCard(booking)).join('')}
                        </div>
                    `}
                </div>
            `;

            document.getElementById('app').innerHTML = components.layout(content, user);
        } catch (error) {
            utils.showNotification('Ошибка загрузки записей: ' + error.message, 'error');
        }
    },

    async myTrainings() {
        const user = authManager.getUser();
        const userRole = user?.role?.name || user?.role_name;

        if (!user || userRole !== 'trainer') {
            router.navigate('/');
            return;
        }

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${components.loader()}</div>`,
            user
        );

        try {
            const trainings = await api.getMyTrainings();

            const content = `
                <div class="container">
                    <div class="page-header">
                        <h1>Мои тренировки</h1>
                    </div>

                    ${trainings.length === 0 ?
                        components.emptyState('💪', 'Нет тренировок', 'У вас пока нет запланированных тренировок')
                    : `
                        <div class="trainings-list">
                            ${trainings.map(training => {
                                // Backend returns 'bookings' array with user objects
                                const bookings = training.bookings || [];
                                const clients = bookings.map(b => b.user);
                                return `
                                    <div class="trainer-training-card">
                                        <div class="training-header">
                                            <h3>${training.title}</h3>
                                            <span class="training-date">${utils.formatDate(training.date)}</span>
                                        </div>
                                        <div class="training-info">
                                            <div class="info-item">
                                                <span class="info-label">⏰ Время:</span>
                                                <span class="info-value">${training.start_time?.slice(0, 5)} - ${training.end_time?.slice(0, 5)}</span>
                                            </div>
                                            ${training.room ? `
                                                <div class="info-item">
                                                    <span class="info-label">🏠 Помещение:</span>
                                                    <span class="info-value">${training.room.title}</span>
                                                </div>
                                            ` : ''}
                                            ${training.description ? `
                                                <div class="info-item">
                                                    <span class="info-label">📝 Описание:</span>
                                                    <span class="info-value">${training.description}</span>
                                                </div>
                                            ` : ''}
                                        </div>
                                        <div class="training-participants">
                                            <h4>Участники (${clients.length}):</h4>
                                            ${clients.length === 0 ?
                                                '<p class="no-participants">Пока нет записавшихся</p>'
                                            : `
                                                <ul class="participants-list">
                                                    ${clients.map(client => `
                                                        <li>${client.first_name || client.name} ${client.last_name || client.surname} (${client.email})</li>
                                                    `).join('')}
                                                </ul>
                                            `}
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    `}
                </div>
            `;

            document.getElementById('app').innerHTML = components.layout(content, user);
        } catch (error) {
            utils.showNotification('Ошибка загрузки тренировок: ' + error.message, 'error');
        }
    },

    async subscriptions() {
        const user = authManager.getUser();
        const userRole = user?.role?.name || user?.role_name;

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${components.loader()}</div>`,
            user
        );

        try {
            const subscriptions = await api.getAllSubscriptions();

            const content = `
                <div class="container">
                    <div class="page-header">
                        <h1>Доступные абонементы</h1>
                        ${userRole === 'admin' ? `
                            <button class="btn btn-primary" onclick="showCreateSubscriptionModal()">
                                Создать абонемент
                            </button>
                        ` : ''}
                    </div>

                    ${subscriptions.length === 0 ?
                        components.emptyState('🎫', 'Нет абонементов', 'Пока не добавлено ни одного абонемента')
                    : `
                        <div class="subscriptions-grid">
                            ${subscriptions.map(subscription => {
                                const actions = [];

                                if (userRole === 'client') {
                                    actions.push({
                                        type: 'primary',
                                        text: 'Купить',
                                        onclick: `handleBuySubscription(${subscription.id})`
                                    });
                                }

                                if (userRole === 'admin') {
                                    actions.push({
                                        type: 'secondary',
                                        text: 'Редактировать',
                                        onclick: `showEditSubscriptionModal(${subscription.id})`
                                    });
                                    actions.push({
                                        type: 'danger',
                                        text: 'Удалить',
                                        onclick: `handleDeleteSubscription(${subscription.id})`
                                    });
                                }

                                return components.subscriptionCard(subscription, actions);
                            }).join('')}
                        </div>
                    `}
                </div>
            `;

            document.getElementById('app').innerHTML = components.layout(content, user);
        } catch (error) {
            utils.showNotification('Ошибка загрузки абонементов: ' + error.message, 'error');
        }
    },

    async profile() {
        const user = authManager.getUser();
        const userRole = user?.role?.name || user?.role_name;

        if (!user) {
            router.navigate('/login');
            return;
        }

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${components.loader()}</div>`,
            user
        );

        try {
            let roleSpecificSection = '';

            if (userRole === 'client') {
                try {
                    const membership = await api.getMyMembership();

                    // Fetch subscription details
                    const subscriptions = await api.getAllSubscriptions();
                    const subscription = subscriptions.find(s => s.id === membership.subscription_id);

                    roleSpecificSection = `
                        <div class="profile-section">
                            <h2>Мой абонемент</h2>
                            <div class="membership-card active">
                                <div class="membership-header">
                                    <h3>${subscription?.title || 'Абонемент'}</h3>
                                    <span class="membership-status status-active">Активен</span>
                                </div>
                                <div class="membership-body">
                                    <div class="membership-info">
                                        <div class="info-item">
                                            <span class="info-label">📅 Начало:</span>
                                            <span class="info-value">${utils.formatDate(membership.start_date)}</span>
                                        </div>
                                        <div class="info-item">
                                            <span class="info-label">📅 Окончание:</span>
                                            <span class="info-value">${utils.formatDate(membership.end_date)}</span>
                                        </div>
                                        <div class="info-item">
                                            <span class="info-label">⏳ Длительность:</span>
                                            <span class="info-value">${subscription?.duration_days || 0} дней</span>
                                        </div>
                                        <div class="info-item">
                                            <span class="info-label">💰 Цена:</span>
                                            <span class="info-value">${subscription?.price || 0} ₽</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                } catch (error) {
                    roleSpecificSection = `
                        <div class="profile-section">
                            <h2>Мой абонемент</h2>
                            <div class="empty-membership">
                                <p>У вас нет активного абонемента</p>
                                <a href="/subscriptions" class="btn btn-primary" data-link>Выбрать абонемент</a>
                            </div>
                        </div>
                    `;
                }
            } else if (userRole === 'trainer') {
                // Get trainer's workload statistics
                try {
                    const trainings = await api.getMyTrainings();

                    // Calculate statistics
                    const totalTrainings = trainings.length;
                    const totalClients = trainings.reduce((sum, t) => sum + (t.bookings?.length || 0), 0);
                    const avgClientsPerTraining = totalTrainings > 0 ? (totalClients / totalTrainings).toFixed(1) : 0;

                    // Group by day of week
                    const dayNames = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
                    const trainingsByDay = {};
                    const clientsByDay = {};

                    dayNames.forEach(day => {
                        trainingsByDay[day] = 0;
                        clientsByDay[day] = 0;
                    });

                    trainings.forEach(training => {
                        const date = new Date(training.date);
                        const dayName = dayNames[date.getDay()];
                        trainingsByDay[dayName]++;
                        clientsByDay[dayName] += training.bookings?.length || 0;
                    });

                    const maxTrainings = Math.max(...Object.values(trainingsByDay), 1);
                    const maxClients = Math.max(...Object.values(clientsByDay), 1);

                    roleSpecificSection = `
                        <div class="profile-section">
                            <h2>Статистика нагрузки</h2>

                            <!-- Stats Cards -->
                            <div class="stats-cards">
                                <div class="stat-card">
                                    <div class="stat-card-icon">📊</div>
                                    <div class="stat-card-value">${totalTrainings}</div>
                                    <div class="stat-card-label">Всего тренировок</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-card-icon">👥</div>
                                    <div class="stat-card-value">${totalClients}</div>
                                    <div class="stat-card-label">Всего клиентов</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-card-icon">📈</div>
                                    <div class="stat-card-value">${avgClientsPerTraining}</div>
                                    <div class="stat-card-label">Среднее участников</div>
                                </div>
                            </div>

                            <!-- Charts -->
                            <div class="workload-charts">
                                <div class="chart-container">
                                    <h3 class="chart-title">Тренировки по дням недели</h3>
                                    <div class="bar-chart">
                                        ${dayNames.map(day => `
                                            <div class="bar-item">
                                                <div class="bar-wrapper">
                                                    <div class="bar" style="height: ${(trainingsByDay[day] / maxTrainings) * 100}%">
                                                        <span class="bar-value">${trainingsByDay[day]}</span>
                                                    </div>
                                                </div>
                                                <div class="bar-label">${day.slice(0, 2)}</div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>

                                <div class="chart-container">
                                    <h3 class="chart-title">Клиенты по дням недели</h3>
                                    <div class="bar-chart">
                                        ${dayNames.map(day => `
                                            <div class="bar-item">
                                                <div class="bar-wrapper">
                                                    <div class="bar bar-secondary" style="height: ${(clientsByDay[day] / maxClients) * 100}%">
                                                        <span class="bar-value">${clientsByDay[day]}</span>
                                                    </div>
                                                </div>
                                                <div class="bar-label">${day.slice(0, 2)}</div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                } catch (error) {
                    roleSpecificSection = `
                        <div class="profile-section">
                            <h2>Статистика нагрузки</h2>
                            <p class="empty-state-text">Не удалось загрузить статистику</p>
                        </div>
                    `;
                }
            }

            const content = `
                <div class="container">
                    <h1>Профиль</h1>

                    <div class="profile-section">
                        <h2>Личная информация</h2>
                        <div class="profile-info">
                            <div class="info-item">
                                <span class="info-label">Имя:</span>
                                <span class="info-value">${user.first_name || user.name || ''} ${user.last_name || user.surname || ''}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Email:</span>
                                <span class="info-value">${user.email}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Роль:</span>
                                <span class="info-value">${components.getRoleText(userRole)}</span>
                            </div>
                        </div>
                    </div>

                    ${roleSpecificSection}
                </div>
            `;

            document.getElementById('app').innerHTML = components.layout(content, user);
        } catch (error) {
            utils.showNotification('Ошибка загрузки профиля: ' + error.message, 'error');
        }
    },

    async admin(usersPage = 1, requestsPage = 1, membershipsPage = 1, roomsPage = 1) {
        const user = authManager.getUser();
        const userRole = user?.role?.name || user?.role_name;

        if (!user || userRole !== 'admin') {
            router.navigate('/');
            return;
        }

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${components.loader()}</div>`,
            user
        );

        try {
            // Load all data in parallel
            const [users, requests, memberships, rooms] = await Promise.all([
                api.getAllUsers(),
                api.getAllRequests(),
                api.getAllMemberships(),
                api.getRooms()
            ]);

            // Pagination settings
            const itemsPerPage = 5;

            // Users pagination
            const totalUsersPages = Math.ceil(users.length / itemsPerPage);
            const usersStart = (usersPage - 1) * itemsPerPage;
            const usersEnd = usersStart + itemsPerPage;
            const paginatedUsers = users.slice(usersStart, usersEnd);

            // Requests pagination - show latest first
            const sortedRequests = [...requests].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            const totalRequestsPages = Math.ceil(sortedRequests.length / itemsPerPage);
            const requestsStart = (requestsPage - 1) * itemsPerPage;
            const requestsEnd = requestsStart + itemsPerPage;
            const paginatedRequests = sortedRequests.slice(requestsStart, requestsEnd);

            // Memberships pagination
            const totalMembershipsPages = Math.ceil(memberships.length / itemsPerPage);
            const membershipsStart = (membershipsPage - 1) * itemsPerPage;
            const membershipsEnd = membershipsStart + itemsPerPage;
            const paginatedMemberships = memberships.slice(membershipsStart, membershipsEnd);

            // Rooms pagination
            const totalRoomsPages = Math.ceil(rooms.length / itemsPerPage);
            const roomsStart = (roomsPage - 1) * itemsPerPage;
            const roomsEnd = roomsStart + itemsPerPage;
            const paginatedRooms = rooms.slice(roomsStart, roomsEnd);

            const content = `
                <div class="container">
                    <h1>Панель администратора</h1>

                    <!-- Users Section -->
                    <div class="admin-section">
                        <h2>Пользователи системы (${users.length})</h2>
                        <div class="admin-table-wrapper">
                            <table class="admin-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Имя</th>
                                        <th>Email</th>
                                        <th>Роль</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${paginatedUsers.map(u => `
                                        <tr>
                                            <td>${u.id}</td>
                                            <td>${u.first_name || u.name} ${u.last_name || u.surname}</td>
                                            <td>${u.email}</td>
                                            <td><span class="role-badge role-${u.role_name || u.role?.name}">${components.getRoleText(u.role_name || u.role?.name)}</span></td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        ${components.pagination(usersPage, totalUsersPages, 'handleUsersPageChange')}
                    </div>

                    <!-- Requests Section -->
                    <div class="admin-section">
                        <h2>Заявки на абонементы (${requests.length})</h2>
                        ${requests.length === 0 ? `
                            <p class="empty-state-text">Нет заявок</p>
                        ` : `
                            <div class="requests-list">
                                ${paginatedRequests.map(req => `
                                    <div class="request-item collapsible" data-request-id="${req.id}">
                                        <div class="request-item-header" onclick="handleToggleRequest(${req.id})">
                                            <div class="request-item-title">
                                                <span class="chevron">▶</span>
                                                <strong>${req.user.first_name || req.user.name} ${req.user.last_name || req.user.surname}</strong>
                                                <span class="request-item-email">${req.user.email}</span>
                                            </div>
                                            <span class="request-status-badge status-${req.status}">${pages.getRequestStatusText(req.status)}</span>
                                        </div>
                                        <div class="request-item-body" style="display: none;">
                                            <div class="request-details">
                                                <div class="info-item">
                                                    <span class="info-label">🎫 Абонемент:</span>
                                                    <span class="info-value">${req.subscription.title}</span>
                                                </div>
                                                <div class="info-item">
                                                    <span class="info-label">💰 Цена:</span>
                                                    <span class="info-value">${req.subscription.price} ₽</span>
                                                </div>
                                                <div class="info-item">
                                                    <span class="info-label">⏳ Длительность:</span>
                                                    <span class="info-value">${req.subscription.duration_days} дней</span>
                                                </div>
                                                <div class="info-item">
                                                    <span class="info-label">📅 Дата заявки:</span>
                                                    <span class="info-value">${utils.formatDateTime(req.created_at)}</span>
                                                </div>
                                            </div>
                                            ${req.status === 'pending' ? `
                                                <div class="request-item-actions">
                                                    <button class="btn btn-success" onclick="event.stopPropagation(); handleApproveRequest(${req.id})">
                                                        ✓ Одобрить
                                                    </button>
                                                    <button class="btn btn-danger" onclick="event.stopPropagation(); handleRejectRequest(${req.id})">
                                                        ✗ Отклонить
                                                    </button>
                                                </div>
                                            ` : ''}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                            ${components.pagination(requestsPage, totalRequestsPages, 'handleRequestsPageChange')}
                        `}
                    </div>

                    <!-- Memberships Section -->
                    <div class="admin-section">
                        <h2>Активные абонементы (${memberships.length})</h2>
                        ${memberships.length === 0 ? `
                            <p class="empty-state-text">Нет активных абонементов</p>
                        ` : `
                            <div class="admin-table-wrapper">
                                <table class="admin-table">
                                    <thead>
                                        <tr>
                                            <th>Клиент</th>
                                            <th>Абонемент</th>
                                            <th>Начало</th>
                                            <th>Окончание</th>
                                            <th>Статус</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${paginatedMemberships.map(m => `
                                            <tr>
                                                <td>${m.user.first_name || m.user.name} ${m.user.last_name || m.user.surname}</td>
                                                <td>${m.subscription.title}</td>
                                                <td>${utils.formatDate(m.start_date)}</td>
                                                <td>${utils.formatDate(m.end_date)}</td>
                                                <td><span class="status-badge status-${m.status}">${m.status === 'active' ? 'Активен' : 'Истек'}</span></td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                            ${components.pagination(membershipsPage, totalMembershipsPages, 'handleMembershipsPageChange')}
                        `}
                    </div>

                    <!-- Rooms Section -->
                    <div class="admin-section">
                        <h2>Помещения (${rooms.length})</h2>
                        <button class="btn btn-primary" onclick="handleShowAddRoomModal()">+ Добавить помещение</button>

                        ${rooms.length === 0 ? `
                            <p class="empty-state-text">Нет помещений</p>
                        ` : `
                            <div class="admin-table-wrapper">
                                <table class="admin-table">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Название</th>
                                            <th>Вместимость</th>
                                            <th>Действия</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${paginatedRooms.map(room => `
                                            <tr>
                                                <td>${room.id}</td>
                                                <td>${room.title}</td>
                                                <td>${room.capacity} чел.</td>
                                                <td class="action-buttons">
                                                    <button class="btn btn-small btn-secondary" onclick="handleEditRoom(${room.id}, '${room.title}', ${room.capacity})">
                                                        ✎ Редактировать
                                                    </button>
                                                    <button class="btn btn-small btn-danger" onclick="handleDeleteRoom(${room.id}, '${room.title}')">
                                                        🗑 Удалить
                                                    </button>
                                                </td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                            ${components.pagination(roomsPage, totalRoomsPages, 'handleRoomsPageChange')}
                        `}
                    </div>
                </div>
            `;

            document.getElementById('app').innerHTML = components.layout(content, user);
        } catch (error) {
            utils.showNotification('Ошибка загрузки админ-панели: ' + error.message, 'error');
        }
    },

    getRequestStatusText(status) {
        const statuses = {
            'pending': 'Ожидает',
            'approved': 'Одобрена',
            'rejected': 'Отклонена'
        };
        return statuses[status] || status;
    },

    notFound() {
        const user = authManager.getUser();
        const content = components.emptyState(
            '404',
            'Страница не найдена',
            'К сожалению, запрашиваемая страница не существует.'
        );

        document.getElementById('app').innerHTML = components.layout(
            `<div class="container">${content}</div>`,
            user
        );
    }
};
