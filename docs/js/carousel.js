// 轮播组件功能实现
class Carousel {
    constructor(carouselSelector, options = {}) {
        this.carousel = document.querySelector(carouselSelector);
        if (!this.carousel) return;
        
        this.track = this.carousel.querySelector('.carousel-track, .gallery-track');
        this.items = this.carousel.querySelectorAll('.carousel-item, .gallery-item');
        this.prevBtn = this.carousel.querySelector('.carousel-prev, .gallery-prev');
        this.nextBtn = this.carousel.querySelector('.carousel-next, .gallery-next');
        this.indicatorsContainer = this.carousel.querySelector('.carousel-indicators');
        
        this.options = {
            autoplay: options.autoplay || true,
            autoplaySpeed: options.autoplaySpeed || 5000,
            infinite: options.infinite || true,
            indicators: options.indicators !== undefined ? options.indicators : true,
            ...options
        };
        
        this.currentIndex = 0;
        this.itemWidth = this.items[0] ? this.items[0].offsetWidth : 0;
        this.timer = null;
        
        this.init();
    }
    
    init() {
        if (this.items.length <= 1) {
            if (this.prevBtn) this.prevBtn.style.display = 'none';
            if (this.nextBtn) this.nextBtn.style.display = 'none';
            return;
        }
        
        // 创建指示器
        if (this.options.indicators && this.indicatorsContainer) {
            this.createIndicators();
        }
        
        // 添加事件监听
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prevSlide());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.nextSlide());
        }
        
        // 自动播放
        if (this.options.autoplay) {
            this.startAutoplay();
            
            // 鼠标悬停时暂停自动播放
            this.carousel.addEventListener('mouseenter', () => this.stopAutoplay());
            this.carousel.addEventListener('mouseleave', () => this.startAutoplay());
        }
        
        // 响应式调整
        window.addEventListener('resize', () => this.handleResize());
        
        // 初始化位置
        this.updateCarousel();
    }
    
    createIndicators() {
        this.indicatorsContainer.innerHTML = '';
        
        this.items.forEach((_, index) => {
            const indicator = document.createElement('button');
            indicator.classList.add('indicator');
            if (index === this.currentIndex) {
                indicator.classList.add('active');
            }
            
            indicator.addEventListener('click', () => this.goToSlide(index));
            this.indicatorsContainer.appendChild(indicator);
        });
    }
    
    updateIndicators() {
        const indicators = this.indicatorsContainer.querySelectorAll('.indicator');
        indicators.forEach((indicator, index) => {
            if (index === this.currentIndex) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });
    }
    
    nextSlide() {
        let nextIndex = this.currentIndex + 1;
        
        if (this.options.infinite) {
            nextIndex = nextIndex >= this.items.length ? 0 : nextIndex;
        } else {
            nextIndex = Math.min(nextIndex, this.items.length - 1);
        }
        
        this.goToSlide(nextIndex);
    }
    
    prevSlide() {
        let prevIndex = this.currentIndex - 1;
        
        if (this.options.infinite) {
            prevIndex = prevIndex < 0 ? this.items.length - 1 : prevIndex;
        } else {
            prevIndex = Math.max(prevIndex, 0);
        }
        
        this.goToSlide(prevIndex);
    }
    
    goToSlide(index) {
        this.currentIndex = index;
        this.updateCarousel();
        
        if (this.options.indicators && this.indicatorsContainer) {
            this.updateIndicators();
        }
        
        // 重置自动播放计时器
        if (this.options.autoplay) {
            this.stopAutoplay();
            this.startAutoplay();
        }
    }
    
    updateCarousel() {
        if (!this.track || this.items.length === 0) return;
        
        // 计算位移
        const offset = -this.currentIndex * 100;
        this.track.style.transform = `translateX(${offset}%)`;
        this.track.style.transition = 'transform 0.5s ease';
    }
    
    startAutoplay() {
        this.timer = setInterval(() => {
            this.nextSlide();
        }, this.options.autoplaySpeed);
    }
    
    stopAutoplay() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
    
    handleResize() {
        // 重新计算项目宽度
        this.itemWidth = this.items[0] ? this.items[0].offsetWidth : 0;
        this.updateCarousel();
    }
}

