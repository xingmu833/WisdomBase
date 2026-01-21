#!/bin/bash
# WisdomBase API 测试脚本
# 使用: ./test_api.sh

BASE_URL="http://localhost:8000/api/v1"

echo "🚀 WisdomBase API 测试脚本"
echo "=========================="
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 测试登录
echo -e "${YELLOW}1. 测试Admin登录...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }')

echo "$LOGIN_RESPONSE" | jq '.'

# 提取token
ADMIN_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.accessToken')
ADMIN_REFRESH=$(echo "$LOGIN_RESPONSE" | jq -r '.data.refreshToken')

echo -e "${GREEN}✓ Admin Token: ${ADMIN_TOKEN:0:20}...${NC}"
echo ""

# 2. 测试获取当前用户
echo -e "${YELLOW}2. 获取当前用户信息...${NC}"
curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.'
echo ""

# 3. 测试获取用户列表
echo -e "${YELLOW}3. 获取用户列表...${NC}"
curl -s -X GET "$BASE_URL/users?skip=0&limit=10" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.'
echo ""

# 4. 测试创建新用户
echo -e "${YELLOW}4. 创建新用户...${NC}"
CREATE_USER=$(curl -s -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "username": "testuser",
    "password": "test123456",
    "email": "test@example.com",
    "nickname": "测试用户",
    "roles": ["viewer"]
  }')

echo "$CREATE_USER" | jq '.'
NEW_USER_ID=$(echo "$CREATE_USER" | jq -r '.id // empty')
echo ""

# 5. 测试编辑者登录
echo -e "${YELLOW}5. 测试Editor登录...${NC}"
EDITOR_LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "editor",
    "password": "editor123"
  }')

echo "$EDITOR_LOGIN" | jq '.'
EDITOR_TOKEN=$(echo "$EDITOR_LOGIN" | jq -r '.data.accessToken')
echo -e "${GREEN}✓ Editor Token: ${EDITOR_TOKEN:0:20}...${NC}"
echo ""

# 6. 测试查看者登录
echo -e "${YELLOW}6. 测试Viewer登录...${NC}"
VIEWER_LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "viewer",
    "password": "viewer123"
  }')

echo "$VIEWER_LOGIN" | jq '.'
VIEWER_TOKEN=$(echo "$VIEWER_LOGIN" | jq -r '.data.accessToken')
echo -e "${GREEN}✓ Viewer Token: ${VIEWER_TOKEN:0:20}...${NC}"
echo ""

# 7. 测试Token刷新
echo -e "${YELLOW}7. 测试Token刷新...${NC}"
REFRESH=$(curl -s -X POST "$BASE_URL/auth/refresh-token" \
  -H "Content-Type: application/json" \
  -d "{
    \"refreshToken\": \"$ADMIN_REFRESH\"
  }")

echo "$REFRESH" | jq '.'
NEW_ADMIN_TOKEN=$(echo "$REFRESH" | jq -r '.data.accessToken')
echo -e "${GREEN}✓ New Token: ${NEW_ADMIN_TOKEN:0:20}...${NC}"
echo ""

# 8. 测试获取操作日志
echo -e "${YELLOW}8. 获取操作日志...${NC}"
curl -s -X GET "$BASE_URL/logs?skip=0&limit=10" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.'
echo ""

# 9. 测试权限拒绝（Viewer尝试访问用户列表）
echo -e "${YELLOW}9. 测试权限拒绝（Viewer访问用户列表）...${NC}"
curl -s -X GET "$BASE_URL/users?skip=0&limit=10" \
  -H "Authorization: Bearer $VIEWER_TOKEN" | jq '.'
echo ""

# 10. 测试登出
echo -e "${YELLOW}10. 测试登出...${NC}"
curl -s -X POST "$BASE_URL/auth/logout" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.'
echo ""

echo -e "${GREEN}✓ 所有测试完成！${NC}"
