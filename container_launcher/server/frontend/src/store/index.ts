import { message, isConnecting, isConnected, isDisconnected, connect, sendMessage, shutdown as connectionShutdown } from './connection'
import { config, containers, shutdown as configShutdown } from './config';
import { user, isUnauthorised, isLoggedOut, shutdown as userShutdown } from './user';
import { activity } from './activity';

function shutdown() {
    connectionShutdown();
    userShutdown();
    configShutdown();
}


export {
    shutdown,

    message,
    isConnecting,
    isConnected,
    isDisconnected,
    connect,
    sendMessage,

    config,
    containers,

    user,
    isUnauthorised,
    isLoggedOut,

    activity,
}
