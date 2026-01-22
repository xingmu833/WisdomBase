<script setup lang="ts">
defineOptions({
  name: "Welcome"
});
</script>

<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <h1>欢迎进入 WisdomBase 智库系统</h1>
    </div>
  </div>
</template>

<style scoped lang="scss">
.welcome-container {
  display: flex;
  flex-direction: column;
  height: 100%;

  .welcome-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;

    h1 {
      margin: 0;
      text-align: center;
    }
  }
}
</style>
