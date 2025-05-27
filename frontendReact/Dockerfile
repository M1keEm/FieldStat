FROM node:18-alpine3.17 as build

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

FROM nginx:alpine

# Remove the default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build files from the build stage
COPY --from=build /app/dist /var/www/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

