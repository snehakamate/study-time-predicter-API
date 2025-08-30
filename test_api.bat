@echo off
echo 🧪 Testing Study Time Prediction API
echo ====================================
echo.

echo 🔍 Testing Health Endpoint...
curl -s http://127.0.0.1:8000/health
echo.
echo.

echo 🔮 Testing Prediction Endpoint...
curl -s -X POST "http://127.0.0.1:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"failures\":0,\"higher\":1,\"absences\":3,\"freetime\":2,\"goout\":3,\"famrel\":4,\"famsup\":1,\"schoolsup\":0,\"paid\":1,\"traveltime\":2,\"health\":5,\"internet\":1,\"age\":17}"

echo.
echo.
echo ✅ Test completed! Check the results above.
pause
