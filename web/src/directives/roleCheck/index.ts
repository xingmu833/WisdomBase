import type { Directive, DirectiveBinding } from "vue";
import { hasAuth } from "@/router/utils";
import { useRouter } from "vue-router";

export const requireAdmin: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding<string[] | string>) {
    const router = useRouter();
    const { value } = binding;

    if (value) {
      const requiredRoles = Array.isArray(value) ? value : [value];
      // 检查权限，不符合则删除元素
      if (!hasAuth(requiredRoles)) {
        el.parentNode?.removeChild(el);
      }
    } else {
      throw new Error(
        "[Directive: requireAdmin]: need auth list! Like v-require-admin=\"['admin','editor']\""
      );
    }
  }
};

export const requireEditor: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding<string[] | string>) {
    const { value } = binding;

    if (value) {
      const requiredRoles = Array.isArray(value) ? value : [value];
      if (!hasAuth(requiredRoles)) {
        el.parentNode?.removeChild(el);
      }
    } else {
      throw new Error(
        "[Directive: requireEditor]: need auth list! Like v-require-editor=\"['editor','admin']\""
      );
    }
  }
};
