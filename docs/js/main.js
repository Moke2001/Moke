// 导航栏滚动效果
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// 响应式导航菜单
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const navItems = document.querySelectorAll('.nav-links a');

hamburger.addEventListener('click', function() {
    navLinks.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// 点击导航链接后关闭菜单
navItems.forEach(item => {
    item.addEventListener('click', function() {
        navLinks.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // 减去导航栏高度
                behavior: 'smooth'
            });
        }
    });
});

// 图片懒加载
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.src;
    });
} else {
    // 回退到传统的懒加载库
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
    document.body.appendChild(script);
}

// 页面加载动画
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// 滚动时添加动画类
const animateOnScroll = function() {
    const elements = document.querySelectorAll('.vision-section, .research-highlights, .news-section, .lab-showcase, .research-directions, .team-section, .publications-section, .resources-section, .contact-section');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (elementPosition < screenPosition) {
            element.classList.add('animate');
        }
    });
};

window.addEventListener('scroll', animateOnScroll);
// 初始化时检查一次
window.addEventListener('load', animateOnScroll);

// 页面访问统计（模拟）
function trackPageView() {
    console.log('Page viewed: ' + window.location.pathname);
    // 实际项目中可以集成Google Analytics或其他统计工具
}

// 页面加载完成后执行
window.addEventListener('load', function() {
    trackPageView();
    
    // 添加一些性能监控
    const loadTime = performance.now();
    console.log('Page load time: ' + loadTime.toFixed(2) + 'ms');
    
    // 检测是否满足性能指标（首屏加载≤2秒）
    if (loadTime > 2000) {
        console.warn('Performance warning: Page load time exceeds 2 seconds');
    }
});