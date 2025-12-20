---
description: TailwindCSS 样式指南与最佳实践
include: ["src/**/*.{ts,tsx}", "src/lib/cn.ts", "src/styles/**/*.css"]
---

# TailwindCSS 样式指南

项目使用 TailwindCSS 4，并有特定模式与约束。

## 关键规则：禁止动态类名

**所有 Tailwind 类必须是静态定义的，禁止动态构造 className：**

```typescript
// ❌ 错误 - 动态构造类名
const size = 'large'
const className = `text-${size}` // Tailwind 清理时无法识别

// ❌ 错误 - 带变量的模板字符串
const color = 'blue'
const className = `bg-${color}-500`

// ✅ 正确 - 静态类名 + 条件逻辑
const className = clsx({
  'text-base': size === 'small',
  'text-lg': size === 'medium',
  'text-xl': size === 'large',
})

// ✅ 正确 - 预定义映射
const sizeClasses = {
  small: 'text-base',
  medium: 'text-lg',
  large: 'text-xl',
}
const className = sizeClasses[size]
```

## 类名工具

使用 `src/lib/cn.ts` 中的 `cn()` 合并类名：

```typescript
import { cn } from '~/lib/cn'

function Button({ className, variant = 'primary', ...props }) {
  return (
    <button
      className={cn(
        // 基础样式
        'px-4 py-2 rounded-md font-medium transition-colors',
        // 变体样式
        {
          'bg-primary text-white hover:bg-primary/90': variant === 'primary',
          'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary',
          'border border-border bg-background hover:bg-fill': variant === 'outline'
        },
        // 透传的 className
        className
      )}
      {...props}
    />
  )
}
```

## 响应式设计模式

```typescript
// 移动优先
<div className="w-full md:w-1/2 lg:w-1/3">

// 响应式间距
<div className="p-4 md:p-6 lg:p-8">

// 响应式排版
<h1 className="text-2xl md:text-3xl lg:text-4xl">
```

## 暗色模式支持

使用 TailwindCSS v4 内置的 `dark:` 前缀：

```typescript
<div className="bg-background dark:bg-background text-text dark:text-text">
  Content that adapts to dark mode
</div>
```

## 组件样式模式

**基础组件模式**：

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

function Button({ variant = 'primary', size = 'md', className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        // 始终应用的基础样式
        'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',

        // 尺寸变体
        {
          'h-8 px-3 text-sm': size === 'sm',
          'h-10 px-4': size === 'md',
          'h-12 px-6 text-lg': size === 'lg'
        },

        // 颜色变体
        {
          'bg-primary text-white hover:bg-primary/90': variant === 'primary',
          'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary',
          'border border-border bg-background hover:bg-fill': variant === 'outline'
        },

        className
      )}
      {...props}
    />
  )
}
```

## 动画集成

结合 Framer Motion，使用 `m.` 前缀：

```typescript
import { m } from 'framer-motion'
import { cn } from '~/lib/cn'

<m.button
  className={cn(
    'bg-primary text-white px-4 py-2 rounded-md',
    'transition-colors duration-200'
  )}
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
>
  Animated Button
</m.button>
```

## 最佳实践

1. **仅使用静态类名**：不要动态拼接 class
2. **使用 cn()**：统一类名组合方式
3. **移动优先**：以移动端为基础，再逐步扩展断点
4. **组件变体**：使用对象映射模式定义可复用变体
5. **暗色模式**：样式设计时同时考虑暗色模式
