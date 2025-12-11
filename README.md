# PPTX to JPEG Converter Service

一个基于FastAPI和Docker的PPTX转JPEG图片服务，可以将PowerPoint演示文稿的每一页转换为独立的JPEG图片。

## 功能特性

- 🚀 基于FastAPI的高性能Web服务
- 🐳 Docker容器化部署，环境一致性保证
- 📄 支持PPTX和PPT格式文件
- 🖼️ 将每页幻灯片转换为高质量JPEG图片
- 🔗 返回每张图片的URL地址，便于直接使用
- 🔧 自动清理临时文件
- 📊 健康检查端点
- 🌐 支持中文文件名和特殊字符处理

## 技术架构

### 转换流程
1. **PPTX → PDF**: 使用LibreOffice的`soffice`命令
2. **PDF → JPEG**: 使用ImageMagick的`convert`命令
3. **存储**: 将JPEG图片保存到静态文件目录，使用随机ID+序号命名
4. **返回**: 返回每张图片的URL地址列表

### 技术栈
- **后端**: FastAPI + Python 3
- **转换工具**: LibreOffice + ImageMagick + Ghostscript
- **容器化**: Docker + Docker Compose
- **基础镜像**: Ubuntu 22.04

## 项目结构

```
.
├── docker-compose.yml    # Docker Compose配置文件
├── Dockerfile           # Docker镜像构建文件
├── requirements.txt     # Python依赖包
├── main.py             # FastAPI应用主文件
└── README.md           # 项目说明文档
```

## 快速开始

### 1. 构建和启动服务

```bash
# 构建Docker镜像
docker compose build

# 启动服务
docker compose up -d

# 查看服务状态
docker compose ps

# 查看服务日志
docker compose logs -f
```

### 2. 验证服务运行

访问以下URL验证服务是否正常运行：

- **健康检查**: http://localhost:8131/health
- **API文档**: http://localhost:8131/docs
- **根路径**: http://localhost:8131/

### 3. 使用API转换文件

#### 使用curl命令

```bash
curl -X POST "http://localhost:8131/convert/pptx-to-jpeg/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_presentation.pptx"
```

**响应示例:**
```json
{
  "status": "success",
  "message": "Successfully converted 5 slides",
  "slide_count": 5,
  "images": [
    "/static/a1b2c3d4_001.jpg",
    "/static/a1b2c3d4_002.jpg",
    "/static/a1b2c3d4_003.jpg",
    "/static/a1b2c3d4_004.jpg",
    "/static/a1b2c3d4_005.jpg"
  ],
  "original_filename": "your_presentation.pptx",
  "note": "Images will be automatically cleaned up after 1 hour"
}
```

#### 使用Python requests

```python
import requests

url = "http://localhost:8131/convert/pptx-to-jpeg/"
files = {"file": open("your_presentation.pptx", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print(f"转换成功！共 {result['slide_count']} 张图片")
    print("图片URLs:")
    for i, image_url in enumerate(result['images'], 1):
        full_url = f"http://localhost:8131{image_url}"
        print(f"  {i}. {full_url}")
else:
    print(f"转换失败: {response.text}")
```

## API接口说明

### POST /convert/pptx-to-jpeg/

将PPTX/PPT文件转换为JPEG图片并返回URL列表。

**请求参数:**
- `file`: 上传的PPTX或PPT文件 (multipart/form-data)

**响应:**
- 成功: 返回JSON格式的图片URL列表 (application/json)
- 失败: 返回错误信息 (application/json)

**响应字段:**
- `status`: 转换状态 ("success" 或 "error")
- `message`: 状态消息
- `slide_count`: 幻灯片数量
- `images`: 图片URL数组
- `original_filename`: 原始文件名
- `note`: 额外说明信息

**状态码:**
- `200`: 转换成功
- `400`: 文件格式不支持或未上传文件
- `500`: 转换过程出错

## 图片访问方式

转换完成后，你可以直接通过以下URL访问每张图片：

- `http://localhost:8131/static/a1b2c3d4_001.jpg`
- `http://localhost:8131/static/a1b2c3d4_002.jpg`
- `http://localhost:8131/static/a1b2c3d4_003.jpg`
- ...

**文件名格式**: `{随机ID}_{序号}.jpg`
- 随机ID: 8位十六进制字符串，确保唯一性
- 序号: 3位数字，从001开始递增

### GET /static/{filename}

获取转换后的图片文件。

**路径参数:**
- `filename`: 图片文件名 (例如: `a1b2c3d4_001.jpg`)

**响应:**
- 成功: 返回图片文件流 (image/jpeg)
- 失败: 返回404错误

### GET /health

健康检查端点，用于监控服务状态。

**响应示例:**
```json
{
  "status": "healthy",
  "service": "pptx-to-jpeg-converter"
}
```

## 配置说明

### 图片质量设置

在`main.py`中可以调整以下参数：

```python
# ImageMagick转换参数
cmd = [
    "convert",
    "-density", "150",    # DPI分辨率 (默认150)
    "-quality", "80",     # JPEG压缩质量 (默认80)
    str(input_pdf_path),
    str(output_jpeg_pattern)
]
```

### 超时设置

转换过程有5分钟超时限制，可在`main.py`中调整：

```python
timeout=300  # 5分钟超时
```

## 故障排除

### 常见问题

1. **ImageMagick策略错误**
   - 错误信息: `not authorized`
   - 解决方案: Dockerfile中已自动修复ImageMagick策略

2. **LibreOffice转换失败**
   - 检查文件格式是否支持
   - 确认文件未损坏
   - 查看容器日志获取详细错误信息

3. **内存不足**
   - 大文件转换可能需要更多内存
   - 考虑增加Docker容器内存限制

4. **中文文件名编码错误**
   - 错误信息: `'latin-1' codec can't encode characters`
   - 解决方案: 服务已自动处理中文文件名，将特殊字符替换为安全字符
   - 如果仍有问题，建议重命名文件为英文名称

### 查看日志

```bash
# 查看实时日志
docker compose logs -f pptx_converter_service

# 查看最近100行日志
docker compose logs --tail=100 pptx_converter_service
```

## 开发说明

### 本地开发

```bash
# 安装Python依赖
pip install -r requirements.txt

# 运行开发服务器
python main.py
```

### 构建优化

- 使用多阶段构建减少镜像大小
- 添加健康检查确保服务可用性
- 配置重启策略提高服务稳定性

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！
