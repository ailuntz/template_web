<script lang="ts">
import { toasts } from '$lib/stores/ui';
import { cn } from '$lib/utils/cn';

interface Props {
	id: string;
	message: string;
	type?: 'success' | 'error' | 'info' | 'warning';
}

const { id, message, type = 'info' }: Props = $props();

const typeStyles = {
	success: 'bg-secondary text-secondary-foreground border-border',
	error: 'bg-destructive text-destructive-foreground border-destructive',
	info: 'bg-accent text-accent-foreground border-border',
	warning: 'bg-muted text-muted-foreground border-border',
};

function dismiss() {
	toasts.remove(id);
}
</script>

<div
	class={cn(
		'flex items-center justify-between gap-4 rounded-lg border p-4 shadow-lg',
		typeStyles[type],
	)}
	role="alert"
>
	<p class="text-sm">{message}</p>
	<button
		onclick={dismiss}
		class="text-current opacity-70 hover:opacity-100"
		aria-label="Dismiss"
	>
		<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
		</svg>
	</button>
</div>
