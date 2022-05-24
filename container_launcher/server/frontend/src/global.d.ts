/// <reference types="svelte" />

type ApiMessage = ConnectedMessage | DisconnectedMessage | UnauthorisedMessage | LoggedOutMessage |
                  RequestConfigMessage | ConfigMessage | RequestContainersMessage | ContainersMessage |
                  RequestUserMessage | UserMessage;

type ConnectedMessage = {
    type: 'connected',
};

type DisconnectedMessage = {
    type: 'disconnected',
};

type UnauthorisedMessage = {
    type: 'unauthorised',
};

type LoggedOutMessage = {
    type: 'logged-out',
};

type RequestConfigMessage = {
    type: 'request-config',
};

type Config = {
    title: string,
    vle: ConfigVLE,
};

type ConfigVLE = {
    url: string,
};

type ConfigMessage = {
    type: 'config',
    config: Config,
};

type RequestContainersMessage = {
    type: 'request-containers',
};

type Container = PausedContainer;

type PausedContainer = {
    name: string,
    title: string,
    description: string,
    state: 'paused',
};

type RunningContainer = {
    name: string,
    title: string,
    description: string,
    state: 'running',
    url: 'string',
};

type ContainersMessage = {
    type: 'containers',
    containers: Container[],
};

type RequestUserMessage = {
    type: 'request-user',
};

type User = {
    id: string,
    name: string,
};

type UserMessage = {
    type: 'user',
    user: User,
};
