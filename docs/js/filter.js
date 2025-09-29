// 学术成果筛选功能实现
class PublicationFilter {
    constructor() {
        this.yearFilter = document.getElementById('year-filter');
        this.fieldFilter = document.getElementById('field-filter');
        this.publications = document.querySelectorAll('.publication-item');
        this.noResultsMessage = null;
        
        this.init();
    }
    
    init() {
        if (!this.yearFilter || !this.fieldFilter || this.publications.length === 0) {
            return;
        }
        
        // 创建无结果提示元素
        this.createNoResultsMessage();
        
        // 添加事件监听器
        this.yearFilter.addEventListener('change', () => this.applyFilters());
        this.fieldFilter.addEventListener('change', () => this.applyFilters());
        
        // 初始化时应用一次筛选
        this.applyFilters();
    }
    
    createNoResultsMessage() {
        this.noResultsMessage = document.createElement('div');
        this.noResultsMessage.className = 'no-results';
        this.noResultsMessage.style.display = 'none';
        this.noResultsMessage.innerHTML = `
            <div style="text-align: center; padding: 40px; background-color: var(--light-color); border-radius: 8px; margin-top: 20px;">
                <i class="fas fa-search" style="font-size: 3rem; color: var(--text-light); margin-bottom: 20px;"></i>
                <h4 style="color: var(--text-color); margin-bottom: 10px;">未找到符合条件的论文</h4>
                <p style="color: var(--text-light);">请尝试调整筛选条件</p>
            </div>
        `;
        
        const parentElement = this.publications[0].parentElement;
        parentElement.parentNode.insertBefore(this.noResultsMessage, parentElement.nextSibling);
    }
    
    applyFilters() {
        const selectedYear = this.yearFilter.value;
        const selectedField = this.fieldFilter.value;
        let visibleCount = 0;
        
        this.publications.forEach(publication => {
            const publicationYear = publication.getAttribute('data-year');
            const publicationField = publication.getAttribute('data-field');
            
            // 检查是否满足筛选条件
            const yearMatch = selectedYear === 'all' || publicationYear === selectedYear;
            const fieldMatch = selectedField === 'all' || publicationField === selectedField;
            
            if (yearMatch && fieldMatch) {
                publication.style.display = 'flex';
                visibleCount++;
                // 添加淡入动画
                setTimeout(() => {
                    publication.style.opacity = '1';
                    publication.style.transform = 'translateX(0)';
                }, 50);
            } else {
                publication.style.opacity = '0';
                publication.style.transform = 'translateX(-20px)';
                // 等待动画完成后隐藏
                setTimeout(() => {
                    publication.style.display = 'none';
                }, 300);
            }
        });
        
        // 显示或隐藏无结果提示
        if (visibleCount === 0) {
            this.noResultsMessage.style.display = 'block';
        } else {
            this.noResultsMessage.style.display = 'none';
        }
        
        // 触发筛选完成事件
        this.onFilterComplete(visibleCount);
    }
    
    onFilterComplete(visibleCount) {
        // 可以在这里添加筛选完成后的回调逻辑
        console.log(`筛选完成，显示 ${visibleCount} 篇论文`);
        
        // 发送筛选统计（模拟）
        this.trackFilterUsage(visibleCount);
    }
    
    trackFilterUsage(visibleCount) {
        // 实际项目中可以集成分析工具
        const filterData = {
            year: this.yearFilter.value,
            field: this.fieldFilter.value,
            visibleCount: visibleCount,
            timestamp: new Date().toISOString()
        };
        
        console.log('Filter usage tracked:', filterData);
        
        // 可以添加AJAX请求发送统计数据
        /*
        fetch('/api/track-filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filterData)
        });
        */
    }
    
    // 重置筛选条件
    resetFilters() {
        this.yearFilter.value = 'all';
        this.fieldFilter.value = 'all';
        this.applyFilters();
    }
    
    // 获取当前筛选条件
    getCurrentFilters() {
        return {
            year: this.yearFilter.value,
            field: this.fieldFilter.value
        };
    }
}

