<script lang="ts">
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from '$components/ui/card';
import { Skeleton } from '$components/ui/skeleton';
import { readCurrentUserApiV1UsersMeGet } from '$lib/api';
import { auth, currentUser, isLoading } from '$lib/stores/auth';
import { onMount } from 'svelte';

onMount(async () => {
	const token = auth.initialize();
	// 只在有 token 但没有缓存用户时才从后端获取
	if (token && !$currentUser) {
		try {
			const { data, error } = await readCurrentUserApiV1UsersMeGet();
			if (data) {
				auth.setUser(data);
			} else if (error) {
				auth.logout();
			}
		} catch (error) {
			console.error('Failed to fetch user:', error);
		}
	}
	auth.setLoading(false);
});
</script>

<svelte:head>
	<title>仪表盘 - MyApp</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold">仪表盘</h1>
		<p class="text-muted-foreground">欢迎回来，{$currentUser?.full_name || $currentUser?.email || '用户'}</p>
	</div>

	<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
		{#if $isLoading}
			{#each Array(4) as _}
				<Card>
					<CardHeader class="pb-2">
						<Skeleton class="h-4 w-24" />
					</CardHeader>
					<CardContent>
						<Skeleton class="h-8 w-16" />
					</CardContent>
				</Card>
			{/each}
		{:else}
			<Card>
				<CardHeader class="pb-2">
					<CardDescription>总访问量</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="text-2xl font-bold">1,234</div>
				</CardContent>
			</Card>

			<Card>
				<CardHeader class="pb-2">
					<CardDescription>活跃用户</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="text-2xl font-bold">567</div>
				</CardContent>
			</Card>

			<Card>
				<CardHeader class="pb-2">
					<CardDescription>任务完成</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="text-2xl font-bold">89</div>
				</CardContent>
			</Card>

			<Card>
				<CardHeader class="pb-2">
					<CardDescription>待处理</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="text-2xl font-bold">12</div>
				</CardContent>
			</Card>
		{/if}
	</div>

	<Card>
		<CardHeader>
			<CardTitle>快速开始</CardTitle>
			<CardDescription>以下是一些常用操作</CardDescription>
		</CardHeader>
		<CardContent>
			<ul class="space-y-2">
				<li>
					<a href="/dashboard/profile" class="text-primary hover:underline">
						完善个人资料
					</a>
				</li>
				<li>
					<a href="/dashboard/settings" class="text-primary hover:underline">
						调整系统设置
					</a>
				</li>
			</ul>
		</CardContent>
	</Card>
</div>
