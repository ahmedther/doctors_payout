<script>
    import { onMount } from "svelte";
    import Login from "../Components/Login.svelte";
    import Footer from "../UI/Footer.svelte";
    import Spinner from "../UI/Spinner.svelte";
    import Overlay from "../UI/Overlay.svelte";
    import Main from "../Components/Main.svelte";
    let userName = null;
    let userID = null;
    let authToken = null;
    let isLoading = true;

    function handelAuth(e) {
        if (!e.detail.userName) return;
        userName = e.detail.userName;
        authToken = e.detail.authToken;
        userID = e.detail.userID;
        const expirationDate = new Date();
        expirationDate.setTime(expirationDate.getTime() + 60 * 60 * 1000); // Set the expiration to 1 hour from now
        document.cookie = `userName=${userName}; expires=${expirationDate.toUTCString()}; path=/`;
        document.cookie = `authToken=${authToken}; expires=${expirationDate.toUTCString()}; path=/`;
        document.cookie = `userID=${userID}; expires=${expirationDate.toUTCString()}; path=/`;
        document.cookie = `emailId=${
            e.detail.emailId
        }; expires=${expirationDate.toUTCString()}; path=/`;
    }

    onMount(() => {
        const cookies = document.cookie.split("; ");
        for (const cookie of cookies) {
            const [name, value] = cookie.split("=");
            if (name === "userName") {
                userName = value;
            } else if (name === "authToken") {
                authToken = value;
            }
        }

        isLoading = false;
    });
</script>

<div class="main-container">
    {#if isLoading}<Overlay /><Spinner />
    {:else if !userName}
        <section>
            <Login on:authenticated={handelAuth} />
        </section>
    {:else}
        <main>
            <Main on:logout={(_) => (userName = null)} {userName} />
        </main>
    {/if}

    <footer>
        <Footer />
    </footer>
</div>

<style>
    .main-container {
        background-color: #e0e5ec;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }
    section {
        align-self: center;
        height: calc(99vh - 1vh);
        display: flex;
        align-items: center;
    }

    main {
        width: 100%;
    }
</style>
