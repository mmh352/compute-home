/// <reference types="svelte" />

type ApiMessage = ConnectedMessage | DisconnectedMessage | RequestConfigMessage | ConfigMessage | LoginMessage;

type ConnectedMessage = {
    type: 'connected';
};

type DisconnectedMessage = {
    type: 'disconnected';
};

type RequestConfigMessage = {
    type: 'request-config',
};

type ConfigMessage = {
    type: 'config',
};

type LoginMessage = {
    type: 'login',
};
