# 高速、免费的 ChatGPT 代理节点

体验机器人可直接加QQ: [775762961](https://qm.qq.com/cgi-bin/qm/qr?k=q3jn9yXYFYjeSkiMrUsQMosq1QM9Ges7&noverify=0&personal_qrcode_source=4) (ps: 机器人发言频繁被封了，可以直接加群：752372415)

## 使用方法
### 1. 使用 curl 访问
#### 1.1 使用代理节点的 Token 进行访问（代理Token在下面有申请方法）
注意⚠️：该 API 仅用于测试，有限流。
```sh
curl -X POST --location "https://external.hdcjh.xyz/gateway/transmit-openai/v1/chat/completions" \
    -H "Authorization: Bearer 806601c981dec75e3e69b9984cb155b9" \
    -H "Content-Type: application/json" \
    -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello!"}]}'
```

#### 1.2 使用 OpenAI 的 API KEY 进行访问
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

#### 2.1 使用代理节点的 Token 进行访问（代理Token在下面有申请方法）

注意⚠️：该 API 仅用于测试，有限流。
```py
import openai

# 这里记得修改成自己的 API KEY
openai.api_key = '806601c981dec75e3e69b9984cb155b9'
openai.api_base = 'https://external.hdcjh.xyz/gateway/transmit-openai/v1'

# 一个调用的小例子
messages = [{"role": "user", "content": "老公，你说句话呀"}]
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages,
  temperature=0.9,
  max_tokens=1024,
  n=1,
)
response = completion.choices[0]
print(response['message']['content'])
```

#### 2.2 使用 OpenAI 的 API KEY 进行访问
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
                temperature=0.9,
                max_tokens=1024,
                n=1,
            )
response = completion.choices[0]
print(response['message']['content'])
```

### 3. 免费的 API Token


[点击这里](https://qm.qq.com/cgi-bin/qm/qr?k=soc5WAKNEbftNsX1uX39SYm_jHNI6Bu7&authKey=cfpBHNk+pKQ5Mi/hbqs64ivQya/BjTeSKD3PwQ4eCuG7cDiKs5SyzLVnfFP2K4Qv&noverify=0)或者搜索加入 QQ 群：752372415

进群加机器人好友后，会**自动回复免费的代理 Token**，限流为 500 次每周且 100 次每天。

**用的舒服的话，不妨点个 star~**
<table border="0" width="10%">
  <tr>
    <td><img src="https://img1.github.io/tmp/1.jpg" height="80" width="82"></td>
    <td><img src="https://img1.github.io/tmp/2.jpg" height="80" width="82"></td>
    <td><img src="https://img1.github.io/tmp/3.jpg" height="80" width="82"></td>
  </tr>
  <tr>
    <td><img src="https://img1.github.io/tmp/4.jpg" height="80" width="82"></td>
    <td><img src="https://img.shields.io/github/stars/dusty-cjh/free-proxy.svg?style=social"></td>
    <td><img src="https://img1.github.io/tmp/6.jpg" height="82" width="82"></td>
  </tr>
   <tr>
    <td><img src="https://img1.github.io/tmp/7.jpg" height="82" width="82"></td>
    <td><img src="https://img1.github.io/tmp/8.jpg" height="82" width="82"></td>
    <td><img src="https://img1.github.io/tmp/9.jpg" height="82" width="82"></td>
  </tr>
</table>

### 4. 关于安全
* 本项目为纯 API 转发，并不会以任何方式保存用户的 API KEY
* 任何代理都是有窃听用户隐私的能力的，区别只在于提供者想不想
* 如果有担心 API KEY 泄漏的同学，可以进群找机器人直接拿免费的KEY，或者自行搭建服务器，下面是具体 ChatGPT 代理的搭建方法，欢迎小伙伴们一起讨论～

## 代理服务器搭建方法
### 原理
使用 Traefik 作为反向代理，把关于 ChatGPT 的请求转发到 openai 即可。

关于代理 Token：
* 代理 Token 就是在请求 OpenAI 的时候，Traefik 先检测代理 token 是否有效，如果有效则替换为 OpenAI 的 API KEY，最后再转发到 OpenAI。

关于限流：
* 第一层限流在 Traefik，直接配置插件
* 第二层限流在代码里，使用 Redis 存储每个代理 Token 在一段时间范围内的请求次数，超过限制则返回错误。
  * 更进一步可以考虑批量获取请求次数，例如限流为 10000/hour，那么就可以每次取 100 个请求次数，等本地的 Redis token 消耗光了以后再重新获取，以提升整体性能。缺点是可能产生限流误差，比如在这个例子中最大的误差就是 10%
  * 更进一步也可以考虑在协程中使用信号去控制请求是否返回，主请求通路和验证同时进行，以降低延迟。缺点是可能会比较费 Token。


### 前期准备
* 买一个国外的 VPS 或者**白嫖大厂的 VPS**
  * 大厂基本每年都有打骨折的活动，下面链接里是相关的 2023 年的一些活动链接，还有一些本身就很便宜的直接去官网买就行。
  * AWS / 
  * [Azure](https://91ai.net/thread-1139144-1-1.html) / 
  * [Digital Ocean](https://walixz.com/digitalocean-coupon.html) / 
  * [甲骨文免费服务器](https://www.oracle.com/cn/cloud/free/) / 
  * [hosteons](https://hosteons.com/)
* 申请免费的 Redis 存储
    * 可以直接去 [redis lab](https://app.redislabs.com/#/databases) 申请，注册就送永久 30MB 免费存储，对于小网站来说 30MB 绝对够用了。
* 为 VPS 申请域名、证书
    * 直接使用 Cloudflare 托管域名，然后在 Cloudflare 中一键申请，或者也可以去 Let's Encrypt 申请短效证书。
* 在 VPS 上安装 docker
    * 直接看[官网文档](https://docs.docker.com/get-docker/)
* 使用 docker 安装 traefik
    * 也是直接看[官方文档](https://doc.traefik.io/traefik/getting-started/quick-start/)按步骤来即可

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
