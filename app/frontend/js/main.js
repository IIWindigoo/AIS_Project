// Main application file

// Global event handlers
async function handleLogout() {
    const result = await authManager.logout();
    if (result.success) {
        utils.showNotification('Вы вышли из системы', 'success');
        router.navigate('/');
    }
}

async function handleBookTraining(trainingId) {
    try {
        await api.createBooking(trainingId);
        utils.showNotification('Вы успешно записались на тренировку!', 'success');
        router.navigate('/my-bookings');
    } catch (error) {
        utils.showNotification('Ошибка записи: ' + error.message, 'error');
    }
}

async function handleCancelBooking(trainingId) {
    const confirmed = await utils.showModal(
        'Подтверждение',
        'Вы уверены, что хотите отменить запись?',
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, отменить', action: 'confirm', type: 'danger' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.cancelBooking(trainingId);
            utils.showNotification('Запись отменена', 'success');
            pages.myBookings();
        } catch (error) {
            utils.showNotification('Ошибка отмены: ' + error.message, 'error');
        }
    }
}

async function handleDeleteTraining(trainingId) {
    const confirmed = await utils.showModal(
        'Удаление тренировки',
        'Вы уверены, что хотите удалить эту тренировку?',
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, удалить', action: 'confirm', type: 'danger' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.deleteTraining(trainingId);
            utils.showNotification('Тренировка удалена', 'success');
            pages.trainings();
        } catch (error) {
            utils.showNotification('Ошибка удаления: ' + error.message, 'error');
        }
    }
}

// Фильтрация и поиск тренировок
function handleTrainingSearch() {
    handleTrainingFilter();
}

function handleTrainingFilter() {
    if (!window.allTrainings || !window.renderTrainings) return;

    const searchInput = document.getElementById('trainingSearch');
    const dateFilter = document.getElementById('dateFilter');
    const availabilityFilter = document.getElementById('availabilityFilter');

    const searchQuery = searchInput?.value || '';
    const dateValue = dateFilter?.value || 'all';
    const availabilityValue = availabilityFilter?.value || 'all';

    let filtered = window.allTrainings;

    // Поиск по названию или тренеру
    if (searchQuery) {
        const query = searchQuery.toLowerCase();
        filtered = filtered.filter(training => {
            const title = training.title?.toLowerCase() || '';
            const trainerName = `${training.trainer?.first_name || ''} ${training.trainer?.last_name || ''}`.toLowerCase();
            return title.includes(query) || trainerName.includes(query);
        });
    }

    // Фильтр по дате
    if (dateValue !== 'all') {
        const now = new Date();
        now.setHours(0, 0, 0, 0);

        filtered = filtered.filter(training => {
            const trainingDate = new Date(training.date);
            trainingDate.setHours(0, 0, 0, 0);

            if (dateValue === 'today') {
                return trainingDate.getTime() === now.getTime();
            } else if (dateValue === 'week') {
                const weekEnd = new Date(now);
                weekEnd.setDate(weekEnd.getDate() + 7);
                return trainingDate >= now && trainingDate <= weekEnd;
            } else if (dateValue === 'month') {
                const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0);
                return trainingDate >= now && trainingDate <= monthEnd;
            }
            return true;
        });
    }

    // Фильтр по доступности мест
    if (availabilityValue !== 'all') {
        filtered = filtered.filter(training => {
            const bookingCount = training.booking_count || 0;
            const capacity = training.room?.capacity || 0;
            const isFull = bookingCount >= capacity;

            if (availabilityValue === 'available') {
                return !isFull;
            } else if (availabilityValue === 'full') {
                return isFull;
            }
            return true;
        });
    }

    // Перерисовываем с сохранением значений фильтров
    window.renderTrainings(filtered, searchQuery, dateValue, availabilityValue);
}

function resetTrainingFilters() {
    if (!window.allTrainings || !window.renderTrainings) return;

    // Сбрасываем все фильтры
    const searchInput = document.getElementById('trainingSearch');
    const dateFilter = document.getElementById('dateFilter');
    const availabilityFilter = document.getElementById('availabilityFilter');

    if (searchInput) searchInput.value = '';
    if (dateFilter) dateFilter.value = 'all';
    if (availabilityFilter) availabilityFilter.value = 'all';

    // Показываем все тренировки
    window.renderTrainings(window.allTrainings, '', 'all', 'all');

    utils.showNotification('Фильтры сброшены', 'info');
}

