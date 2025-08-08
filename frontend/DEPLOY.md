# 前端部署说明

## 快速开始

### 1. 生产环境部署

```bash
# 构建并启动生产环境
docker-compose up -d

# 访问应用
http://localhost
```

### 2. 开发环境部署

```bash
# 启动开发环境
docker-compose --profile dev up -d

# 访问开发环境
http://localhost:5173
```

### 3. 单独使用 Docker 命令

```bash
# 构建生产镜像
docker build -t foodbasket-frontend .

# 运行生产容器
docker run -d -p 80:80 --name foodbasket-frontend foodbasket-frontend

# 构建开发镜像
docker build -f Dockerfile.dev -t foodbasket-frontend-dev .

# 运行开发容器
docker run -d -p 5173:5173 -v $(pwd):/app --name foodbasket-frontend-dev foodbasket-frontend-dev
```

## 配置说明

### 环境变量

- `NODE_ENV`: 环境模式 (development/production)

### 端口配置

- 生产环境: 80
- 开发环境: 5173

### 健康检查

访问 `http://localhost/health` 检查服务状态

## 注意事项

1. **API 代理配置**: 如果需要连接后端 API，请修改 `nginx.conf` 中的代理配置
2. **HTTPS 配置**: 生产环境建议配置 HTTPS，可以在 nginx.conf 中添加 SSL 配置
3. **域名配置**: 修改 nginx.conf 中的 `server_name` 为实际域名
4. **缓存策略**: 静态资源已配置长期缓存，更新时需要清除缓存

## 故障排除

### 常见问题

1. **端口冲突**: 如果 80 端口被占用，修改 docker-compose.yml 中的端口映射
2. **构建失败**: 检查 Node.js 版本和依赖包版本
3. **路由问题**: 确保 nginx.conf 中的 history 模式配置正确

### 日志查看

```bash
# 查看容器日志
docker logs foodbasket-frontend

# 查看 nginx 日志
docker exec foodbasket-frontend tail -f /var/log/nginx/access.log
docker exec foodbasket-frontend tail -f /var/log/nginx/error.log
```

## 性能优化

1. **镜像大小**: 使用多阶段构建减小镜像体积
2. **缓存策略**: 静态资源配置长期缓存
3. **Gzip 压缩**: 已启用 Gzip 压缩
4. **安全头**: 配置了基本的安全响应头
