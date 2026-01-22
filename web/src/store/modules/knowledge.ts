import { defineStore } from "pinia";
import { store } from "../utils";

export interface DocumentItem {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  author: string;
}

export interface KnowledgeState {
  documents: DocumentItem[];
  currentDocument: DocumentItem | null;
  isLoading: boolean;
  error: string | null;
}

export const useKnowledgeStore = defineStore("pure-knowledge", {
  state: (): KnowledgeState => ({
    documents: [
      {
        id: "1",
        title: "欢迎使用 WisdomBase",
        content: "# 欢迎\n\n这是一个示例文档。",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        author: "admin"
      }
    ],
    currentDocument: null,
    isLoading: false,
    error: null
  }),
  getters: {
    getDocuments(): DocumentItem[] {
      return this.documents;
    },
    getCurrentDocument(): DocumentItem | null {
      return this.currentDocument;
    },
    getLoading(): boolean {
      return this.isLoading;
    },
    getError(): string | null {
      return this.error;
    }
  },
  actions: {
    setDocuments(docs: DocumentItem[]) {
      this.documents = docs;
    },
    setCurrentDocument(doc: DocumentItem | null) {
      this.currentDocument = doc;
    },
    createDocument(doc: Omit<DocumentItem, "id" | "createdAt" | "updatedAt">) {
      const newDoc: DocumentItem = {
        id: Date.now().toString(),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        ...doc
      };
      this.documents.push(newDoc);
      return newDoc;
    },
    updateDocument(id: string, updates: Partial<DocumentItem>) {
      const index = this.documents.findIndex(doc => doc.id === id);
      if (index !== -1) {
        this.documents[index] = {
          ...this.documents[index],
          ...updates,
          updatedAt: new Date().toISOString()
        };
        if (this.currentDocument?.id === id) {
          this.currentDocument = this.documents[index];
        }
      }
    },
    deleteDocument(id: string) {
      const index = this.documents.findIndex(doc => doc.id === id);
      if (index !== -1) {
        this.documents.splice(index, 1);
        if (this.currentDocument?.id === id) {
          this.currentDocument = null;
        }
      }
    },
    setLoading(loading: boolean) {
      this.isLoading = loading;
    },
    setError(error: string | null) {
      this.error = error;
    }
  }
});

export function useKnowledgeStoreHook() {
  return useKnowledgeStore(store);
}