async function showCreateTrainingModal() {
    try {
        const rooms = await api.getAllRooms();
        const users = await api.getAllUsers();
        const trainers = users.filter(u => (u.role?.name || u.role_name) === 'trainer');

        const modalContent = `
            <form id="createTrainingForm">
                <div class="form-group">
                    <label class="form-label">Название *</label>
                    <input type="text" name="title" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Описание</label>
                    <textarea name="description" class="form-input" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Дата и время *</label>
                    <input type="datetime-local" name="date" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Длительность (минуты) *</label>
                    <input type="number" name="duration" class="form-input" required min="15" step="15" value="60">
                </div>
                <div class="form-group">
                    <label class="form-label">Тренер *</label>
                    <select name="trainer_id" class="form-input" required>
                        <option value="">Выберите тренера</option>
                        ${trainers.map(t => `<option value="${t.id}">${t.first_name || t.name} ${t.last_name || t.surname}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Помещение *</label>
                    <select name="room_id" class="form-input" required>
                        <option value="">Выберите помещение</option>
                        ${rooms.map(r => `<option value="${r.id}">${r.title}</option>`).join('')}
                    </select>
                </div>
            </form>
        `;

        const action = await utils.showModal(
            'Создать тренировку',
            modalContent,
            [
                { text: 'Отмена', action: 'cancel', type: 'secondary' },
                { text: 'Создать', action: 'create', type: 'primary' }
            ]
        );

        if (action === 'create') {
            const form = document.getElementById('createTrainingForm');
            const formData = new FormData(form);

            // Parse datetime-local value
            const datetimeStr = formData.get('date');
            const datetime = new Date(datetimeStr);

            // Extract date in YYYY-MM-DD format
            const date = datetime.toISOString().split('T')[0];

            // Extract start time in HH:MM:SS format
            const hours = String(datetime.getHours()).padStart(2, '0');
            const minutes = String(datetime.getMinutes()).padStart(2, '0');
            const start_time = `${hours}:${minutes}:00`;

            // Calculate end time based on duration
            const durationMinutes = parseInt(formData.get('duration'));
            const endDatetime = new Date(datetime.getTime() + durationMinutes * 60000);
            const endHours = String(endDatetime.getHours()).padStart(2, '0');
            const endMinutes = String(endDatetime.getMinutes()).padStart(2, '0');
            const end_time = `${endHours}:${endMinutes}:00`;

            const data = {
                title: formData.get('title'),
                description: formData.get('description') || '',
                date: date,
                start_time: start_time,
                end_time: end_time,
                trainer_id: parseInt(formData.get('trainer_id')),
                room_id: parseInt(formData.get('room_id'))
            };

            await api.createTraining(data);
            utils.showNotification('Тренировка создана!', 'success');
            pages.trainings();
        }
    } catch (error) {
        utils.showNotification('Ошибка создания: ' + error.message, 'error');
    }
}

async function showEditTrainingModal(trainingId) {
    try {
        const trainings = await api.getAllTrainings();
        const training = trainings.find(t => t.id === trainingId);

        if (!training) {
            utils.showNotification('Тренировка не найдена', 'error');
            return;
        }

        const rooms = await api.getAllRooms();
        const users = await api.getAllUsers();
        const trainers = users.filter(u => (u.role?.name || u.role_name) === 'trainer');

        // Combine date and start_time to create datetime-local value
        const dateStr = `${training.date}T${training.start_time.slice(0, 5)}`;

        // Calculate duration from start_time and end_time
        const [startHours, startMinutes] = training.start_time.split(':').map(Number);
        const [endHours, endMinutes] = training.end_time.split(':').map(Number);
        const durationMinutes = (endHours * 60 + endMinutes) - (startHours * 60 + startMinutes);

        const modalContent = `
            <form id="editTrainingForm">
                <div class="form-group">
                    <label class="form-label">Название *</label>
                    <input type="text" name="title" class="form-input" value="${training.title}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Описание</label>
                    <textarea name="description" class="form-input" rows="3">${training.description || ''}</textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Дата и время *</label>
                    <input type="datetime-local" name="date" class="form-input" value="${dateStr}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Длительность (минуты) *</label>
                    <input type="number" name="duration" class="form-input" value="${durationMinutes}" required min="15" step="15">
                </div>
                <div class="form-group">
                    <label class="form-label">Тренер *</label>
                    <select name="trainer_id" class="form-input" required>
                        ${trainers.map(t => `
                            <option value="${t.id}" ${t.id === training.trainer_id ? 'selected' : ''}>
                                ${t.first_name || t.name} ${t.last_name || t.surname}
                            </option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Помещение *</label>
                    <select name="room_id" class="form-input" required>
                        ${rooms.map(r => `
                            <option value="${r.id}" ${r.id === training.room_id ? 'selected' : ''}>
                                ${r.title}
                            </option>
                        `).join('')}
                    </select>
                </div>
            </form>
        `;

        const action = await utils.showModal(
            'Редактировать тренировку',
            modalContent,
            [
                { text: 'Отмена', action: 'cancel', type: 'secondary' },
                { text: 'Сохранить', action: 'save', type: 'primary' }
            ]
        );

        if (action === 'save') {
            const form = document.getElementById('editTrainingForm');
            const formData = new FormData(form);

            // Parse datetime-local value
            const datetimeStr = formData.get('date');
            const datetime = new Date(datetimeStr);

            // Extract date in YYYY-MM-DD format
            const date = datetime.toISOString().split('T')[0];

            // Extract start time in HH:MM:SS format
            const hours = String(datetime.getHours()).padStart(2, '0');
            const minutes = String(datetime.getMinutes()).padStart(2, '0');
            const start_time = `${hours}:${minutes}:00`;

            // Calculate end time based on duration
            const durationMinutes = parseInt(formData.get('duration'));
            const endDatetime = new Date(datetime.getTime() + durationMinutes * 60000);
            const endHours = String(endDatetime.getHours()).padStart(2, '0');
            const endMinutes = String(endDatetime.getMinutes()).padStart(2, '0');
            const end_time = `${endHours}:${endMinutes}:00`;

            const data = {
                title: formData.get('title'),
                description: formData.get('description') || '',
                date: date,
                start_time: start_time,
                end_time: end_time
            };

            await api.updateTraining(trainingId, data);
            utils.showNotification('Тренировка обновлена!', 'success');
            pages.trainings();
        }
    } catch (error) {
        utils.showNotification('Ошибка обновления: ' + error.message, 'error');
    }
}

// Subscriptions handlers
async function handleDeleteSubscription(subId) {
    const confirmed = await utils.showModal(
        'Удаление абонемента',
        'Вы уверены, что хотите удалить этот абонемент?',
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, удалить', action: 'confirm', type: 'danger' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.deleteSubscription(subId);
            utils.showNotification('Абонемент удален', 'success');
            pages.subscriptions();
        } catch (error) {
            utils.showNotification('Ошибка удаления: ' + error.message, 'error');
        }
    }
}

async function showCreateSubscriptionModal() {
    const modalContent = `
        <form id="createSubscriptionForm">
            <div class="form-group">
                <label class="form-label">Название *</label>
                <input type="text" name="title" class="form-input" required minlength="2" maxlength="30">
            </div>
            <div class="form-group">
                <label class="form-label">Цена (рубли) *</label>
                <input type="number" name="price" class="form-input" required min="1" value="1000">
            </div>
            <div class="form-group">
                <label class="form-label">Длительность (дни) *</label>
                <input type="number" name="duration_days" class="form-input" required min="1" value="30">
            </div>
        </form>
    `;

    try {
        const action = await utils.showModal(
            'Создать абонемент',
            modalContent,
            [
                { text: 'Отмена', action: 'cancel', type: 'secondary' },
                { text: 'Создать', action: 'create', type: 'primary' }
            ]
        );

        if (action === 'create') {
            const form = document.getElementById('createSubscriptionForm');
            const formData = new FormData(form);

            const data = {
                title: formData.get('title'),
                price: parseInt(formData.get('price')),
                duration_days: parseInt(formData.get('duration_days'))
            };

            await api.createSubscription(data);
            utils.showNotification('Абонемент создан!', 'success');
            pages.subscriptions();
        }
    } catch (error) {
        utils.showNotification('Ошибка создания: ' + error.message, 'error');
    }
}

async function showEditSubscriptionModal(subId) {
    try {
        const subscriptions = await api.getAllSubscriptions();
        const subscription = subscriptions.find(s => s.id === subId);

        if (!subscription) {
            utils.showNotification('Абонемент не найден', 'error');
            return;
        }

        const modalContent = `
            <form id="editSubscriptionForm">
                <div class="form-group">
                    <label class="form-label">Название *</label>
                    <input type="text" name="title" class="form-input" value="${subscription.title}" required minlength="2" maxlength="30">
                </div>
                <div class="form-group">
                    <label class="form-label">Цена (рубли) *</label>
                    <input type="number" name="price" class="form-input" value="${subscription.price}" required min="1">
                </div>
                <div class="form-group">
                    <label class="form-label">Длительность (дни) *</label>
                    <input type="number" name="duration_days" class="form-input" value="${subscription.duration_days}" required min="1">
                </div>
            </form>
        `;

        const action = await utils.showModal(
            'Редактировать абонемент',
            modalContent,
            [
                { text: 'Отмена', action: 'cancel', type: 'secondary' },
                { text: 'Сохранить', action: 'save', type: 'primary' }
            ]
        );

        if (action === 'save') {
            const form = document.getElementById('editSubscriptionForm');
            const formData = new FormData(form);

            const data = {
                title: formData.get('title'),
                price: parseInt(formData.get('price')),
                duration_days: parseInt(formData.get('duration_days'))
            };

            await api.updateSubscription(subId, data);
            utils.showNotification('Абонемент обновлен!', 'success');
            pages.subscriptions();
        }
    } catch (error) {
        utils.showNotification('Ошибка обновления: ' + error.message, 'error');
    }
}

// Membership handlers
async function handleBuySubscription(subscriptionId) {
    const confirmed = await utils.showModal(
        'Подтверждение покупки',
        'Вы уверены, что хотите подать заявку на этот абонемент? После одобрения администратором абонемент будет активирован.',
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, подать заявку', action: 'confirm', type: 'primary' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.createSubscriptionRequest(subscriptionId);
            utils.showNotification('Заявка на абонемент успешно отправлена! Ожидайте одобрения администратора.', 'success');
            router.navigate('/profile');
        } catch (error) {
            utils.showNotification('Ошибка: ' + error.message, 'error');
        }
    }
}

