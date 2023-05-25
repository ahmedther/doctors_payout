<script>
    import Navigation from "../UI/Navigation.svelte";
    import KDrequest from "./KDrequest.svelte";
    export let userName;

    let activeItem = "home";

    function handelNav(e) {
        activeItem = e.detail;
    }
</script>

<div class="navigation">
    <Navigation on:logout on:nav={handelNav} {userName} {activeItem} />
</div>

{#if activeItem == "home"}
    <section class="input-box" />
    <KDrequest on:logout />
{:else if activeItem == "download"}
    <p class="dow">Downlaod PAge</p>
{/if}

<style>
    .navigation {
        position: fixed;
        top: 0.1rem;
        width: 100%;
        padding: 10px;
        z-index: 9999;
        /* Add any other styling properties as needed */
    }
</style>
