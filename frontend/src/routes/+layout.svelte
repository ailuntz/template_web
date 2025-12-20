<script lang="ts">
import '../styles/app.css';
import { ToastContainer } from '$components/ui/toast';
import { theme } from '$lib/stores/ui';
import { tokenManager } from '$lib/utils/token-manager';
import { onMount } from 'svelte';

onMount(() => {
	theme.initialize();
	tokenManager.start();

	return () => {
		tokenManager.stop();
	};
});
</script>

<slot />
<ToastContainer />
