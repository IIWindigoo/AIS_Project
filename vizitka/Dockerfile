FROM nginx:alpine

# Копируем все файлы сайта в nginx
COPY . /usr/share/nginx/html/

# Копируем конфигурацию nginx (если есть)
COPY nginx.conf /etc/nginx/nginx.conf

# Создаем лог-файлы
RUN touch /var/log/nginx/access.log && touch /var/log/nginx/error.log

# Устанавливаем правильные права
RUN chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]