<style>
    #accordion {
        background: white;
        border-bottom: 1px solid #ebe9f1;
    }

    #accordion button {
        width: 100%;
        padding: 1rem;
        background: white;
        border: none;
        text-align: left;
        cursor: pointer;
    }

    #accordion #panel {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.25s ease;
    }

    .container {
        height: calc(100vh - 156px);
        min-width: 100%;
        display: grid;
        grid-template-columns: 300px 1fr;
        grid-template-areas: "sidebar chat";
        border: 1px solid #ebe9f1;
        padding: 0;
    }

    .mobile-container {
        height: calc(100vh - 206px);
        display: grid;
        grid-template-areas: "chat";
        border: 1px solid #ebe9f1;
        padding: 0;
    }

    #sidebar {
        grid-area: sidebar;
        display: grid;
        grid-template-rows: 60px 1fr;
        grid-template-areas: "header" "users";
        border-right: 1px solid #ebe9f1;
        min-height: 0;
    }

    #sidebar #header {
        grid-area: header;
    }

    #sidebar #users {
        grid-area: users;
        overflow-y: auto;
        min-height: 0;
    }

    .user {
        display: flex;
        flex-direction: row;
        align-items: center;
        padding: 0.75rem 1rem;
    }

    .user:hover {
        cursor: pointer;
        background: #F8F8F8;
    }

    #chat {
        grid-area: chat;
        min-height: 0;
        display: grid;
        grid-template-rows: 1fr 65px;
        grid-template-areas:
                "messages"
                "input";
    }

    #messages {
        grid-area: messages;
        overflow-y: auto;
        background-image: url("/custom/images/chat-background.svg");
        background-color: #f2f0f7;
        background-repeat: repeat;
        background-size: 200px;
        padding: 0.75rem 1rem;
        min-height: 0;
    }

    #messages .avatar img {
        border: 2px solid #fff;
    }

    .message__avatar {
        float: right;
    }

    .message__body {
        display: block;
        margin: 10px 30px 0 0;
        overflow: hidden;
    }

    .message__content {
        float: right;
        padding: 0.7rem 1rem;
        margin: 0 1rem 10px 0;
        clear: both;
        color: #fff;
        background-image: linear-gradient(80deg, #7367f0, #9e95f5);
        background-repeat: repeat-x;
        border-radius: 0.357rem;
        box-shadow: 0 4px 8px 0 rgba(34, 41, 47, 0.12);
        max-width: 75%;
    }

    .message__content p {
        margin: 0;
    }

    .message_left .message__avatar {
        float: left;
    }

    .message_left .message__content {
        float: left;
        margin: 0 0 10px 1rem;
        color: #6e6b7b;
        background: none;
        background-color: white;
    }

    #input {
        grid-area: input;
        border-top: 1px solid #ebe9f1;
        padding: 0 1rem;
        display: flex;
        align-items: center;
    }

    #input form {
        background-color: #fff;
        display: flex;
        align-items: center;
        flex-grow: 1;
    }

    #input .input-group {
        flex: 1;
    }

    #input .btn span {
        white-space: nowrap;
    }
</style>
<script lang="ts">
    import {PUBLIC_CHAT_URL} from "$env/static/public";

    import {onMount} from "svelte";

    import {io, type Socket} from "socket.io-client";

    import ChevronUp from "$lib/components/icons/ChevronUp.svelte";
    import ChevronDown from "$lib/components/icons/ChevronDown.svelte";
    import TokenService from "$lib/services/token.ts";

    interface ConnectedUser {
        id: string;
        username: string;
        avatar_url?: string;
    }

    let containerElement: HTMLDivElement;

    let isAccordionOpen = $state<boolean>(false);
    let isChatContainerSmall = $state<boolean>(false);

    let socket = $state<Socket>();
    let connectedUsers = $state<ConnectedUser[]>([]);

    onMount(() => {
        console.log(PUBLIC_CHAT_URL);

        socket = io(PUBLIC_CHAT_URL, {
            transports: ["websocket"],
            auth: {token: TokenService.getToken()},
            autoConnect: false
        });

        socket?.on("list_users", (data) => console.log(data));
        socket?.on("join_chat", (data) => console.log(data));
        socket?.on("leave_chat", (data) => console.log(data));

        socket?.connect();

        return () => {
            socket?.disconnect();
        }
    });

    onMount(() => {
        const ro = new ResizeObserver(entries => {
            for (const entry of entries) {
                isChatContainerSmall = entry.contentRect.width < 934;
            }
        });

        ro.observe(containerElement);

        return () => ro.disconnect();
    });