async function handleApproveRequest(requestId) {
    const confirmed = await utils.showModal(
        'Одобрить заявку',
        'Вы уверены, что хотите одобрить эту заявку? Будет создан активный абонемент для клиента.',
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, одобрить', action: 'confirm', type: 'success' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.updateRequestStatus(requestId, 'approved');
            utils.showNotification('Заявка одобрена! Абонемент активирован.', 'success');
            pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage);
        } catch (error) {
            utils.showNotification('Ошибка: ' + error.message, 'error');
        }
    }
}

async function handleRejectRequest(requestId) {
    const confirmed = await utils.showModal(
        'Отклонить заявку',
        'Вы уверены, что хотите отклонить эту заявку?',
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, отклонить', action: 'confirm', type: 'danger' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.updateRequestStatus(requestId, 'rejected');
            utils.showNotification('Заявка отклонена.', 'success');
            pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage);
        } catch (error) {
            utils.showNotification('Ошибка: ' + error.message, 'error');
        }
    }
}

// Admin pagination handlers
let adminState = {
    usersPage: 1,
    requestsPage: 1,
    membershipsPage: 1,
    roomsPage: 1
};

function handleUsersPageChange(page) {
    adminState.usersPage = page;
    pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage);
}

function handleRequestsPageChange(page) {
    adminState.requestsPage = page;
    pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage);
}

