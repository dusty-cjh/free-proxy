## 使用步骤

1. 将上面文件中的 `external.hdcjh.xyz` 替换成自己的域名
2. 将上面文件中的 `example@mail.com` 替换成自己的邮箱
3. 生成面板密码：`echo $(htpasswd -nb user password) | sed -e s/\\$/\\$\\$/g`
4. 将密码粘贴到 docker-compose.yml 这里：`traefik.http.middlewares.traefik-auth.basicauth.users`
5. 创建网络：`docker network create traefik`
6. 启动：`docker-compose up -d`
7. 访问：`https://your.domain.com/dashboard` 来查看是否成功访问面板
8. 搞定


