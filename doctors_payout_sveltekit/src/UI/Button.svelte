<script>
    export let value = "";
</script>

<input type="submit" {value} class="submit-button" on:click />

<style>
    .submit-button {
        width: 100px;
        padding: 10px;
        border: none;
        background-color: #4a74a5;
        color: #ffffff;
        border-radius: 10px;
        cursor: pointer;
        font-size: 1.3rem;
        font-weight: 600;
    }

    .submit-button:hover {
        background-color: #375e85;
    }
</style>
