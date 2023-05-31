<script>
    import { createEventDispatcher } from "svelte";
    import Input from "../UI/Input.svelte";
    import Button from "../UI/Button.svelte";

    export let error = false;
    export let errorMessage = null;

    let username;
    let password;

    const dispatch = createEventDispatcher();

    function errordisplay() {
        if (!errorMessage) return;
        const message = errorMessage;
        errorMessage = "";

        let index = 0;
        const typeErrorMessage = () => {
            if (index < message.length) {
                errorMessage += message.charAt(index);
                index++;

                setTimeout(typeErrorMessage, 50);
            }
        };
        typeErrorMessage();
        let rIndex = message.length;
        const removeErrorMessage = () => {
            if (rIndex > 0) {
                errorMessage = errorMessage.slice(0, -1);
                rIndex--;
                setTimeout(removeErrorMessage, 20);
            } else {
                error = false;
                errorMessage = null;
            }
        };
        setTimeout(() => {
            removeErrorMessage();
        }, 5000);
    }

    $: if (error) {
        errordisplay();
    }
</script>

<form
    on:submit|preventDefault={() => {
        if ((username.length === 0) | (password.length === 0)) {
            error = true;
            errorMessage = "Username or Password Cannot Be empty";
            return;
        }
        dispatch("submit", { username, password });
    }}
>
    <Input
        isPassword={false}
        name="username"
        placeholder="Username"
        bind:value={username}
    />
    <Input
        isPassword={true}
        name="password"
        placeholder="Password"
        bind:value={password}
    />
    {#if errorMessage}
        <p class="error-message">{errorMessage}</p>
    {/if}

    <Button value="Submit" />
</form>

<style>
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .error-message {
        color: red;
        font-size: 14px;
        margin-bottom: 10px;
        max-width: 30rem;
        text-align: center;
    }
</style>
