# Ollama 本地模型测试脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  StaffFAQ 本地模型测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Ollama 是否安装
Write-Host "[1/4] 检查 Ollama 安装..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version
    Write-Host "✅ Ollama 已安装: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama 未安装，请先下载安装" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 检查模型是否已下载
Write-Host "[2/4] 检查模型..." -ForegroundColor Yellow
$modelList = ollama list
if ($modelList -match "qwen2.5:1.5b") {
    Write-Host "✅ 模型 qwen2.5:1.5b 已安装" -ForegroundColor Green
} else {
    Write-Host "⚠️  模型未安装，正在下载..." -ForegroundColor Yellow
    Write-Host "   这可能需要几分钟..." -ForegroundColor Gray
    ollama pull qwen2.5:1.5b
}
Write-Host ""

# 检查 .env 配置
Write-Host "[3/4] 检查配置文件..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "LLM_PROVIDER=ollama") {
        Write-Host "✅ .env 配置正确（使用本地模型）" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env 中 LLM_PROVIDER 不是 ollama" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  .env 文件不存在" -ForegroundColor Yellow
}
Write-Host ""

# 检查虚拟环境
Write-Host "[4/4] 检查虚拟环境..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "✅ 虚拟环境已创建" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  一切就绪！可以启动应用了" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "运行以下命令启动：" -ForegroundColor Yellow
    Write-Host "  venv\Scripts\activate" -ForegroundColor Gray
    Write-Host "  streamlit run app.py" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "⚠️  虚拟环境未创建" -ForegroundColor Yellow
    Write-Host "   运行: python -m venv venv" -ForegroundColor Gray
}
