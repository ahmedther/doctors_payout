<script>
    import { createEventDispatcher } from "svelte";
    import { makeAuthRequest } from "../js/helper.js";

    import LoginForm from "./LoginForm.svelte";
    import Spinner from "../UI/Spinner.svelte";
    import Overlay from "../UI/Overlay.svelte";

    let errorMessage = null;
    let error = false;
    let isLoading = false;
    const dispatch = createEventDispatcher();

    async function handleSubmit(e) {
        isLoading = true;
        error = false;
        errorMessage = null;
        const data = await makeAuthRequest(e.detail);
        if (data.error) {
            errorMessage = data.error;
            error = true;
            isLoading = false;
            return;
        }
        dispatch("authenticated", {
            userName: data.success,
            authToken: data.token,
            userID: data.user_id,
        });
        isLoading = false;
    }
</script>

{#if isLoading}
    <Overlay />
    <Spinner />
{:else}
    <div class="container">
        <h1>Doctor's Payout K.D</h1>

        <LoginForm on:submit={handleSubmit} {errorMessage} {error} />
    </div>
{/if}

<style>
    .container {
        background-color: #e0e5ec;
        border-radius: 20px;
        padding: 4rem;
        box-shadow: 10px 10px 20px #cbced1, -10px -10px 20px #ffffff;
    }

    h1 {
        text-align: center;
        color: #555555;
        font-family: "Roboto", sans-serif;
        font-size: 2.2rem;
        margin-bottom: 4rem;
    }
</style>
