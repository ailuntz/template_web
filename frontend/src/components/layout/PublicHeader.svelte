<script lang="ts">
import ThemeToggle from '$components/biz/ThemeToggle.svelte';
import { Button } from '$components/ui/button';
</script>

<header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
	<div class="container mx-auto flex h-14 items-center justify-between px-4">
		<a href="/" class="flex items-center space-x-2">
			<span class="text-xl font-bold">MyApp</span>
		</a>

		<nav class="hidden md:flex items-center space-x-6">
			<a href="/" class="text-sm font-medium transition-colors hover:text-primary">
				首页
			</a>
			<a href="/features" class="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
				功能
			</a>
			<a href="/pricing" class="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
				价格
			</a>
		</nav>

		<div class="flex items-center space-x-4">
			<ThemeToggle />
			<a href="/auth/login">
				<Button variant="ghost" size="sm">登录</Button>
			</a>
			<a href="/auth/register">
				<Button size="sm">注册</Button>
			</a>
		</div>
	</div>
</header>