// 页面加载完成后初始化筛选功能
window.addEventListener('load', function() {
    // 初始化学术成果筛选功能
    const publicationFilter = new PublicationFilter();
    
    // 为URL参数支持添加筛选功能
    // 这允许通过URL直接访问特定筛选条件的页面
    function applyFiltersFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        const year = urlParams.get('year');
        const field = urlParams.get('field');
        
        if (year && document.getElementById('year-filter')) {
            document.getElementById('year-filter').value = year;
        }
        
        if (field && document.getElementById('field-filter')) {
            document.getElementById('field-filter').value = field;
        }
        
        // 如果URL中有筛选参数，手动触发筛选
        if ((year || field) && publicationFilter) {
            publicationFilter.applyFilters();
        }
    }
    
    // 应用URL中的筛选参数
    applyFiltersFromUrl();
    
    // 监听筛选变化，更新URL参数（可选功能）
    function updateUrlWithFilters() {
        if (!publicationFilter) return;
        
        const filters = publicationFilter.getCurrentFilters();
        const urlParams = new URLSearchParams();
        
        if (filters.year !== 'all') {
            urlParams.set('year', filters.year);
        }
        
        if (filters.field !== 'all') {
            urlParams.set('field', filters.field);
        }
        
        // 更新URL但不刷新页面
        const newUrl = `${window.location.pathname}${urlParams.toString() ? '?' + urlParams.toString() : ''}`;
        window.history.replaceState({}, '', newUrl);
    }
    
    // 添加筛选变化监听器
    if (document.getElementById('year-filter') && document.getElementById('field-filter')) {
        document.getElementById('year-filter').addEventListener('change', updateUrlWithFilters);
        document.getElementById('field-filter').addEventListener('change', updateUrlWithFilters);
    }
    
    // 添加键盘快捷键支持
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + R 重置筛选
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            if (publicationFilter) {
                publicationFilter.resetFilters();
            }
        }
    });
    
    // 为移动设备优化筛选体验
    const optimizeForMobile = function() {
        const isMobile = window.innerWidth < 768;
        const filterGroups = document.querySelectorAll('.filter-group');
        
        if (isMobile) {
            filterGroups.forEach(group => {
                group.style.width = '100%';
            });
        } else {
            filterGroups.forEach(group => {
                group.style.width = 'auto';
            });
        }
    };
    
    // 初始化和响应式调整
    optimizeForMobile();
    window.addEventListener('resize', optimizeForMobile);
});

// 添加高级筛选功能：搜索框
class AdvancedPublicationFilter extends PublicationFilter {
    constructor() {
        super();
        
        this.searchInput = null;
        this.searchTimeout = null;
        
        this.initAdvancedFeatures();
    }
    
    initAdvancedFeatures() {
        // 检查是否已经存在搜索框，不存在则创建
        this.searchInput = document.getElementById('publication-search');
        if (!this.searchInput) {
            this.createSearchInput();
        }
        
        // 添加搜索功能
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.handleSearch());
        }
    }
    
    createSearchInput() {
        const filterContainer = document.querySelector('.publications-filter');
        if (!filterContainer) return;
        
        const searchGroup = document.createElement('div');
        searchGroup.className = 'filter-group';
        searchGroup.innerHTML = `
            <label for="publication-search">搜索论文:</label>
            <input type="text" id="publication-search" placeholder="输入关键词搜索..." style="padding: 8px 15px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; width: 200px;">
        `;
        
        filterContainer.appendChild(searchGroup);
        this.searchInput = document.getElementById('publication-search');
    }
    
    handleSearch() {
        // 清除之前的超时
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
        
        // 设置新的超时，实现防抖
        this.searchTimeout = setTimeout(() => {
            this.applyAdvancedFilters();
        }, 300);
    }
    
    applyAdvancedFilters() {
        const searchTerm = this.searchInput.value.toLowerCase().trim();
        const selectedYear = this.yearFilter.value;
        const selectedField = this.fieldFilter.value;
        let visibleCount = 0;
        
        this.publications.forEach(publication => {
            const publicationYear = publication.getAttribute('data-year');
            const publicationField = publication.getAttribute('data-field');
            const publicationText = publication.textContent.toLowerCase();
            
            // 检查是否满足所有筛选条件
            const yearMatch = selectedYear === 'all' || publicationYear === selectedYear;
            const fieldMatch = selectedField === 'all' || publicationField === selectedField;
            const searchMatch = searchTerm === '' || publicationText.includes(searchTerm);
            
            if (yearMatch && fieldMatch && searchMatch) {
                publication.style.display = 'flex';
                visibleCount++;
                // 添加淡入动画
                setTimeout(() => {
                    publication.style.opacity = '1';
                    publication.style.transform = 'translateX(0)';
                }, 50);
            } else {
                publication.style.opacity = '0';
                publication.style.transform = 'translateX(-20px)';
                // 等待动画完成后隐藏
                setTimeout(() => {
                    publication.style.display = 'none';
                }, 300);
            }
        });
        
        // 显示或隐藏无结果提示
        if (visibleCount === 0) {
            this.noResultsMessage.style.display = 'block';
        } else {
            this.noResultsMessage.style.display = 'none';
        }
        
        // 触发筛选完成事件
        this.onFilterComplete(visibleCount);
    }
}

// 在页面加载完成后延迟初始化高级筛选功能
window.addEventListener('load', function() {
    // 延迟加载高级功能，确保基础功能已加载完成
    setTimeout(() => {
        const advancedFilter = new AdvancedPublicationFilter();
    }, 500);
});