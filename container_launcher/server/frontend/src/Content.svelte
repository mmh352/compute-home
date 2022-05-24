<script lang="ts">
    import { Router, Link, Route } from "svelte-navigator";

    import Launcher from './routes/Launcher.svelte';
    import Activity from './components/Activity.svelte';
    import Dialog from './components/Dialog.svelte';

    import { config, user, isUnauthorised, isLoggedOut, isDisconnected, connect } from './store';
</script>

<main class="flex flex-col max-w-5xl h-screen mx-auto bg-white dark:bg-neutral-800 overflow-hidden shadow-lg dark:shadow-neutral-800">
    <header class="flex-none flex flex-row space-x-4 px-3 py-2 border-b border-b-blue text-sm shadow-md z-10">
        <span class="flex-1">{#if $config && $config.title}{$config.title}{:else}Loading... Please wait...{/if}</span>
        {#if $user && $user.name}
            <span class="flex-none">{$user.name}</span>
            <a href="/logout" class="flex-none text-blue dark:text-blue-300 hover:underline">Logout</a>
        {/if}
    </header>
    <Router basepath="/app">
        <Route path="/">
            <Launcher/>
        </Route>
    </Router>
    <Activity/>
    {#if $isLoggedOut}
        <Dialog>
            <h2 slot="title">Logged Out</h2>
            <div slot="content">
                You have logged out of the {$config.title}. If you want to access the {$config.title} again, then please
                {#if $config.vle && $config.vle.url}<a href={$config.vle.url} class="text-blue dark:text-blue-300 hover:underline">return to the VLE</a>{:else}return to the VLE{/if}
                from which you accessed the {$config.title} and
                {#if $config.vle && $config.vle.url}<a href={$config.vle.url} class="text-blue dark:text-blue-300 hover:underline">log in again</a>{:else}log in again{/if}.
            </div>
        </Dialog>
    {:else if $isUnauthorised}
        <Dialog>
            <h2 slot="title">Unauthorised</h2>
            <div slot="content">
                You are not authorised to access the {$config.title}. Please
                {#if $config.vle && $config.vle.url}<a href={$config.vle.url} class="text-blue dark:text-blue-300 hover:underline">return to the VLE</a>{:else}return to the VLE{/if}
                from which you accessed the {$config.title} and
                {#if $config.vle && $config.vle.url}<a href={$config.vle.url} class="text-blue dark:text-blue-300 hover:underline">log in again</a>{:else}log in again{/if}.
            </div>
        </Dialog>
    {:else if $isDisconnected}
        <Dialog>
            <h2 slot="title">Disconnected</h2>
            <div slot="content">
                You have been disconnected from the {$config.title}. You can <button on:click={() => { connect(); }} class="text-blue dark:text-blue-300 hover:underline">click here to re-connect</button>.
            </div>
        </Dialog>
    {/if}
</main>
