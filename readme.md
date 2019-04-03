# CookiesPool
## Install
1. Install redis
```bash
docker run -d -p 127.0.0.1:6179:6179 redis
docker ps -a 
```
*Take note the redis container info and write it in the cookiespool/config.py*
  
  
2. Build the image 
```bash
git clone -b docker https://github.com/Hiram711/CookiesPool.git
cd CookiesPool
docker build  . -t cookiepool:generate
```

3. Run
```bash
docker run -d --name cookiepool_server --link your-redis-container cookiepool:generate sh -c 'uwsgi --http :5000 --wsgi-file cookiespool/api.py --callable app  --processes 4 --threads 2'
docker run -d --name cookiepool_generator --link your-redis-container cookiepool:generate
```