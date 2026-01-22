<script setup lang="ts">
import { computed } from "vue";
import { useUserStoreHook } from "@/store/modules/user";
import { useRouter } from "vue-router";

defineOptions({
  name: "AccessDenied"
});

const router = useRouter();
const userStore = useUserStoreHook();

const userRoles = computed(() => userStore.roles);

const goHome = () => {
  router.push("/");
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="access-denied-container">
    <div class="error-content">
      <div class="error-code">403</div>
      <h1>无权访问</h1>
      <p>您没有权限访问此页面。仅 Admin 和 Editor 角色可以访问知识库。</p>
      <p class="user-info">当前角色: {{ userRoles.join(", ") || "Guest" }}</p>
      <div class="actions">
        <el-button type="primary" @click="goHome">返回首页</el-button>
        <el-button @click="goBack">返回上一页</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.access-denied-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  .error-content {
    text-align: center;
    color: #fff;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    backdrop-filter: blur(10px);
    max-width: 500px;

    .error-code {
      font-size: 120px;
      font-weight: bold;
      line-height: 1;
      margin-bottom: 20px;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    h1 {
      font-size: 32px;
      margin: 0 0 15px 0;
      font-weight: 600;
    }

    p {
      font-size: 16px;
      margin: 10px 0;
      line-height: 1.6;

      &.user-info {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 15px;
      }
    }

    .actions {
      display: flex;
      gap: 10px;
      justify-content: center;
      margin-top: 30px;

      button {
        padding: 10px 30px;
      }
    }
  }
}
</style>
