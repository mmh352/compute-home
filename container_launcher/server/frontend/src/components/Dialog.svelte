<script lang="ts"></script>

<div class="fixed left-0 top-0 w-full h-full z-50 bg-white dark:bg-black bg-opacity-80 dark:bg-opacity-60">
    <div role="dialog" class="flex flex-col w-72 md:w-96 max-w-screen absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-neutral-800 border-2 border-blue dark:border-blue-300 shadow-xl dark:shadow-blue-900">
        {#if $$slots.title}
            <div class="flex-none px-3 py-2 border-b-2 border-b-gray dark:border-b-gray-900 font-bold"><slot name="title"/></div>
        {/if}
        {#if $$slots.content}
            <div class="flex-1 px-3 py-2"><slot name="content"/></div>
        {/if}
        {#if $$slots.buttons}
            <div class="flex-none px-3 py-2"><slot name="buttons"/></div>
        {/if}
    </div>
</div>
