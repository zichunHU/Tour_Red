# Tour - 旅游应用

一个用于发现和管理旅游景点和路线的全栈 Web 应用程序。该项目后端采用 Python Flask 提供 REST API，前端则使用 Vue.js 构建用户界面。

## 核心功能

-   **景点管理**: 查看、创建、编辑和删除旅游景点。
-   **路线规划**: 创建和管理由多个景点组成的旅游路线。
-   **用户认证**: 基本的用户登录和注册功能。
-   **个性化推荐**: 为用户提供个性化的内容。
-   **富文本内容**: 支持为景点详情上传富文本和图片。
-   **后台管理面板**: 一个用于管理网站内容的专用界面。

## 技术栈

-   **后端**:
    -   Python
    -   Flask
    -   Flask-Cors
-   **前端**:
    -   Vue.js 3
    -   Vite
    -   Vue Router
    -   Tiptap (用于富文本编辑)
-   **数据库**:
    -   基于文件的 JSON 存储。

## 项目结构

该项目主要分为两个目录：

-   `./backend/`: 包含 Flask API 服务器、应用逻辑和数据文件。
-   `./frontend/`: 包含 Vue.js 客户端应用程序、组件和视图。

## 环境配置与安装

### 先决条件

-   Python 3.8+ 和 `pip`
-   Node.js 16+ 和 `npm`

### 后端设置

1.  **进入后端目录:**
    ```bash
    cd backend
    ```

2.  **创建并激活虚拟环境:**
    ```bash
    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **安装所需的 Python 包:**
    ```bash
    pip install -r requirements.txt
    ```

### 前端设置

1.  **进入前端目录:**
    ```bash
    cd frontend
    ```

2.  **安装所需的 npm 包:**
    ```bash
    npm install
    ```

## 运行应用

1.  **启动后端服务器:**
    -   确保您位于 `backend` 目录，并已激活虚拟环境。
    -   运行应用:
        ```bash
        python run.py
        ```
    -   后端服务器将启动于 `http://127.0.0.1:5000`。

2.  **启动前端开发服务器:**
    -   确保您位于 `frontend` 目录。
    -   运行开发服务器:
        ```bash
        npm run dev
        ```
    -   前端应用将在终端所示的地址（通常是 `http://localhost:5173`）上可用。

# 项目架构概述

本文档旨在详细介绍 "Tour" 项目的整体架构，帮助新成员快速理解项目结构、技术选型和数据流程，以便于后续的开发和维护。

## 1. 概述

本项目采用**前后端分离**的客户端-服务器（Client-Server）架构模式。

-   **前端 (Client)**：一个基于 **Vue.js** 的单页面应用 (SPA)，负责用户界面的渲染和交互逻辑。它通过 HTTP 请求与后端 API 进行通信。
-   **后端 (Server)**：一个基于 **Python Flask** 的 RESTful API 服务器，负责处理业务逻辑、数据操作，并向前端提供标准化的 JSON 数据接口。


## 2. 目录结构

项目的核心代码位于两个主目录中：

-   `./backend/`：存放所有后端 Flask 应用相关的代码。
-   `./frontend/`：存放所有前端 Vue.js 应用相关的代码。

```
Tour/
├── backend/                # 后端应用
│   ├── app/                # Flask 应用核心模块
│   │   ├── __init__.py     # 应用工厂，用于创建和配置 Flask app
│   │   ├── attractions_bp.py # 景点相关的 API 蓝图
│   │   ├── auth_bp.py      # 用户认证相关的 API 蓝图
│   │   ├── routes_bp.py    # 路线相关的 API 蓝图
│   │   └── data_loader.py  # 数据加载器，从 JSON 文件读取数据
│   ├── data/               # 数据存储目录
│   │   ├── attractions/    # 景点数据和图片
│   │   ├── routes.json     # 路线数据
│   │   └── users.json      # 用户数据
│   ├── run.py              # 后端应用的启动脚本
│   └── requirements.txt    # Python 依赖列表
│
└── frontend/               # 前端应用
    ├── src/
    │   ├── components/     # 可复用的 Vue 组件
    │   ├── views/          # 页面级视图组件
    │   ├── router/         # 路由配置
    │   ├── App.vue         # 根组件
    │   └── main.js         # 前端应用入口文件
    ├── index.html          # SPA 的主 HTML 文件
    ├── package.json        # Node.js 依赖和脚本配置
    └── vite.config.js      # Vite 构建工具配置
```

## 3. 后端架构 (Flask)

后端采用模块化的设计思路，易于扩展和维护。

### 应用工厂模式

