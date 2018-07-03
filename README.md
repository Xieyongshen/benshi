# benshi

## 项目介绍
这是由本事创业团队开发的初期产品微信小程序版本


### 组织结构

``` lua
benshi
├── doc -- 项目文档文件夹：包括需求、设计、开发进度等文档
|
├── myproject -- 项目文件夹
|         |--dist  -- 生成的可调式代码文件（非源代码）
|         |
|         |--src  --源代码文件夹
|             ├── components  -- 模块化组件文件夹
|             |       └── group.wepy -- 组件文件
|             |
|             ├── app.wpy  -- app项目配置文件
|             └── pages -- 页面集合文件夹
|                   └── page.wepy -- 页面文件
| 
└── README.md   -- readme文件
```

### 技术选型

#### 后端技术:
Django


#### 前端技术:
技术 | 名称 | 官网
----|------|----
wepy | 微信小程序官方框架  | [https://tencent.github.io/wepy/document.html#/](https://tencent.github.io/wepy/document.html#/)
Vue.js | 渐进式javascript框架  | [https://cn.vuejs.org/](https://cn.vuejs.org/)

#### 模块介绍

> demo

待完善


### 框架规范约定

约定优于配置(convention over configuration)，此框架约定了很多编程规范，下面一一列举：

```


- 类名：首字母大写驼峰规则；方法名：首字母小写驼峰规则；常量：全大写；变量：首字母小写驼峰规则，尽量非缩写

- 提交说明：提交说明尽量统一，如[init]、[add]、[delete]、[update]等加上message；如需要回滚请注意备份

- util类，需要在以`util`的包下，并以`Util`结尾，如`JsonUtil



```

### 软件架构
软件架构说明


### 安装教程

1. xxxx
2. xxxx
3. xxxx

### 使用说明

1. xxxx
2. xxxx
3. xxxx

### 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