function handleMembershipsPageChange(page) {
    adminState.membershipsPage = page;
    pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage || 1);
}

function handleRoomsPageChange(page) {
    adminState.roomsPage = page;
    pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage);
}

async function handleShowAddRoomModal() {
    const modalContent = `
        <form id="addRoomForm">
            <div class="form-group">
                <label class="form-label">Название помещения *</label>
                <input type="text" name="title" class="form-input" required minlength="2" maxlength="30" placeholder="Например: Зал №1">
            </div>
            <div class="form-group">
                <label class="form-label">Вместимость *</label>
                <input type="number" name="capacity" class="form-input" required min="1" max="1000" placeholder="Количество человек">
            </div>
        </form>
    `;

    const result = await utils.showModal(
        'Добавить помещение',
        modalContent,
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Добавить', action: 'confirm', type: 'primary' }
        ]
    );

    if (result === 'confirm') {
        const form = document.getElementById('addRoomForm');
        const formData = new FormData(form);
        const data = {
            title: formData.get('title'),
            capacity: parseInt(formData.get('capacity'))
        };

        try {
            await api.createRoom(data);
            utils.showNotification('Помещение успешно добавлено', 'success');
            pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage || 1);
        } catch (error) {
            utils.showNotification('Ошибка создания помещения: ' + error.message, 'error');
        }
    }
}

