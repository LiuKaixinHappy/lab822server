# 822LAB 服务器端 接口文档

url: http://

port: 8080

## 图像处理

### 实验

#### 获取操作列表
- URL： /imgproc/lab/
- Method: GET
- Response:
  - 成功：{
    result: 1,
    message: [{type: '图像平滑', subType: [{name:'高斯平滑', code: 'GaussBlur', id:},{name: '', code: '', id:},...]}, {type: '', subType: [ {name: '', code: '', id:},...]}]
  }
  - 失败：{
    result: 0,
    message: ''
  }

#### 请求图像处理
- URL： /imgproc/lab/
- Method: POST
- Request:
  - {
    operation: ['GaussBlur','',..],   // 字符串数组, 传操作的code
    image: {name: '', content: ''},   // 如果是新图，名称为「用户id-年月日时分秒.jpg/.png」，content为图片，如果是在上次操作基础上继续，则name为上次图片的name，content为空，暂时不做用户模块，只有我，id记为1就好
  }
- Response：
  - 成功：{
    result:1,
    message:{imaUrl:'', imgName:''}
  }
  - 失败：{
    result:0,
    message: ''
  }

NOTE：新图的名称是由客户端取的，处理后的图片名称由服务器端取，每次处理后服务器端会返回给客户端，客户端下一次请求则带着此名称

### 学习
