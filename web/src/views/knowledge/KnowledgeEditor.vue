<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import Vditor from "vditor";
import "vditor/dist/index.css";
import { useKnowledgeStoreHook } from "@/store/modules/knowledge";
import type { DocumentItem } from "@/store/modules/knowledge";

defineOptions({
  name: "KnowledgeEditor"
});

const props = defineProps<{
  docId?: string;
}>();

const knowledge = useKnowledgeStoreHook();
const editorEl = ref<HTMLDivElement>();
let vditor: Vditor | null = null;

const currentDoc = computed(() => {
  if (props.docId) {
    return knowledge.documents.find(d => d.id === props.docId);
  }
  return null;
});

const documentTitle = ref("");
const isSaving = ref(false);

const initEditor = () => {
  if (!editorEl.value) return;

  vditor = new Vditor(editorEl.value, {
    height: "calc(100vh - 200px)",
    minHeight: 500,
    placeholder: "请输入 Markdown 内容...",
    cache: {
      enable: false
    },
    mode: "ir",
    preview: {
      mode: "both",
      maxWidth: 1200
    },
    toolbar: [
      "emoji",
      "br",
      "bold",
      "italic",
      "strike",
      "link",
      "|",
      "list",
      "ordered-list",
      "check",
      "outdent",
      "indent",
      "|",
      "quote",
      "line",
      "code",
      "inline-code",
      "|",
      "table",
      "image",
      "|",
      "undo",
      "redo",
      "|",
      "fullscreen",
      "export",
      "outline"
    ],
    hint: {
      delay: 200
    },
    counter: {
      enable: true,
      type: "markdown"
    }
  });

  if (currentDoc.value) {
    vditor.setValue(currentDoc.value.content);
    documentTitle.value = currentDoc.value.title;
  }
};

const saveDocument = async () => {
  if (!documentTitle.value.trim()) {
    ElMessage.warning("请输入文档标题");
    return;
  }

  if (!vditor) return;

  const content = vditor.getValue();

  isSaving.value = true;
  try {
    if (currentDoc.value) {
      // 更新现有文档
      knowledge.updateDocument(currentDoc.value.id, {
        title: documentTitle.value,
        content
      });
      ElMessage.success("文档已保存");
    } else {
      // 创建新文档
      knowledge.createDocument({
        title: documentTitle.value,
        content,
        author: "current_user"
      });
      ElMessage.success("文档已创建");
    }
  } catch (error) {
    ElMessage.error("保存失败，请重试");
    console.error("Save error:", error);
  } finally {
    isSaving.value = false;
  }
};

onMounted(() => {
  initEditor();
});
</script>

<template>
  <div class="knowledge-editor">
    <div class="editor-header">
      <div class="title-section">
        <input
          v-model="documentTitle"
          type="text"
          placeholder="输入文档标题..."
          class="document-title"
        />
      </div>
      <div class="action-section">
        <el-button type="primary" :loading="isSaving" @click="saveDocument">
          {{ isSaving ? "保存中..." : "保存文档" }}
        </el-button>
      </div>
    </div>
    <div ref="editorEl" class="vditor-container" />
  </div>
</template>

<style scoped lang="scss">
.knowledge-editor {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: #fff;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;

  .title-section {
    flex: 1;

    .document-title {
      width: 100%;
      padding: 10px 15px;
      font-size: 18px;
      font-weight: 600;
      border: 1px solid #ddd;
      border-radius: 4px;
      transition: border-color 0.3s;

      &:focus {
        outline: none;
        border-color: #409eff;
        box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
      }
    }
  }

  .action-section {
    display: flex;
    gap: 10px;
  }
}

.vditor-container {
  flex: 1;
  overflow: hidden;

  :deep(.vditor) {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
  }
}
</style>
