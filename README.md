# 高速、免费的 ChatGPT 代理节点

## 使用方法
### 1. 使用 curl 访问
把下面的命令粘贴到 cmd 即可，记得替换上自己的 API KEY
```sh
curl -X POST --location "https://external.hdcjh.xyz/62239e6c0f995ae1/v1/completions" \
    -H "Authorization: Bearer 这里填你的API KEY" \
    -H "Content-Type: application/json" \
    -d "{
          \"model\": \"text-davinci-003\",
          \"prompt\": \"Say this is a test\",
          \"max_tokens\": 7,
          \"temperature\": 0
        }"
```

### 2. 使用 python openai 模块访问
```py
import openai

# 这里记得修改成自己的 API KEY
openai.api_key = 'sk-jiofjg89ghprhgprhhghrgshp8hg3hgrugh3g'
openai.api_base = 'https://external.hdcjh.xyz/62239e6c0f995ae1/v1'  # md5(b'ChatGPT').digest()[:8].hex()

# 一个调用的小例子
messages = [{"role": "user", "content": "老公，你说句话呀"}]
completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
            )
response = completion.choices[0]
print(response)
```

## 搭建方法
### 原理
使用 Traefik 作为反向代理，把关于 ChatGPT 的请求转发到 openai 即可。
### 前期准备
* 买一个国外的 VPS
* 为 VPS 申请域名、证书
* 使用 Cloudflare 托管域名
* 在 VPS 上安装 docker
* 使用 docker 安装 traefik
### 配置 Traefik
1. 创建一个配置文件 `/etc/traefik/traefik.yml`
记得把里面的 example@mail.com 替换为自己的邮箱，该邮箱将用于 Traefik 自动去 Let's Encrypt 上申请证书。

```yaml
global:
  checkNewVersion: true
  sendAnonymousUsage: false  # true by default

  # (Optional) Log information
  # ---
  # log:
  #  level: ERROR  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  #   format: common  # common, json, logfmt
  #   filePath: /var/log/traefik/traefik.log

# (Optional) Accesslog
# ---
accessLog:
  format: common  # common, json, logfmt
  filePath: /var/log/traefik/access.log
  bufferingSize: 100

# (Optional) Enable API and Dashboard
# ---
api:
  dashboard: true  # true by default
  insecure: true  # Don't do this in production!

# Entry Points configuration
# ---
entryPoints:
  web:
    address: :80
    # (Optional) Redirect to HTTPS
    # ---
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https

  websecure:
    address: :443

# Configure your CertificateResolver here...
# ---
certificatesResolvers:
  staging:
    acme:
      email: example@mail.com
      storage: /ssl-certs/acme.json
      caServer: "https://acme-staging-v02.api.letsencrypt.org/directory"
      httpChallenge:
        entryPoint: web

  production:
    acme:
      email: example@mail.com
      storage: /ssl-certs/acme.json
      caServer: "https://acme-v02.api.letsencrypt.org/directory"
      httpChallenge:
        entryPoint: web

# (Optional) Overwrite Default Certificates
# tls:
#   stores:
#     default:
#       defaultCertificate:
#         certFile: /etc/traefik/certs/cert.pem
#         keyFile: /etc/traefik/certs/cert-key.pem
# (Optional) Disable TLS version 1.0 and 1.1
#   options:
#     default:
#       minVersion: VersionTLS12

providers:
  docker:
    exposedByDefault: false  # Default is true
  file:
    filename: /etc/traefik/config.yml
    watch: true
  providersThrottleDuration: 10s

experimental:
  hub: true

metrics:
  prometheus:
    addEntryPointsLabels: true
    addServicesLabels: true
    entryPoint: websecure
    addRoutersLabels: true
```

2. 创建 Traefik 的动态配置文件 `/etc/traefik/config.yml`
```yaml
# official config file example: https://doc.traefik.io/traefik/reference/dynamic-configuration/file/
http:
  routers:
    chatGPT:
      # md5(b'ChatGPT').digest()[:8].hex()
      rule: "Host(`external.hdcjh.xyz`) && PathPrefix(`/62239e6c0f995ae1`)"
      service: chatGPT
      middlewares:
        - chatGPT
      tls:
        certResolver: production
        domains:
          - main: "hdcjh.xyz"
            sans:
              - "*.hdcjh.xyz"
  services:
    chatGPT:
      loadBalancer:
        servers:
          - url: https://api.openai.com
        passHostHeader: false
  middlewares:
    chatGPT:
      stripPrefix:
        # md5(b'ChatGPT').digest()[:8].hex()
        prefixes:
          - "/62239e6c0f995ae1"
        forceSlash: false
```

3. 编写 docker compose，用于启动 traefik
copy 下面的代码到自己的 docker-compose.yml 文件：
```
version: '3.9'

services:
  reverse-proxy:
    image: traefik:v2.9
    container_name: traefik
    command:
      - --api.insecure=true
      - --providers.docker=true
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/log/access.log:/var/log/access.log
      - /etc/traefik:/etc/traefik
      - traefik-ssl-certs:/ssl-certs

  whoami:
    image: traefik/whoami
    labels:
      - "traefik.http.routers.whoami.rule=Host(`whoami.docker.localhost`)"

networks:
  default:
    external:
      name: traefik

volumes:
  traefik-ssl-certs:
    driver: local
```
4. 手动添加网络，运行下面的命令即可
`docker network create traefik --driver bridge`
5. 启动代理
`docker compose up -d`
6. 去 8080 端口查看 traefik 执行情况
例如在我这里就是直接访问 https://external.hdcjh.xyz:8080 这个链接。
可以看到 traefik 反向代理运行良好，然后就可以直接使用啦～
<img width="1439" alt="image" src="https://user-images.githubusercontent.com/45847340/223733268-34092b82-5e7b-4a39-a8c1-abcd350e89a5.png">

### 常见问题
* 别人访问了我的 Traefik 面板怎么办？
  * 首先，因为使用了 Cloudflare 代理，第三者不知道服务器的真实 IP ，所以压根就无法访问面板端口。
  * 其次，可以使用 Traefik 的 BasicAuth 中间件实现登录操作，只需要给 traefik 的 container 添加相应的 label 即可。
* 有人 DDos 攻击我的服务器怎么办？
  * 首先，Cloudflare 可以开启 DDos 防护
  * 其次，Traefik RateLimit 中间件可以实现限流，我这里设置的是每10秒最多100次请求

其他问题请留言，我会一一回答。