async function handleEditRoom(roomId, currentTitle, currentCapacity) {
    const modalContent = `
        <form id="editRoomForm">
            <div class="form-group">
                <label class="form-label">Название помещения *</label>
                <input type="text" name="title" class="form-input" required minlength="2" maxlength="30" value="${currentTitle}">
            </div>
            <div class="form-group">
                <label class="form-label">Вместимость *</label>
                <input type="number" name="capacity" class="form-input" required min="1" max="1000" value="${currentCapacity}">
            </div>
        </form>
    `;

    const result = await utils.showModal(
        'Редактировать помещение',
        modalContent,
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Сохранить', action: 'confirm', type: 'primary' }
        ]
    );

    if (result === 'confirm') {
        const form = document.getElementById('editRoomForm');
        const formData = new FormData(form);
        const data = {
            title: formData.get('title'),
            capacity: parseInt(formData.get('capacity'))
        };

        try {
            await api.updateRoom(roomId, data);
            utils.showNotification('Помещение успешно обновлено', 'success');
            pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage || 1);
        } catch (error) {
            utils.showNotification('Ошибка обновления помещения: ' + error.message, 'error');
        }
    }
}

async function handleDeleteRoom(roomId, roomTitle) {
    const confirmed = await utils.showModal(
        'Удаление помещения',
        `Вы уверены, что хотите удалить помещение "${roomTitle}"?<br><br><strong>Внимание:</strong> Все связанные с ним тренировки также будут затронуты.`,
        [
            { text: 'Отмена', action: 'cancel', type: 'secondary' },
            { text: 'Да, удалить', action: 'confirm', type: 'danger' }
        ]
    );

    if (confirmed === 'confirm') {
        try {
            await api.deleteRoom(roomId);
            utils.showNotification('Помещение успешно удалено', 'success');
            pages.admin(adminState.usersPage, adminState.requestsPage, adminState.membershipsPage, adminState.roomsPage || 1);
        } catch (error) {
            utils.showNotification('Ошибка удаления помещения: ' + error.message, 'error');
        }
    }
}

function handleToggleRequest(requestId) {
    const requestItem = document.querySelector(`.request-item[data-request-id="${requestId}"]`);
    if (!requestItem) return;

    const body = requestItem.querySelector('.request-item-body');
    const chevron = requestItem.querySelector('.chevron');

    if (body.style.display === 'none') {
        body.style.display = 'block';
        chevron.textContent = '▼';
        requestItem.classList.add('expanded');
    } else {
        body.style.display = 'none';
        chevron.textContent = '▶';
        requestItem.classList.remove('expanded');
    }
}

// Setup routes
router.addRoute('/', pages.home);
router.addRoute('/login', pages.login);
router.addRoute('/register', pages.register);
router.addRoute('/trainings', pages.trainings);
router.addRoute('/subscriptions', pages.subscriptions);
router.addRoute('/my-bookings', pages.myBookings);
router.addRoute('/my-trainings', pages.myTrainings);
router.addRoute('/profile', pages.profile);
router.addRoute('/admin', () => {
    // Reset admin pagination state when navigating to admin page
    adminState = { usersPage: 1, requestsPage: 1, membershipsPage: 1, roomsPage: 1 };
    return pages.admin();
});
router.addRoute('/404', pages.notFound);

// Authentication guard
router.beforeEach(async (to, from) => {
    const publicRoutes = ['/', '/login', '/register', '/trainings', '/subscriptions'];
    const isPublic = publicRoutes.includes(to);

    if (!isPublic && !authManager.isAuthenticated()) {
        utils.showNotification('Требуется авторизация', 'warning');
        return '/login';
    }

    return true;
});

// Initialize app
async function initApp() {
    try {
        await authManager.checkAuth();
    } catch (error) {
        console.log('Not authenticated');
    }

    // Subscribe to auth changes
    authManager.subscribe((user) => {
        // Re-render current page on auth change
        router.handleRoute();
    });

    // Start router
    router.start();
}

// Start the app when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
