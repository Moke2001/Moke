// 量子态粒子鼠标跟随效果
class QuantumParticles {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: 0, y: 0 };
        this.isMobile = window.innerWidth < 768;
        this.particleCount = this.isMobile ? 30 : 60;
        
        this.init();
    }
    
    init() {
        // 设置canvas尺寸
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        
        // 添加canvas到容器
        this.container.appendChild(this.canvas);
        
        // 创建粒子
        this.createParticles();
        
        // 鼠标跟随效果
        if (!this.isMobile) {
            this.container.addEventListener('mousemove', (e) => {
                const rect = this.canvas.getBoundingClientRect();
                this.mouse.x = e.clientX - rect.left;
                this.mouse.y = e.clientY - rect.top;
            });
        }
        
        // 动画循环
        this.animate();
    }
    
    resizeCanvas() {
        this.canvas.width = this.container.offsetWidth;
        this.canvas.height = this.container.offsetHeight;
        
        // 响应式调整粒子数量
        const newIsMobile = window.innerWidth < 768;
        if (newIsMobile !== this.isMobile) {
            this.isMobile = newIsMobile;
            this.particleCount = this.isMobile ? 30 : 60;
            this.createParticles();
        }
    }
    
    createParticles() {
        this.particles = [];
        
        for (let i = 0; i < this.particleCount; i++) {
            const particle = {
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 3 + 1,
                speedX: (Math.random() - 0.5) * 0.5,
                speedY: (Math.random() - 0.5) * 0.5,
                color: this.getRandomParticleColor(),
                opacity: Math.random() * 0.7 + 0.3,
                phase: Math.random() * Math.PI * 2,
                // 量子特性
                quantumState: Math.random(),
                entanglement: null
            };
            
            this.particles.push(particle);
        }
        
        // 创建量子纠缠
        this.createEntanglement();
    }
    
    getRandomParticleColor() {
        const colors = [
            'rgba(255, 255, 255, ',
            'rgba(173, 216, 230, ',
            'rgba(144, 238, 144, ',
            'rgba(255, 218, 185, '  
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
    
    createEntanglement() {
        // 每两个粒子建立纠缠关系
        for (let i = 0; i < this.particles.length; i += 2) {
            if (i + 1 < this.particles.length) {
                this.particles[i].entanglement = this.particles[i + 1];
                this.particles[i + 1].entanglement = this.particles[i];
            }
        }
    }
    
    updateParticles() {
        this.particles.forEach((particle, index) => {
            // 更新位置
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // 边界检测
            if (particle.x < 0 || particle.x > this.canvas.width) {
                particle.speedX *= -1;
            }
            if (particle.y < 0 || particle.y > this.canvas.height) {
                particle.speedY *= -1;
            }
            
            // 鼠标吸引/排斥效果
            if (!this.isMobile) {
                const dx = particle.x - this.mouse.x;
                const dy = particle.y - this.mouse.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                // 排斥区域
                if (distance < 150) {
                    const force = (150 - distance) / 150 * 0.5;
                    particle.x += (dx / distance) * force;
                    particle.y += (dy / distance) * force;
                }
                // 吸引区域
                else if (distance < 300) {
                    const force = (distance - 150) / 150 * 0.05;
                    particle.x -= (dx / distance) * force;
                    particle.y -= (dy / distance) * force;
                }
            }
            
            // 量子波动效果
            particle.phase += 0.02;
            particle.size = 2 + Math.sin(particle.phase) * 1.5;
            particle.opacity = 0.3 + Math.sin(particle.phase + Math.PI/2) * 0.4;
            
            // 量子态变化
            particle.quantumState = (particle.quantumState + 0.005) % 1;
            
            // 量子纠缠效果
            if (particle.entanglement) {
                this.updateEntangledParticle(particle, index);
            }
        });
    }
    
    updateEntangledParticle(particle, index) {
        const entangledParticle = particle.entanglement;
        const dx = entangledParticle.x - particle.x;
        const dy = entangledParticle.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // 保持纠缠距离
        if (distance > 100) {
            const force = (distance - 100) / distance * 0.03;
            entangledParticle.x -= (dx / distance) * force;
            entangledParticle.y -= (dy / distance) * force;
        }
        
        // 量子态同步
        entangledParticle.quantumState = particle.quantumState;
    }
    
    drawParticles() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制连接线
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                // 根据距离绘制连接线
                if (distance < 100) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(255, 255, 255, ${(100 - distance) / 100 * 0.3})`;
                    this.ctx.lineWidth = (100 - distance) / 100 * 0.5;
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
        
        // 绘制粒子
        this.particles.forEach(particle => {
            this.ctx.beginPath();
            
            // 创建粒子发光效果
            const gradient = this.ctx.createRadialGradient(
                particle.x, particle.y, 0,
                particle.x, particle.y, particle.size * 3
            );
            gradient.addColorStop(0, `${particle.color}${particle.opacity})`);
            gradient.addColorStop(1, `${particle.color}0)`);
            
            this.ctx.fillStyle = gradient;
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            // 量子态表示（闪烁效果）
            if (particle.quantumState > 0.7) {
                this.ctx.beginPath();
                this.ctx.fillStyle = `rgba(255, 255, 255, ${(particle.quantumState - 0.7) * 3})`;
                this.ctx.arc(particle.x, particle.y, particle.size / 2, 0, Math.PI * 2);
                this.ctx.fill();
            }
        });
    }
    
    animate() {
        this.updateParticles();
        this.drawParticles();
        requestAnimationFrame(() => this.animate());
    }
}

// 页面加载完成后初始化粒子效果
window.addEventListener('load', function() {
    setTimeout(() => {
        const particleContainer = document.getElementById('particles-container');
        if (particleContainer) {
            new QuantumParticles('particles-container');
        }
    }, 100); // 延迟初始化，确保容器已完全加载
});

// 性能优化：当页面不可见时暂停动画
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        if (window.particleAnimation) {
            cancelAnimationFrame(window.particleAnimation);
        }
    } else {
        if (window.particleInstance) {
            window.particleInstance.animate();
        }
    }
});