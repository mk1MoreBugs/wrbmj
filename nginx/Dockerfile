FROM nginx:1.27.3-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx data /usr/share/nginx/html
EXPOSE 80
