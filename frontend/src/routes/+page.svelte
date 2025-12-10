<script lang="ts">
import PublicLayout from '$components/layout/PublicLayout.svelte';
import { Button } from '$components/ui/button';
</script>

<svelte:head>
	<title>MyApp - 首页</title>
</svelte:head>

<PublicLayout>
	<section class="container mx-auto px-4 py-24 text-center">
		<h1 class="text-4xl font-bold tracking-tight sm:text-6xl">
			欢迎使用 <span class="text-primary">MyApp</span>
		</h1>
		<p class="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
			一个现代化的全栈应用模板，使用 Svelte + FastAPI 构建，提供完整的用户认证和管理功能。
		</p>
		<div class="mt-10 flex items-center justify-center gap-4">
			<a href="/auth/register">
				<Button size="lg">开始使用</Button>
			</a>
			<a href="/features">
				<Button variant="outline" size="lg">了解更多</Button>
			</a>
		</div>
	</section>

	<section class="container mx-auto px-4 py-16">
		<h2 class="text-center text-3xl font-bold">核心特性</h2>
		<div class="mt-12 grid gap-8 md:grid-cols-3">
			<div class="rounded-lg border p-6">
				<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
					<svg class="h-6 w-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold">安全认证</h3>
				<p class="mt-2 text-muted-foreground">
					基于 JWT 的安全认证系统，支持用户注册、登录和会话管理。
				</p>
			</div>

			<div class="rounded-lg border p-6">
				<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
					<svg class="h-6 w-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold">高性能</h3>
				<p class="mt-2 text-muted-foreground">
					FastAPI 后端配合 Svelte 前端，提供极致的性能体验。
				</p>
			</div>

			<div class="rounded-lg border p-6">
				<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
					<svg class="h-6 w-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold">类型安全</h3>
				<p class="mt-2 text-muted-foreground">
					全栈 TypeScript 支持，通过 OpenAPI 自动生成类型安全的 API 客户端。
				</p>
			</div>
		</div>
	</section>
</PublicLayout>
