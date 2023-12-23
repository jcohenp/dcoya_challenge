# Use vanilla Alpine as the base image
FROM alpine:latest

# Install necessary packages (Nginx and OpenSSL)
RUN apk update && apk add nginx openssl

# Copy index.html and default Nginx configuration
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf

# Generate SSL certificate (self-signed)
RUN openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -subj "/C=IL/L=Tel aviv/O=JulOrganization/CN=dcoya" \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt

# Set permissions for SSL files and Nginx directories
RUN chmod 600 /etc/ssl/private/nginx-selfsigned.key \
    && chmod 644 /etc/ssl/certs/nginx-selfsigned.crt \
    && chown -R nginx:nginx /etc/ssl/private/nginx-selfsigned.key \
    && chown -R nginx:nginx /etc/ssl/certs/nginx-selfsigned.crt \
    && mkdir -p /run/nginx \
    && chown -R nginx:nginx /etc/nginx \
    && chown -R nginx:nginx /var/lib/nginx \
    && chown -R nginx:nginx /run/nginx \
    && chown -R nginx:nginx /usr/share/nginx

# Create environment file (machine-name.txt) for my nginx configuration
COPY machine-name.txt /usr/share/nginx/html/machine-name.txt

# Switch to non-root user (nginx)
USER nginx

# Expose port 443 (HTTPS)
EXPOSE 443

# Nginx execution as default process for the Docker image
CMD ["nginx", "-g", "daemon off;"]
