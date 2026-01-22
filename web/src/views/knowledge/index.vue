<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import KnowledgeEditor from "./KnowledgeEditor.vue";
import DocumentTree from "./DocumentTree.vue";

defineOptions({
  name: "KnowledgeMain"
});

const selectedDocId = ref<string>();
const showNewDocDialog = ref(false);
const newDocTitle = ref("");

const handleCreateNew = () => {
  showNewDocDialog.value = true;
};

const handleConfirmNewDoc = () => {
  if (newDocTitle.value.trim()) {
    showNewDocDialog.value = false;
    newDocTitle.value = "";
    // 编辑器会自动加载新文档
  }
};
</script>

<template>
  <div class="knowledge-main">
    <div class="knowledge-container">
      <aside class="sidebar">
        <div class="sidebar-header">
          <el-button type="primary" block @click="handleCreateNew">
            ➕ 新建文档
          </el-button>
        </div>
        <DocumentTree />
      </aside>
      <main class="editor-area">
        <KnowledgeEditor :doc-id="selectedDocId" />
      </main>
    </div>

    <el-dialog
      v-model="showNewDocDialog"
      title="新建文档"
      width="400px"
      @confirm="handleConfirmNewDoc"
    >
      <el-input
        v-model="newDocTitle"
        placeholder="输入文档标题..."
        clearable
        @keyup.enter="handleConfirmNewDoc"
      />
      <template #footer>
        <el-button @click="showNewDocDialog = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmNewDoc">
          创建
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.knowledge-main {
  width: 100%;
  height: 100%;
}

.knowledge-container {
  display: flex;
  height: 100vh;
  background: #f5f7fa;

  .sidebar {
    width: 280px;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    background: #fff;

    .sidebar-header {
      padding: 15px;
      border-bottom: 1px solid #e0e0e0;

      button {
        width: 100%;
      }
    }
  }

  .editor-area {
    flex: 1;
    overflow: hidden;
  }
}
</style>
