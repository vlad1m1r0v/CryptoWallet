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
        background: #F8F8F8;
    }

    #chat {
        grid-area: chat;
        min-height: 0;
        display: grid;
        grid-template-rows: 1fr auto;
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

    .message__content .message__image img {
        width: 100%;
        margin-top: 0.5rem;
        border-radius: 0.357rem;
    }

    .message_left .message__date {
        text-align: right;
    }

    .message__date small {
        font-size: 10px;
    }

    #input {
        grid-area: input;
        border-top: 1px solid #ebe9f1;
        padding: 0.75rem;
    }

    #input form {
        background-color: #fff;
        display: flex;
        align-items: center;
        flex-grow: 1;
    }

    svg.error {
        stroke: #ea5455 !important;
    }

    svg.success {
        stroke: #28c76f !important;
    }

    span.error, span.error:focus {
        border-color: #ea5455 !important;
    }

    span.success, span.success:focus {
        border-color: #28c76f !important;
    }


    #input .btn span {
        white-space: nowrap;
    }
</style>
<script lang="ts">
    import {PUBLIC_SOCKET_URL} from "$env/static/public";

    import {goto} from "$app/navigation";

    import {onMount, tick} from "svelte";
    import {get} from "svelte/store";

    import {io, type Socket} from "socket.io-client";

    import {toast} from "svelte-sonner";

    import {createForm} from "felte";
    import {validator} from "@felte/validator-zod";
    import {reporter} from "@felte/reporter-svelte";

    import {z} from "zod";

    import {formatDate} from "$lib/utils/date.ts";

    import {createMessageSchema} from "$lib/schemas/createMessage.ts";

    import {user} from "$lib/stores/user.ts";

    import ChevronUp from "$lib/components/icons/ChevronUp.svelte";
    import ChevronDown from "$lib/components/icons/ChevronDown.svelte";
    import TokenService from "$lib/services/token.ts";


    interface User {
        id: string;
        username: string;
        avatar_url?: string;
    }

    interface Message {
        id: string;
        text: string;
        image_url?: string;
        user: User;
        created_at: string;
    }

    let containerElement: HTMLDivElement;
    let chatElement: HTMLDivElement;

    let isAccordionOpen = $state<boolean>(false);
    let isChatContainerSmall = $state<boolean>(false);

    let socket = $state<Socket>();
    let connectedUsers = $state<User[]>([]);
    let messages = $state<Message[]>([]);


    onMount(() => {
        socket = io(PUBLIC_SOCKET_URL + "/chat", {
            transports: ["websocket"],
            auth: {token: TokenService.getToken()},
            autoConnect: false
        });

        socket?.on("list_users", (users: User[]) => {
            connectedUsers = users;
        });

        socket?.on("join_chat", (user: User) => {
            connectedUsers = [...connectedUsers, user];
        });

        socket?.on("leave_chat", (data: { id: string }) => {
            connectedUsers = connectedUsers.filter(u => u.id !== data.id);
        });

        socket?.on("list_messages", async (data: Message[]) => {
            messages = data;
            await tick();
            chatElement.scrollTo({
                top: chatElement.scrollHeight,
                behavior: "smooth"
            });
        })

        socket?.on("send_message", async (data: Message) => {
            messages = [...messages, data];
            await tick();
            chatElement.scrollTo({
                top: chatElement.scrollHeight,
                behavior: "smooth"
            });
        });

        socket?.on("increment_total_messages", async () => {
            user.update(u => (u ? {...u, total_messages: u.total_messages + 1} : u))
        })

        socket?.connect();

        return () => {
            socket?.disconnect();
        }
    });

    onMount(() => {
        const roContainer = new ResizeObserver(entries => {
            for (const entry of entries) {
                isChatContainerSmall = entry.contentRect.width < 934;
            }
        });


        const roScroll = new ResizeObserver(() => {
            setTimeout(() => {
                chatElement.scrollTo({
                    top: chatElement.scrollHeight,
                    behavior: "smooth",
                });
            }, 300)
        });


        roContainer.observe(containerElement);
        roScroll.observe(chatElement);

        return () => {
            roContainer.disconnect();
            roScroll.disconnect();
        };
    });

    user.subscribe((u) => {
        if (u) {
            if (!u.permissions.has_chat_access) {
                toast.error("You don't have access to chat.");
                goto("/profiles/me");
            }
        }
    });

    type FormData = z.infer<typeof createMessageSchema>;

    const toBase64 = (file: File) => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
    });

    const {form, reset, errors, touched, isSubmitting, isValid} = createForm<FormData>({
        onSubmit: async (values) => {
            const user_id = get(user)?.id;

            if (!user_id) return;

            const message: {
                user_id: string;
                text: string;
                image?: string;
            } = {
                "user_id": user_id,
                "text": values.text
            };

            if (values.image) {
                message["image"] = (await toBase64(values.image)) as string;
            }

            socket?.emit("create_message", message);
            reset();
        },
        extend: [
            validator({schema: createMessageSchema}),
            reporter()
        ]
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
                {#each connectedUsers as user (user.id)}
                    <a href={`profiles/${user.id}`}>
                        <div class="user">
                            <span class="avatar">
                                {#if user.avatar_url}
                                    <img
                                            src={user.avatar_url}
                                            height="42"
                                            width="42"
                                            alt="avatar"
                                    >
                                    {:else}
                                        <img
                                                src="/vuexy/images/portrait/small/avatar-s-11.jpg"
                                                height="42"
                                                width="42"
                                                alt="avatar"
                                        >
                                    {/if}
                                <span class="avatar-status-online"></span>
                            </span>
                            <h5 class="ml-1 mb-0">{user.username}</h5>
                        </div>
                    </a>
                {/each}
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
                    {#each connectedUsers as user (user.id)}
                        <a href={`profiles/${user.id}`}>
                            <div class="user">
                            <span class="avatar">
                                {#if user.avatar_url}
                                    <img
                                            src={user.avatar_url}
                                            height="42"
                                            width="42"
                                            alt="avatar"
                                    >
                                    {:else}
                                        <img
                                                src="/vuexy/images/portrait/small/avatar-s-11.jpg"
                                                height="42"
                                                width="42"
                                                alt="avatar"
                                        >
                                    {/if}
                                <span class="avatar-status-online"></span>
                            </span>
                                <h5 class="ml-1 mb-0">{user.username}</h5>
                            </div>
                        </a>
                    {/each}
                </div>
            </div>
            <div id="chat">
                <div id="messages" bind:this={chatElement}>
                    {#each messages as message (message.id)}
                        <div
                                class="message"
                                class:message_left={$user?.id !== message.user.id}
                        >
                            <a href={`profiles/${message.user.id}`}>
                                <div class="message__avatar">
                                                <span class="avatar box-shadow-1 cursor-pointer">
                                                    {#if message.user.avatar_url}
                                                        <img
                                                                src={message.user.avatar_url}
                                                                alt="avatar"
                                                                height="36"
                                                                width="36"
                                                        >
                                                    {:else}
                                                        <img
                                                                src="/vuexy/images/portrait/small/avatar-s-11.jpg"
                                                                alt="avatar"
                                                                height="36"
                                                                width="36"
                                                        >
                                                    {/if}
                                                </span>
                                </div>
                            </a>
                            <div class="message__body">
                                <div class="message__content">
                                    <div class="message__date">
                                        <small>{formatDate(message.created_at)}</small>
                                    </div>
                                    <p>{message.text}</p>
                                    {#if message.image_url}
                                        <div class="message__image">
                                            <img src={message.image_url} alt="image">
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
                <div id="input">
                    <div class="flex-grow-1">
                        <form use:form>
                            <div class="input-group input-group-merge mr-1">
                                <input
                                        name="text"
                                        type="text"
                                        class="form-control"
                                        placeholder="Enter message..."
                                        class:is-valid={!$errors.text && $touched.text}
                                        class:is-invalid={$errors.text && $touched.text}
                                >
                                <div
                                        class="input-group-append"
                                >
                                <span
                                        class="input-group-text"
                                        class:error={$errors.text && $touched.text}
                                        class:success={!$errors.text && $touched.text}
                                >
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
                                                class:is-valid={!$errors.text && $touched.text}
                                                class:is-invalid={$errors.text && $touched.text}
                                        >
                                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                            <polyline points="21 15 16 10 5 21"></polyline>
                                        </svg>
                                        <input
                                                name="image"
                                                type="file"
                                                id="attach-doc"
                                                hidden=""
                                        >
                                    </label>
                                </span>
                                </div>
                            </div>
                            <button
                                    type="submit"
                                    class="btn btn-primary send waves-effect waves-float waves-light"
                                    disabled={$isSubmitting || !$isValid}
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
                        {#if $touched.text && $errors.text}
                            <div class="invalid-feedback d-block h-auto">{$errors.text[0]}</div>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>