-   应用在 `backend/app/__init__.py` 文件中的 `create_app()` 函数内被创建和配置。这种**工厂模式**有助于在不同配置下（如开发、测试、生产）创建应用实例，使代码更具灵活性。

### 蓝图 (Blueprint)

-   为了更好地组织代码，API 按功能被拆分到不同的**蓝图**文件中。
-   每个 `_bp.py` 文件代表一个功能模块，其中定义了该模块相关的 API 路由。
-   蓝图在 `create_app()` 函数中被注册到主应用上，并统一添加了 URL 前缀，使得 API 更具层次感。
    -   **景点蓝图**: 注册在 `/api/attractions`
    -   **路线蓝图**: 注册在 `/api/routes`
    -   **认证蓝图**: 注册在 `/api`

### 数据层

-   项目当前的数据存储在 `backend/data/` 目录下的 **JSON 文件**中。
-   `backend/app/data_loader.py` 模块负责从这些 JSON 文件中读取和解析数据，供各个蓝图调用。
-   **注意**：这是一个简化的数据持久化方案。对于生产环境，建议将数据迁移到更稳定的数据库系统（如 PostgreSQL 或 MySQL）。

## 4. 前端架构 (Vue.js)

前端是一个现代化的单页面应用，构建于 Vue.js 生态系统之上。

### 构建工具

-   项目使用 **Vite** 作为构建工具，提供极速的冷启动和热模块重载 (HMR)，显著提升了开发体验。

### 应用入口

-   `frontend/src/main.js` 是应用的入口文件。它负责初始化 Vue 实例、挂载路由（Vue Router）和根组件 (`App.vue`)。

### 路由

-   `frontend/src/router/index.js` 文件负责配置应用的所有页面路由。
-   它使用 **Vue Router** 库，将不同的 URL 路径映射到对应的视图组件上。

### 组件结构

-   `frontend/src/views/`：存放**页面级组件**。每个组件对应一个完整的页面（如 `HomePage.vue`, `AttractionListPage.vue`）。
-   `frontend/src/components/`：存放**可复用的 UI 组件**（如 `RichTextEditor.vue`）。这些组件可以在不同的视图中被多次使用，提高了代码的复用性。

### API 通信

-   前端通过浏览器内置的 `fetch` API 或其他 HTTP 客户端（如 `axios`）与后端 API 进行异步通信。
-   为了处理跨域问题，后端 Flask 应用已通过 `Flask-Cors` 插件开启了跨域资源共享 (CORS)。

## 5. 数据流示例 (获取景点列表)

以下是一个典型的端到端数据交互流程：

1.  **用户操作**：用户在浏览器中访问景点列表页面。
2.  **前端路由**：Vue Router 匹配到 `/attractions` 路径，渲染 `AttractionListPage.vue` 视图组件。
3.  **发起请求**：在 `AttractionListPage.vue` 的 `onMounted` 或相关生命周期钩子中，通过 `fetch` 向后端 `http://127.0.0.1:5000/api/attractions` 发送一个 GET 请求。
4.  **后端处理**：
    -   Flask 应用接收到请求，并将其路由到 `attractions_bp` 蓝图中对应的处理函数。
    -   该函数调用 `data_loader` 从 `backend/data/attractions/` 目录中读取所有景点的数据。
    -   后端将数据整理成 JSON 格式，并将其作为 HTTP 响应返回。
5.  **前端渲染**：
    -   `AttractionListPage.vue` 接收到包含景点数据的 JSON 响应。
    -   组件将数据保存到其内部状态中。
    -   Vue 的响应式系统自动更新 DOM，将景点列表渲染到页面上。


## 待办事项 (TODO)

-   [ ] **智能推荐**: 在首页根据季节、位置和热度实现动态的个性化推荐。
-   [ ] **AI 辅助搜索**: 添加 AI 助手，以支持通过自然语言对话获取定制推荐（例如“我想了解工人运动历史”）。
-   [ ] **高级筛选**: 为景点和路线列表增加多维度筛选功能（如按区域、主题、评分等）。
-   [ ] **交互式路线定制**: 开发“个性化定制”页面，允许用户通过选择兴趣标签和在地图上勾选景点来创建自己的路线。
-   [ ] **关键词串联路线**: 实现“关键词串联”功能，基于历史主题或事件生成有逻辑的参观路线（例如，搜索“五卅运动”可生成相关景点的路线）。
-   [ ] **多模态内容**: 在景点和路线详情页中集成音频和视频内容。
-   [ ] **社区功能**: 增加“红色记忆”板块，供用户分享评论、评分和感想。
-   [ ] **数据迁移**: 将数据从基于文件的 JSON 迁移到更健壮的数据库系统（如 PostgreSQL, SQLite）。