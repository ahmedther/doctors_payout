<script>
    import { Feather } from "sveltekit-feather-icons";
    import { createEventDispatcher } from "svelte";

    export let emailId;

    const dispatch = createEventDispatcher();

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

<div class="fullpage">
    <div class="success-message">
        <div class="success-icon">
            <i class="fas fa-check-circle"
                ><Feather icon="check-circle" size="133" /></i
            >
        </div>
        <h2 class="success-title">Success!</h2>
        <p class="success-message-text">
            Thank you for submitting your request. Your request has been
            received and is currently being processed. Once the process is
            complete, we will send you the Excel file to the email address
            registered with us. You may now proceed to close the current page. <br
            />
        </p>
        <a
            class="success-message-text"
            href="/"
            on:click|preventDefault={logout}>Click Here to Logout</a
        >
        <p class="success-email">
            Registered email: {emailId ? emailId : "john@example.com"}
        </p>
    </div>
</div>

<style>
    :root {
        --lightGrey-gs-neumorphic-login-signup: #c8d0e7;
        --lightGrey2-gs-neumorphic-login-signup: #e4ebf5;
        --header-colors-gs-neumorphic-login-signup: rgb(0, 60, 255);
        --form-input-font-color--gs-neumorphic-login-signup: #9baacf;
    }

    * {
        margin: 0;
    }
    a,
    a:visited {
        margin-top: 2rem;
        color: #d63031;
    }
    .success-message {
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100rem;
        background-color: var(--lightGrey2-gs-neumorphic-login-signup);
        box-shadow: 0.8rem 0.8rem 1.4rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 1.8rem #ffffff;
        border-radius: 1rem;
        font-weight: bold;
        padding: 5rem;
        text-align: center;
        gap: 1rem;
    }

    .success-icon {
        font-size: 5rem;
        color: #00b894;
    }

    .success-title {
        font-size: 7.2rem;
    }

    .success-message-text {
        font-size: 2rem;
    }

    .success-email {
        margin: 3rem;
        font-size: 2rem;
        color: #00b894;
    }
</style>
