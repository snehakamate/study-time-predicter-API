# PowerShell script to test the Study Time Prediction API

Write-Host "🧪 Testing Study Time Prediction API with PowerShell" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Test data
$testData = @{
    failures = 0
    higher = 1
    absences = 3
    freetime = 2
    goout = 3
    famrel = 4
    famsup = 1
    schoolsup = 0
    paid = 1
    traveltime = 2
    health = 5
    internet = 1
    age = 17
} | ConvertTo-Json

Write-Host "📊 Test Data:" -ForegroundColor Yellow
Write-Host $testData -ForegroundColor Gray
Write-Host ""

try {
    # Test health endpoint
    Write-Host "🔍 Testing Health Endpoint..." -ForegroundColor Blue
    $healthResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
    Write-Host "✅ Health Check: $($healthResponse | ConvertTo-Json)" -ForegroundColor Green
    Write-Host ""

    # Test prediction endpoint
    Write-Host "🔮 Testing Prediction Endpoint..." -ForegroundColor Blue
    $predictionResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -Body $testData -ContentType "application/json"
    
    Write-Host "✅ Prediction Successful!" -ForegroundColor Green
    Write-Host "📊 Results:" -ForegroundColor Yellow
    Write-Host "   Study Time: $($predictionResponse.predicted_study_time)" -ForegroundColor White
    Write-Host "   Confidence: $($predictionResponse.confidence_level)" -ForegroundColor White
    Write-Host "   Key Factors: $($predictionResponse.key_influencing_factors -join ', ')" -ForegroundColor White
    Write-Host "   Recommendation: $($predictionResponse.recommendation)" -ForegroundColor White

} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎯 To test more scenarios, modify the testData object above!" -ForegroundColor Cyan