</script>
<div class="card">
    <div class="card-body p-0">
        <div id="accordion"
             class:d-block={isChatContainerSmall}
             class:d-none={!isChatContainerSmall}
        >
            <button onclick={() => isAccordionOpen = !isAccordionOpen}>
                <h4 class="text-primary p-0 m-0 d-flex justify-content-between align-items-center w-100">
                    Users
                    {#if isAccordionOpen}
                        <ChevronUp/>
                    {:else if !isAccordionOpen}
                        <ChevronDown/>
                    {/if}
                </h4>
            </button>
            <div id="panel" style:max-height={isAccordionOpen ? '500px' : '0'}>
                <div>
                    <div class="user">
                    <span class="avatar">
                        <img
                                src="/vuexy/images/portrait/small/avatar-s-3.jpg"
                                height="42"
                                width="42"
                                alt="avatar">
                        <span class="avatar-status-online"></span>
                    </span>
                        <h5 class="ml-1 mb-0">Teresa Lisbon</h5>
                    </div>
                </div>
            </div>
        </div>
        <div
                bind:this={containerElement}
                class:container={!isChatContainerSmall}
                class:mobile-container={isChatContainerSmall}
        >
            <div
                    id="sidebar"
                    class:d-none={isChatContainerSmall}>
                <div id="header">
                    <h4 class="text-primary pt-2 pl-1 pb-1 mb-0">Users</h4>
                </div>
                <div id="users">
                    <div class="user">
                    <span class="avatar">
                        <img
                                src="/vuexy/images/portrait/small/avatar-s-3.jpg"
                                height="42"
                                width="42"
                                alt="avatar">
                        <span class="avatar-status-online"></span>
                    </span>
                        <h5 class="ml-1 mb-0">Teresa Lisbon</h5>
                    </div>
                </div>
            </div>
            <div id="chat">
                <div id="messages">
                    <!--Someone-->
                    <div class="message message_left">
                        <div class="message__avatar">
                                                <span class="avatar box-shadow-1 cursor-pointer">
                                                    <img
                                                            src="/vuexy/images/portrait/small/avatar-s-7.jpg"
                                                            alt="avatar"
                                                            height="36"
                                                            width="36"
                                                    >
                                                </span>
                        </div>
                        <div class="message__body">
                            <div class="message__content">
                                <p>I will purchase it for sure. 👍</p>
                            </div>
                        </div>
                    </div>
                    <!--Mine-->
                    <div class="message">
                        <div class="message__avatar">
                                                <span class="avatar box-shadow-1 cursor-pointer">
                                                    <img
                                                            src="/vuexy/images/portrait/small/avatar-s-11.jpg"
                                                            alt="avatar"
                                                            height="36"
                                                            width="36"
                                                    >
                                                </span>
                        </div>
                        <div class="message__body">
                            <div class="message__content">
                                <p>Thanks, from ThemeForest.</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="input">
                    <form>
                        <div class="input-group input-group-merge mr-1">
                            <input name="message" type="text" class="form-control message"
                                   placeholder="Enter message...">
                            <div class="input-group-append">
                                <span class="input-group-text">
                                    <label for="attach-doc" class="attachment-icon mb-0">
                                        <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="14"
                                                height="14"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                class="feather feather-image cursor-pointer lighten-2 text-secondary"
                                        >
                                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                            <polyline points="21 15 16 10 5 21"></polyline>
                                        </svg>
                                        <input name="image" type="file" id="attach-doc" hidden="">
                                    </label>
                                </span>
                            </div>
                        </div>
                        <button
                                type="button"
                                class="btn btn-primary send waves-effect waves-float waves-light"
                        >
                            <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="14"
                                    height="14"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="feather feather-send d-lg-none"
                            >
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                            <span class="d-none d-lg-block">Send</span>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>