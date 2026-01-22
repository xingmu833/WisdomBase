<script setup lang="ts">
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useKnowledgeStoreHook } from "@/store/modules/knowledge";
import type { DocumentItem } from "@/store/modules/knowledge";

defineOptions({
  name: "DocumentTree"
});

const knowledge = useKnowledgeStoreHook();
const expandedKeys = ref<string[]>([]);

interface TreeNode {
  id: string;
  label: string;
  children?: TreeNode[];
  raw?: DocumentItem;
}

const treeData = ref<TreeNode[]>([
  {
    id: "root",
    label: "📚 文档库",
    children: knowledge.documents.map(doc => ({
      id: doc.id,
      label: doc.title,
      raw: doc,
      children: []
    }))
  }
]);

const handleNodeClick = (data: TreeNode) => {
  if (data.raw) {
    knowledge.setCurrentDocument(data.raw);
    // 可以在这里触发导航或事件
  }
};

const handleDelete = (node: TreeNode) => {
  if (node.raw) {
    ElMessageBox.confirm("确认删除此文档？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning"
    })
      .then(() => {
        knowledge.deleteDocument(node.raw!.id);
        // 更新树数据
        const idx = treeData.value[0].children?.findIndex(
          n => n.id === node.id
        );
        if (idx !== undefined && idx > -1) {
          treeData.value[0].children?.splice(idx, 1);
        }
        ElMessage.success("文档已删除");
      })
      .catch(() => {
        // 用户取消删除
      });
  }
};
</script>

<template>
  <div class="document-tree">
    <div class="tree-header">
      <h3>📑 文档列表</h3>
    </div>
    <el-tree
      :data="treeData"
      :expand-on-click-node="false"
      :default-expand-all="true"
      @node-click="handleNodeClick"
    >
      <template #default="{ data }">
        <div class="tree-node-content">
          <span class="node-label">{{ data.label }}</span>
          <div v-if="data.raw" class="node-actions">
            <el-button
              link
              type="primary"
              size="small"
              @click.stop="() => $emit('edit', data.raw)"
            >
              编辑
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              @click.stop="handleDelete(data)"
            >
              删除
            </el-button>
          </div>
        </div>
      </template>
    </el-tree>
  </div>
</template>

<style scoped lang="scss">
.document-tree {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 4px;
  overflow: hidden;

  .tree-header {
    padding: 15px;
    border-bottom: 1px solid #e0e0e0;
    background: #fafafa;

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      color: #333;
    }
  }

  :deep(.el-tree) {
    flex: 1;
    overflow-y: auto;
    background: #fff;

    .el-tree-node {
      &:hover {
        background: #f5f7fa;
      }
    }

    .el-tree-node__content {
      height: auto;
      padding: 8px 0;
    }

    .el-tree-node__label {
      flex: 1;
    }
  }
}

.tree-node-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 10px;
  padding-right: 10px;

  .node-label {
    flex: 1;
    font-size: 14px;
    color: #333;
  }

  .node-actions {
    display: none;
    gap: 5px;

    button {
      font-size: 12px;
    }
  }

  &:hover .node-actions {
    display: flex;
  }
}
</style>
