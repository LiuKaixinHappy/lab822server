# 822 lab 接口设计

## 图像处理（imgproc）

分为「实验」和「学习」两个部分



### 实验

#### 1. 获取操作列表

- URL：/imgproc/lab/

- Method：GET

- Response：

  - 成功

    ```javascript
    {
        result: 1,
        message: [
            {
                type: 'string',
                subType: [
                    {
                        name: 'string',
                        code: 'string',
                        params: [
                            {
                                name: 'string',
                                pName: 'string',
                                limit: 'string',
                                type: 'string',
                                value: []
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

    说明: 

    1. message中的type代表图像处理操作的大类型，中文简体，如：图像平滑、边缘检测、角点检测、形态学处理等
    2. message中的subType代表大类型type下包含的小算法，如type为"图像平滑"，则subType为"高斯平滑"、"均值平滑"等，中文简体。
    3. subType中的name为小算法的中文名称
    4. subType中的code为操作代码，唯一，**从100起编号，每一个大类型+100，小算法+1**，如图像平滑为100，则高斯平滑为101，均值为102，以此类推，边缘检测类型为200，则所包含小算法在[200, 300)间。
    5. subType中的params为算法所需要传入的参数，name为参数中文名称，pName为参数英文名称，采用**驼峰法命名**，limit为参数限制，如奇数、整数等，type为参数输入类型，如输入框还是下拉列表，如果是下拉列表，则在value中写出下拉列表中的内容，中文简体。

    约定：

    1. limit目前包含：奇数约束`odd`，大于约束`>`，小于约束`<`，整数约束`int`，当多个约束并存时，使用空格分开，如`odd >1 <100`代表大于1小于100的奇数
    2. type目前包含：输入框`input`， 下拉列表`select`

  - 失败

    ```javascript
    {
        result: 0,
        message: 'string'
    }
    ```

#### 2. 处理图像

- URL：/imgproc/lab/

- Method: POST

- Request:

  ```javascript
  {
      operations: [
          {
              code: 'string',
              params: {}
          }
      ]
      image: 'string'
  }
  ```

  说明：

  1. code为图像操作编码
  2. params为操作的pName和用户输入/选择的value值，如`{kSize: 5, sigmaX:51}`，**如果是下拉选择，则value为用户选择的参数值的索引**
  3. image为图像base64编码
  4. 虽然接口设计的operations为数组，一次可进行多个操作，但目前平台约定一次只能进行一个操作

- Response:

  - 成功：

    ```javascript
    {
        result: 1,
        message: {
            image: 'string',
            log: {
                str: 'string',
                img: 'string'
            }
        }
    }
    ```

    说明：

    1. image为处理完成的图片base64编码
    2. log为需要协同图片一起返回前端的信息，str是文字信息，img是图片信息（base64编码），比如自动阈值分割，处理完后还期望给用户返回自动找出的最佳阈值是多少，则可以记录在str里，如果还希望将图像的直方图呈现给用户，则放在img中

  - 失败：

    ```javascript
    {
        result: 0,
        message: 'string'
    }
    ```
    
# Pull Request 
欢迎大家一起完善平台，如果平台的算法不足以满足你的实验需求，可以Pull Request的方式添加自己的算法，也可以解决issue中的问题。

下面是PR的一些要求：
- 请保持整体代码风格统一
    - 变量名与方法名小写+下划线
    - 常量名大写+下划线
    - 类名每个单词首字母大写
    - 方法之前空两行
    
  NOTE：最好用pycharm，严格遵守提示，自动格式化代码后再提交
  
- 每类图像处理方法内部由责任链模式编写,添加新的图像处理方法请参考[这里](https://www.jianshu.com/p/9c86725058b8)，
- 数据库添加目前尚未完成，所以有需要向数据库添加字段的，联系QQ或微信644306737，备注server-gitPR+姓名
