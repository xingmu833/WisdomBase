@echo off
REM WisdomBase API 测试脚本 (Windows版)
REM 运行: test_api.bat

setlocal enabledelayedexpansion

set BASE_URL=http://localhost:8000/api/v1

echo.
echo 🚀 WisdomBase API 测试脚本 (Windows)
echo ====================================
echo.

REM 1. 测试Admin登录
echo 1️⃣  测试Admin登录...
echo.
curl -s -X POST "%BASE_URL%/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{"username":"admin","password":"admin123"}" ^
  | jq "."

REM 提取token (注意：Windows下jq需要单独安装)
for /f "tokens=*" %%i in ('curl -s -X POST "%BASE_URL%/auth/login" -H "Content-Type: application/json" -d "{"username":"admin","password":"admin123"}" ^| jq -r ".data.accessToken"') do set ADMIN_TOKEN=%%i

echo.
echo ✅ Admin Token: %ADMIN_TOKEN:~0,20%...
echo.

REM 2. 获取当前用户
echo 2️⃣  获取当前用户信息...
echo.
curl -s -X GET "%BASE_URL%/auth/me" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  | jq "."
echo.

REM 3. 获取用户列表
echo 3️⃣  获取用户列表...
echo.
curl -s -X GET "%BASE_URL%/users?skip=0^&limit=10" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  | jq "."
echo.

REM 4. 创建新用户
echo 4️⃣  创建新用户...
echo.
curl -s -X POST "%BASE_URL%/users" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  -d "{"username":"testuser","password":"test123456","email":"test@example.com","nickname":"测试用户","roles":["viewer"]}" ^
  | jq "."
echo.

REM 5. 测试Editor登录
echo 5️⃣  测试Editor登录...
echo.
curl -s -X POST "%BASE_URL%/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{"username":"editor","password":"editor123"}" ^
  | jq "."
echo.

REM 6. 测试Viewer登录
echo 6️⃣  测试Viewer登录...
echo.
curl -s -X POST "%BASE_URL%/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{"username":"viewer","password":"viewer123"}" ^
  | jq "."
echo.

REM 7. 获取操作日志
echo 7️⃣  获取操作日志...
echo.
curl -s -X GET "%BASE_URL%/logs?skip=0^&limit=10" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  | jq "."
echo.

echo ✅ 所有测试完成！
echo.
pause
