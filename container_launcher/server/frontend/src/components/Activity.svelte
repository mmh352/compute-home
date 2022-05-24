<script lang="ts">
    import { activity } from '../store';
</script>

{#if $activity}
    <div class="fixed left-0 top-0 w-full h-full z-50 bg-white dark:bg-black bg-opacity-80 dark:bg-opacity-60">
        <div role="dialog" class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-neutral-800 border-2 border-blue dark:border-blue-300 shadow-xl dark:shadow-blue-900">
            <h2 class="font-bold px-3 py-2 border-b-2 border-b-gray dark:border-b-gray-900">{$activity.title}</h2>
            <ol class="flex flex-row space-x-6 px-4 py-2 justify-center">
                {#each $activity.activities as activity}
                    <li aria-label={activity.title} title={activity.title}>
                        <svg aria-hidden="true" viewBox="0 0 24 24" class="w-16 h-16 md:w-32 md:h-32 {activity.state === 0 ? 'text-gray dark:text-gray-900' : (activity.state === 1 ? 'text-blue dark:text-blue-300 animate-pulse' : (activity.state === 2 ? 'text-red dark:text-red-400' : (activity.state === 3 ? 'text-green dark:text-green-500' : '')))}">
                            <path fill="currentColor" d={activity.svg}/>
                        </svg>
                    </li>
                {/each}
            </ol>
            <p class="px-3 py-2">{$activity.message}</p>
        </div>
    </div>
{/if}
