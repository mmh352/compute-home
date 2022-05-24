import { writable, derived, get } from 'svelte/store';

const INITIAL = 0;
const CONNECTING = 1;
const CONNECTED = 2;
const DISCONNECTED = 5;
const SHUTDOWN = 6;

export const message = writable({} as ApiMessage);
export const connectionStatus = writable(INITIAL);
let connection = null;

export function connect() {
    if (connection === null) {
        connectionStatus.set(CONNECTING);
        if (window.location.protocol === 'https:') {
            connection = new WebSocket('wss://' + window.location.hostname + ':' + window.location.port + '/api');
        } else {
            connection = new WebSocket('ws://' + window.location.hostname + ':' + window.location.port + '/api');
        }
        connection.addEventListener('open', () => {
            connectionStatus.set(CONNECTED);
            message.set({'type': 'connected'});
        });
        connection.addEventListener('close', () => {
            if (get(connectionStatus) !== SHUTDOWN) {
                connectionStatus.set(DISCONNECTED);
            }
            connection = null;
            message.set({'type': 'disconnected'});
        });
        connection.addEventListener('message', (msg) => {
            if (msg.data) {
                message.set(JSON.parse(msg.data));
            }
        });
    }
}

export const isConnecting = derived(connectionStatus, (status) => {
    return status === CONNECTING;
});

export const isConnected = derived(connectionStatus, (status) => {
    return status === CONNECTED;
});

export const isDisconnected = derived(connectionStatus, (status) => {
    return status === DISCONNECTED;
});

export const isShutDown = derived(connectionStatus, (status) => {
    return status === SHUTDOWN;
});

export function sendMessage(message: ApiMessage) {
    if (connection && connection.readyState === 1) {
        connection.send(JSON.stringify(message));
    }
}

export function shutdown() {
    connectionStatus.set(SHUTDOWN);
    if (connection) {
        connection.close();
    }
}
