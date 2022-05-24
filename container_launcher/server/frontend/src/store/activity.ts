import { writable, get } from 'svelte/store';

const WAITING = 0;
const ACTIVE = 1;
const FAILED = 2;
const SUCCEEDED = 3;

function createActivitySetStore() {
    const store = writable(null);

    function initialise(settings) {
        const state = {
            title: settings.title,
            activities: settings.activities.map((activity) => {
                return {
                    id: activity.id,
                    title: activity.title,
                    svg: activity.svg,
                    state: WAITING,
                }
            }),
            message: settings.message || '',
        }
        store.set(state);
    }

    function start(activityId: string, message: string) {
        const state = get(store);
        if (state) {
            let found = false;
            for (let activity of state.activities) {
                if (!found && activity.id !== activityId && (activity.state === WAITING || activity.state === ACTIVE)) {
                    activity.state = SUCCEEDED;
                }
                if (activity.id == activityId) {
                    found = true;
                    activity.state = ACTIVE;
                }
            }
            state.message = message;
            store.set(state);
        }
    }

    function progress() {

    }

    function complete(activityId: string, success: boolean) {
        const state = get(store);
        if (state) {
            for (let activity of state.activities) {
                if (activity.id == activityId) {
                    activity.state = success ? SUCCEEDED : FAILED;
                }
            }
            store.set(state);
        }
    }

    function close() {
        store.set(null);
    }

    return {
        initialise,
        start,
        progress,
        complete,
        close,
        subscribe: store.subscribe,
    }
}

export const activity = createActivitySetStore();
