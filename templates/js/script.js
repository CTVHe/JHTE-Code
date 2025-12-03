// API 配置 - 与后端在同一端口
const API_BASE_URL = 'http://localhost:8000/api';

// 其他前端代码保持不变，与之前完全相同
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

async function translateText() {
    const text = document.getElementById('source-text').value.trim();
    const targetLang = document.getElementById('target-language').value;
    
    document.getElementById('translate-error').style.display = 'none';
    
    if (!text) {
        showError('translate', '请输入要翻译的文本');
        return;
    }
    
    document.getElementById('translate-loading').style.display = 'block';
    document.getElementById('translate-result').style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/translate`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text, target_lang: targetLang})
        });
        
        const data = await response.json();
        document.getElementById('translate-loading').style.display = 'none';
        
        if (data.error) {
            showError('translate', data.error);
            return;
        }
        
        document.getElementById('translation-output').textContent = data.translation;
        document.getElementById('translate-result').style.display = 'block';
        
    } catch (error) {
        document.getElementById('translate-loading').style.display = 'none';
        showError('translate', '网络错误，请检查服务是否启动');
    }
}

async function analyzeSentiment() {
    const text = document.getElementById('sentiment-text').value.trim();
    
    document.getElementById('sentiment-error').style.display = 'none';
    
    if (!text) {
        showError('sentiment', '请输入要分析的文本');
        return;
    }
    
    document.getElementById('sentiment-loading').style.display = 'block';
    document.getElementById('sentiment-result').style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        });
        
        const data = await response.json();
        document.getElementById('sentiment-loading').style.display = 'none';
        
        if (data.error) {
            showError('sentiment', data.error);
            return;
        }
        
        displaySentimentResults(data.analysis);
        document.getElementById('sentiment-result').style.display = 'block';
        
    } catch (error) {
        document.getElementById('sentiment-loading').style.display = 'none';
        showError('sentiment', '网络错误，请检查服务是否启动');
    }
}

function displaySentimentResults(analysis) {
    const output = document.getElementById('sentiment-output');
    output.innerHTML = '';
    
    for (const [aspect, sentiment] of Object.entries(analysis)) {
        const sentimentClass = 
            sentiment === '正面' ? 'positive' :
            sentiment === '负面' ? 'negative' : 'neutral';
        
        const aspectElement = document.createElement('div');
        aspectElement.className = `sentiment-item ${sentimentClass}`;
        aspectElement.innerHTML = `<strong>${aspect}</strong>: ${sentiment}`;
        output.appendChild(aspectElement);
    }
    
    if (Object.keys(analysis).length === 0) {
        output.innerHTML = '<p>未检测到明确的情感方面</p>';
    }
}

function showError(type, message) {
    const errorElement = document.getElementById(`${type}-error`);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}