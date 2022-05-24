import { writable } from 'svelte/store';

import { message, sendMessage } from './connection';
import { activity } from './activity';


export const user = writable({} as User);
export const isUnauthorised = writable(false);
export const isLoggedOut = writable(false);


const unsubscribeMessage = message.subscribe((msg) => {
    if (msg.type === 'config') {
        isUnauthorised.set(false);
        isLoggedOut.set(false);
        activity.start('user', 'Fetching your details...');
        sendMessage({type: 'request-user'});
    } else if (msg.type === 'user') {
        user.set(msg.user);
        activity.complete('user', true);
    } else if (msg.type === 'unauthorised') {
        activity.close();
        isUnauthorised.set(true);
    } else if (msg.type === 'logged-out') {
        activity.close();
        isLoggedOut.set(true);
    }
});


export function shutdown() {
    unsubscribeMessage();
}
