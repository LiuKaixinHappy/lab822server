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
    message: [{type: '', subType: [{name:'', code: '', params:[]},{name: '', code: '', id:},...]}, {type: '', subType: [ {name: '', code: '', id:},...]}]
  }
  - 失败：{
    result: 0,
    message: ''
  }

**message详情**
```JAVASCRIPT
[{
  type: '图像平滑',
  subType: [
  {
      name: '高斯平滑',
      code: '101',
      params: [
      {
          type:'input'(PS:必须奇数),
          name:'卷积核宽',
          pName: 'kSizeW'
      },
      {
          type:'input'(PS:必须奇数),
          name:'卷积核高',
          pName: 'kSizeH'
      },
      {
          type:'input',
          name:'水平方向标准差',
          pName: 'sigmaX'
      },
      {
          type:'input',
          name:'垂直方向标准差',
          pName: 'sigmaY'
      },
      {
          type:'choice',
          name:'边界扩充方式',
          value:['边界复制','常数扩充','反射扩充','边界为中心反射扩充','平铺扩充'],
          pName: 'borderType'
      }]
  },
  {
     name: '均值平滑',
     code: '102'
     params: [
     {
         type:'input',
         name:'算子宽',
         pName: 'kSizeW'
     },
     {
         type:'input',
         name:'算子高',
         pName: 'kSizeH'
     },
     {
         type:'input',
         name:'锚点'(PS：检验坐标在矩阵范围内),
         pName: 'anchor'
     },
     {
         type:'choice',
         name:'边界扩充方式',
         value:['边界复制','常数扩充','反射扩充','边界为中心反射扩充','平铺扩充']
         pName: 'borderType'
     }
     ]
  },
  {
      name: '中值平滑',
      code: '103',
      params: [
      {
          type:'input',
          name:'窗口大小'(PS:大于1),
          pName: 'kSize'
      }
      ]
  },
  {
      name: '双边滤波',
      code: '104',
      params: [
      {
          type:'input',
          name:'权重模板宽',
          pName: 'kSizeW'
      },
      {
          type:'input',
          name:'sigma color',
          pName: 'sigma color'
      },
      {
          type:'input',
          name:'sigma space',
          pName: 'sigma space'
      }
      ]
  },
  {
      name: '联合双边滤波',
      code: '105',
      params: [
      {
          type:'input',(PS:奇数)
          name:'权重模板宽',
          pName: 'kSizeW'
      },
      {
          type:'input',(PS:奇数)
          name:'权重模板高',
          pName: 'kSizeH'
      },
      {
          type:'input',
          name:'空间距离权重模板标准差',
          pName: 'sigma_g'
      },
      {
          type:'input',
          name:'相似性权重模板标准差',
          pName: 'sigma_d'
      },
      {
          type:'choice',
          name:'边界扩充方式',
          value:['边界复制','常数扩充','反射扩充','边界为中心反射扩充','平铺扩充']
          pName: 'borderType'
      }]
  }]
},
{
    type:'边缘检测',
    subType:[{}]
},
{
    type:'轮廓提取',
    subType:[{}]
}]
```
#### 请求图像处理
- URL： /imgproc/lab/
- Method: POST
- Request:
  - {
    operation: ['','',..],   // 字符串数组, 传操作的code
    image: {name: '', content: ''},   // 如果是新图，名称为「用户id-年月日时分秒.jpg/.png」，content为图片，如果是在上次操作基础上继续，则name为上次图片的name，content为空，暂时不做用户模块，只有我，id记为1就好
  }

- Response：
  - 成功：{
    result:1,
    message:{imgUrl:'', imgName:''}
  }
  - 失败：{
    result:0,
    message: ''
  }

NOTE：新图的名称是由客户端取的，处理后的图片名称由服务器端取，每次处理后服务器端会返回给客户端，客户端下一次请求则带着此名称
```JAVASCRIPT

// 第一次
request:
{
    operation: [{
        code:'101',
        param:[{
            pName: (上述参数的pName),
            pValue: 值
        }]
    }],
    image: {
        name: 'userid-20181002132257.jpg',
        content: 'xxx'
    }
}
response:
{
    result:1,
    message:{
        imgUrl:'http://xxxx/xxx/xxx/userid-20181002132257-101.jpg',
        imgName:'userid-20181002132257-101.jpg'
    }
}
// 基于上一次操作
request:
{
    operation: [{
        code:'101',
        param:[{
            pName: (上述参数的pName),
            pValue: 值
        }]
    }],
    image: {
        name: 'userid-20181002132257-101.jpg',(基于哪一次就用哪一次的名字)
        content: ''(空)
    }
}
response:
{
    result:1,
    message:{
        imgUrl:'http://xxxx/xxx/xxx/userid-20181002132257-101-101.jpg',
        imgName:'userid-20181002132257-101-101.jpg'
    }
}
```

### 学习