// 页面加载完成后初始化轮播组件
window.addEventListener('load', function() {
    // 研究成果轮播
    const researchCarousel = new Carousel('.research-highlights .carousel', {
        autoplay: true,
        autoplaySpeed: 6000,
        infinite: true,
        indicators: true
    });
    
    // 为移动设备优化轮播体验
    const isMobile = window.innerWidth < 768;
    if (isMobile) {
        // 移动设备上禁用自动播放或调整速度
        if (researchCarousel) {
            researchCarousel.stopAutoplay();
        }
    }
});

// 触摸滑动支持
class TouchCarousel extends Carousel {
    constructor(carouselSelector, options = {}) {
        super(carouselSelector, options);
        
        this.touchStartX = 0;
        this.touchEndX = 0;
        
        this.initTouchEvents();
    }
    
    initTouchEvents() {
        if (!this.carousel) return;
        
        this.carousel.addEventListener('touchstart', (e) => this.handleTouchStart(e), false);
        this.carousel.addEventListener('touchend', (e) => this.handleTouchEnd(e), false);
        this.carousel.addEventListener('touchmove', (e) => this.handleTouchMove(e), false);
        
        // 鼠标拖拽支持（桌面端）
        let isDragging = false;
        let dragStartX = 0;
        let initialOffset = 0;
        
        this.carousel.addEventListener('mousedown', (e) => {
            isDragging = true;
            dragStartX = e.clientX;
            initialOffset = -this.currentIndex * 100;
            this.stopAutoplay();
            this.track.style.transition = 'none';
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const dragX = e.clientX - dragStartX;
            const dragPercentage = (dragX / this.carousel.offsetWidth) * 100;
            const newOffset = initialOffset + dragPercentage;
            
            // 限制拖动范围
            if (newOffset > 0 && this.currentIndex === 0 && !this.options.infinite) {
                return;
            }
            if (newOffset < -100 * (this.items.length - 1) && 
                this.currentIndex === this.items.length - 1 && !this.options.infinite) {
                return;
            }
            
            this.track.style.transform = `translateX(${newOffset}%)`;
        });
        
        document.addEventListener('mouseup', () => {
            if (!isDragging) return;
            isDragging = false;
            this.track.style.transition = 'transform 0.5s ease';
            
            // 判断是否需要切换到下一张或上一张
            const dragDistance = initialOffset - (-this.currentIndex * 100);
            if (Math.abs(dragDistance) > 20) {
                if (dragDistance > 0) {
                    this.prevSlide();
                } else {
                    this.nextSlide();
                }
            } else {
                this.updateCarousel();
            }
            
            if (this.options.autoplay) {
                this.startAutoplay();
            }
        });
    }
    
    handleTouchStart(e) {
        this.touchStartX = e.changedTouches[0].screenX;
        this.stopAutoplay();
    }
    
    handleTouchEnd(e) {
        this.touchEndX = e.changedTouches[0].screenX;
        this.handleSwipe();
        if (this.options.autoplay) {
            this.startAutoplay();
        }
    }
    
    handleTouchMove(e) {
        // 防止页面滚动干扰轮播滑动
        e.preventDefault();
    }
    
    handleSwipe() {
        const swipeThreshold = 50; // 滑动阈值
        
        if (this.touchEndX < this.touchStartX - swipeThreshold) {
            // 向左滑动
            this.nextSlide();
        } else if (this.touchEndX > this.touchStartX + swipeThreshold) {
            // 向右滑动
            this.prevSlide();
        }
    }
}

// 为支持触摸的设备增强轮播功能
window.addEventListener('load', function() {
    // 检测是否支持触摸
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    if (isTouchDevice) {
        // 为研究成果轮播添加触摸支持
        const researchCarousel = document.querySelector('.research-highlights .carousel');
        if (researchCarousel) {
            new TouchCarousel('.research-highlights .carousel', {
                autoplay: true,
                autoplaySpeed: 6000,
                infinite: true,
                indicators: true
            });
        }
    }
});