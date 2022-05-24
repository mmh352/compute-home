<script lang="ts">
	import { onDestroy } from 'svelte';
	import { connect, shutdown } from './store';

	import Content from './Content.svelte';

	connect();

	onDestroy(shutdown);
</script>

<div>
	<Content/>
</div>

<style global>
	@tailwind base;
	@tailwind components;
	@tailwind utilities;

	@layer components {
		body { @apply bg-neutral-100 dark:bg-neutral-900 dark:text-white }
	}
</style>
