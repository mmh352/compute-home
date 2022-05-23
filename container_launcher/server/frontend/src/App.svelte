<script lang="ts">
	import { connect } from './store';

	import Content from './Content.svelte';

	connect();
</script>

<div>
	<Content/>
</div>

<style global>
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
