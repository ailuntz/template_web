---
description: 使用 LazyMotion 的 Framer Motion 动画指南
include: ["src/components/**/*.{ts,tsx}", "src/modules/**/*.{ts,tsx}", "src/pages/**/*.tsx", "src/framer-lazy-feature.ts"]
---
# 使用 Framer Motion 实现动画

项目使用 Framer Motion 配合 LazyMotion，以优化 bundle 体积。

## 关键规则：使用 `m.` 而非 `motion.`

**始终在动画组件上使用 `m.` 前缀，以确保启用 LazyMotion 优化：**

```typescript
// ✅ 正确 - 使用 m. 前缀
import { m } from 'framer-motion'

function AnimatedComponent() {
  return (
    <m.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      Content
    </m.div>
  )
}

// ❌ 错误 - 不要使用 motion. 前缀
import { motion } from 'framer-motion'

function WrongComponent() {
  return (
    <motion.div> {/* 会破坏 LazyMotion 优化 */}
      Content
    </motion.div>
  )
}
```

## 可用组件

使用 `m.` 搭配任意 HTML 元素：
```typescript
<m.div />
<m.button />
<m.span />
<m.img />
<m.svg />
<m.path />
// ...任何 HTML 元素
```
