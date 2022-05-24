<script lang="ts">
    import { containers } from '../store';
</script>

<div class="flex-1 max-w-5xl mx-auto px-4 pt-4 overflow-auto">
    <h1 class="sr-only">Access your virtual computing environments</h1>
    <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each $containers as container}
            <li class="flex flex-col w-full h-full border border-gray hover:border-blue dark:hover:border-blue-100 dark:bg-neutral-900 transition-colors hover:shadow-md dark:hover:shadow-blue-800">
                <h2 class="flex-none py-1 px-2 border-b boder-b-gray font-bold">{container.title}</h2>
                <p class="flex-1 py-1 px-2 text-sm">{container.description}</p>
                <nav>
                    <ul class="flex-none flex flex-row">
                        {#if container.state === 'paused'}
                            <li class="flex-1" role="presentation">
                                <button class="block w-full py-1 text-blue dark:text-blue-100 hover:bg-blue hover:text-white dark:hover:bg-blue-700 focus:bg-blue focus:text-white dark:focus:bg-blue-700 transition-colors">Start<span class="sr-only"> the {container.title} VCE</span></button>
                            </li>
                        {:else}
                            <li class="flex-1" role="presentation">
                                <button class="block w-full py-1 text-blue dark:text-blue-100 hover:bg-blue hover:text-white dark:hover:bg-blue-700 focus:bg-blue focus:text-white dark:focus:bg-blue-700 transition-colors">Access<span class="sr-only"> the {container.title} VCE</span></button>
                            </li>
                            <li class="flex-1" role="presentation">
                                <button class="block w-full py-1 text-red dark:text-red-300 hover:bg-red hover:text-white dark:hover:bg-red-700 focus:bg-red focus:text-white dark:focus:bg-red-700 dark:focus:text-white transition-colors">Stop<span class="sr-only"> the {container.title} VCE</span></button>
                            </li>
                        {/if}
                    </ul>
                </nav>
            </li>
        {/each}
    </ul>
</div>
