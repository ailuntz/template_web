---
description: 组件组织与架构指南
include: ["src/components/**/*.{ts,tsx}", "src/modules/**/*.{ts,tsx}"]
---
# 组件组织

遵循以下组件架构以保持项目结构一致：

## 目录结构

**基础 UI 组件**：`src/components/ui/`
- 可复用的基础组件（按钮、输入框、模态框等）
- 可在任何应用中复用的通用组件
- 基于 Radix UI 原子组件并自定义样式
- 示例：`Button`、`Input`、`Select`、`Tooltip`、`Accordion`

**通用组件**：`src/components/common/`
- 与应用相关的共享组件
- 在多个功能中使用，但仅针对本应用的组件
- 示例：`ErrorElement`、`Footer`、`LoadRemixAsyncComponent`、`NotFound`

**业务模块组件**：`src/modules/`
- 按领域划分的功能组件
- 属于具体业务特性的逻辑组件
- 示例：`src/modules/feed/`、`src/modules/auth/`、`src/modules/user/`

## 组件放置规则

**通用组件** → `src/components/ui/`
- 可用于任意 React 应用
- 纯 UI、无业务逻辑的组件
- 可跨领域复用

**功能组件** → `src/modules/{domain}/`
- 针对具体业务领域/功能的组件
- 含有领域逻辑或数据处理
- 示例：`FeedTimeline`、`UserProfile`、`AuthForm`

**应用共享组件** → `src/components/common/`
- 在多个功能中使用，但仅属于本应用的组件
- 可能包含应用特定逻辑

## 路径别名

使用 `~/` 作为 `src/` 的导入别名（已在 tsconfig 配置）：

```typescript
// 推荐
import { Button } from '~/components/ui/button'
import { UserProfile } from '~/modules/user/UserProfile'

// 避免
import { Button } from '../../../components/ui/button'
```

## 组件示例

```typescript
// 通用 UI 组件 - 放在 src/components/ui/
// 文件：src/components/ui/button/Button.tsx
export function Button({ children, ...props }) {
  return <button className="..." {...props}>{children}</button>
}

// 业务组件 - 放在 src/modules/
// 文件：src/modules/feed/FeedTimeline.tsx
export function FeedTimeline() {
  // Feed 相关逻辑与 UI
}

// 应用共享组件 - 放在 src/components/common/
// 文件：src/components/common/AppHeader.tsx
export function AppHeader() {
  // 应用导航等头部逻辑
}
```

## 模块化架构原则

**若组件属于某个业务领域/功能，请将其放入对应的模块目录。**

这样可以保持代码库清晰，便于查找领域功能。
