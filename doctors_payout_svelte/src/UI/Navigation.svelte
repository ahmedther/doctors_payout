<script>
    import { Feather } from "sveltekit-feather-icons";
    import { createEventDispatcher } from "svelte";
    export let userName;
    export let activeItem = "home";

    const dispatch = createEventDispatcher();

    function handelHomeClick() {
        activeItem = "home";
        dispatch("nav", activeItem);
    }

    function handelDownloadClick() {
        activeItem = "download";
        dispatch("nav", activeItem);
    }

    function logout() {
        // Clear the "userName" cookie
        document.cookie =
            "userName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

        // Clear the "authToken" cookie
        document.cookie =
            "authToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie =
            "user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

        dispatch("logout");
    }
</script>

<ul class="nav">
    <li class="logo">Doctor's Payout K.D</li>
    <li class="logo user-name">Welcome! {userName}</li>
    <li
        on:click={handelHomeClick}
        class={activeItem === "home" ? "active" : ""}
    >
        <Feather icon="home" />
    </li>
    <li
        on:click={handelDownloadClick}
        class={activeItem === "download" ? "active" : ""}
    >
        <Feather icon="download" />
    </li>
    <li on:click={logout}>
        <Feather icon="log-out" />
    </li>
</ul>

<style>
    .nav {
        width: 98vw;
        height: 3rem;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0 3rem;
        list-style-type: none;
        background-color: #e4ebf5;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 10px 10px 20px #cbced1, -10px -10px 20px #ffffff;
    }
    .nav li.logo {
        margin-right: auto;
        font-family: "Roboto", sans-serif;
        font-size: 1.8rem;
        color: dimgray;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3), -2px -2px 4px white;
    }
    .nav li:not(.logo) {
        margin: 0 1rem;
        padding: 0.5rem 1.5rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 4px 4px 6px 0 rgba(0, 0, 0, 0.1), -4px -4px 6px white;
        border-radius: 10px;
        font-family: "Roboto", sans-serif;
        cursor: pointer;
        transition: color 0.2s ease-out, transform 0.2s ease-out;
        color: dimgray;
    }
    .nav li:not(.logo):hover {
        transform: scale(1.05);
        box-shadow: 4px 4px 10px 0 rgba(0, 0, 0, 0.1), -4px -4px 10px white;
    }
    .nav li:not(.logo):focus {
        outline: none;
        transform: scale(0.95);
        box-shadow: 4px 4px 10px 0 rgba(0, 0, 0, 0.1), -4px -4px 10px white,
            4px 4px 10px 0 rgba(0, 0, 0, 0.1) inset, -4px -4px 10px white inset;
    }
    .nav li:not(.logo):hover,
    .nav li:not(.logo):focus {
        color: rgb(0, 123, 255);
    }
    .nav li:not(.logo).active {
        color: rgb(0, 123, 255);
    }
    .nav li.logo.user-name {
        color: rgb(0, 60, 255);
        font-size: 1.4rem;
    }
</style>
