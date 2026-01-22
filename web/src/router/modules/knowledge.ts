import type { RouteRecordRaw } from "vue-router";
import { useUserStoreHook } from "@/store/modules/user";

const Layout = () => import("@/layout/index.vue");

export default {
  path: "/knowledge",
  name: "Knowledge",
  component: Layout,
  redirect: "/knowledge/editor",
  meta: {
    icon: "ep/notebook",
    title: "知识库",
    rank: 10,
    // 角色权限要求: admin 和 editor
    roles: ["admin", "editor"]
  },
  children: [
    {
      path: "/knowledge/editor",
      name: "KnowledgeEditor",
      component: () => import("@/views/knowledge/index.vue"),
      meta: {
        title: "文档编辑",
        showLink: true,
        roles: ["admin", "editor"],
        keepAlive: true
      },
      beforeEnter: (to, from, next) => {
        const userStore = useUserStoreHook();
        const userRoles = userStore.roles || [];
        const requiredRoles = ["admin", "editor"];

        // 检查用户是否拥有所需角色
        const hasRequiredRole = requiredRoles.some(role =>
          userRoles.includes(role)
        );

        if (hasRequiredRole) {
          next();
        } else {
          // 无权限，跳转到 403 页面
          next("/access-denied");
        }
      }
    },
    {
      path: "/access-denied",
      name: "KnowledgeAccessDenied",
      component: () => import("@/views/knowledge/AccessDenied.vue"),
      meta: {
        title: "无权访问",
        showLink: false
      }
    }
  ]
} satisfies RouteRecordRaw;
