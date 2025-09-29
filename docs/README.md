# Quantum Studio - 清华大学交叉信息研究院量子计算课题组网站

## 项目简介
这是为清华大学交叉信息研究院量子计算课题组打造的官方网站，作为课题组学术成果展示、成员介绍、研究方向推广的核心线上平台。

## 目录结构
```
Quantum Studio/
├── css/
│   └── style.css        # 样式文件
├── images/              # 图像文件夹（需要用户自行添加）
├── js/
│   ├── main.js          # 主要JavaScript功能
│   ├── particles.js     # 量子态粒子效果
│   ├── carousel.js      # 轮播功能
│   └── filter.js        # 学术成果筛选功能
├── index.html           # 主页面
└── README.md            # 项目说明文档
```

## 图像文件准备
为了确保网站正常显示，需要在`images/`文件夹中添加以下图像文件（尺寸建议）：

1. **研究成果图片**
   - `research1.jpg` (600x400px)
   - `research2.jpg` (600x400px)
   - `research3.jpg` (600x400px)

2. **实验室环境图片**
   - `lab1.jpg` (1200x800px)
   - `lab2.jpg` (1200x800px)
   - `lab3.jpg` (1200x800px)
   - `lab4.jpg` (1200x800px)
   - `lab5.jpg` (1200x800px)

3. **团队成员图片**
   - `leader.jpg` (400x400px) - 负责人照片
   - `researcher1.jpg` (300x300px)
   - `researcher2.jpg` (300x300px)
   - `researcher3.jpg` (300x300px)
   - `researcher4.jpg` (300x300px)
   - `researcher5.jpg` (300x300px)
   - `researcher6.jpg` (300x300px)
   - `researcher7.jpg` (300x300px)
   - `researcher8.jpg` (300x300px)

## 功能特点

1. **响应式设计**
   - 兼容桌面端(≥1920px)、平板(≥768px)、移动端(≥320px)
   - 导航栏滚动时背景透明度变化

2. **视觉效果**
   - 量子态粒子鼠标跟随效果（首页）
   - 研究方向卡片悬停展开详情
   - 平滑滚动和页面过渡动画

3. **核心功能模块**
   - 品牌口号全屏展示区
   - 研究方向展示
   - 最新研究成果轮播
   - 新闻动态时间轴
   - 学术定位与愿景陈述
   - 实验室环境实景展示
   - 成员团队介绍
   - 学术成果展示（支持按年份和研究方向筛选）
   - 资源中心（数据集下载、代码仓库链接）
   - 联系方式（地图嵌入、社交媒体链接）

## 技术栈
- HTML5
- CSS3 (Flexbox, Grid)
- JavaScript (原生JS)
- Font Awesome 图标库
- Google Fonts (Inter字体)

## 性能优化
- 图片懒加载
- 首屏加载优化（目标≤2秒）
- 响应式图片适配
- 组件化JavaScript结构

## 使用说明
1. 将所有文件上传到web服务器
2. 确保`images/`文件夹中包含所有必要的图像文件
3. 可以根据实际需求修改`index.html`中的内容（如团队成员信息、研究成果等）
4. 如需调整样式，可以修改`css/style.css`文件

## 注意事项
- 本网站使用了外部资源（Font Awesome、Google Fonts），确保网络连接正常
- 为了获得最佳体验，建议使用现代浏览器（Chrome、Firefox、Safari、Edge）
- 地图功能需要集成实际的地图API（如百度地图或Google Maps）