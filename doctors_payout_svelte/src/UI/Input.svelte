<script>
    export let isPassword = false;
    export let placeholder = "";
    export let value = "";
    export let name = "";
</script>

{#if isPassword}
    <input type="password" {name} {placeholder} bind:value />
{:else}
    <input type="text" {name} {placeholder} bind:value />
{/if}

<style>
    input[type="text"],
    input[type="password"] {
        width: 30rem;
        padding: 1rem;
        margin-bottom: 20px;
        border: none;
        background-color: #e0e5ec;
        box-shadow: 5px 5px 10px #cbced1, -5px -5px 10px #ffffff;
        border-radius: 10px;
        font-size: 1.4rem;
        transition: box-shadow 0.3s ease-in-out;
        color: #0984e3;
    }

    input[type="text"]:focus,
    input[type="password"]:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.3), 5px 5px 10px #cbced1,
            -5px -5px 10px #ffffff;
    }

    input[type="text"]::placeholder,
    input[type="password"]::placeholder {
        color: #a6adb9;
    }

    input[type="text"]:hover,
    input[type="password"]:hover {
        box-shadow: 5px 5px 10px rgba(61, 97, 255, 0.6),
            -5px -5px 10px rgba(255, 255, 255, 0.5);
    }

    input[type="text"]:hover:focus,
    input[type="password"]:hover:focus {
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.3), 6px 6px 12px #cbced1,
            -6px -6px 12px #ffffff;
    }
</style>
