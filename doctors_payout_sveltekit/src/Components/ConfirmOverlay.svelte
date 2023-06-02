<script>
    import { createEventDispatcher } from "svelte";
    export let ConfirmMessage;

    const dispatch = createEventDispatcher();

    function customDispatch(_, type) {
        dispatch(type);
    }
</script>

<div
    class="overlay"
    on:click={(e) => {
        customDispatch(e, "cancel");
    }}
>
    <div class="modal">
        <h2 class="gs-neumorphic-signup-login-header">Confirmation</h2>
        <p class="date-label">{ConfirmMessage}</p>
        <div class="btn-cont">
            <button
                on:click={(e) => {
                    customDispatch(e, "confirm");
                }}
                class="gs-neumorphic-button confim-btn">Confirm</button
            >
            <button
                on:click={(e) => {
                    customDispatch(e, "cancel");
                }}
                class="gs-neumorphic-button cancel-btn">Cancel</button
            >
        </div>
    </div>
</div>

<style>
    :root {
        --lightGrey-gs-neumorphic-login-signup: #c8d0e7;
        --lightGrey2-gs-neumorphic-login-signup: #e4ebf5;
        --header-colors-gs-neumorphic-login-signup: rgb(0, 60, 255);
        --header-font-size-gs-neumorphic-login-signup: 25px;
        --header-scale-open-gs-neumorphic-login-signup: 1.5;
        --card-open-close-tansition-time-gs-neumorphic-login-signup: 1s;
        --form-input-border-radius-gs-neumorphic-login-signup: 5px;
        --form-input-padding-gs-neumorphic-login-signup: 10px;
        --form-input-font-size-gs-neumorphic-login-signup: 15px;
        --form-input-font-color--gs-neumorphic-login-signup: #9baacf;
        --form-input-margin-gs-neumorphic-login-signup: 15px;
        --form-input-max-width-gs-neumorphic-login-signup: 300px;
    }
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }

    .modal {
        background-color: #e4ebf5;
        border-radius: 10px;
        padding: 3rem;
        max-width: 500px;
        width: 90%;
        text-align: center;
    }

    .gs-neumorphic-signup-login-header {
        text-transform: uppercase;
        color: var(--header-colors-gs-neumorphic-login-signup);
        cursor: pointer;
        font-size: 2.8rem;
        font-weight: bold;
        transition: var(
                --card-open-close-tansition-time-gs-neumorphic-login-signup
            )
            ease-in-out;
        padding: 3rem;
    }

    .date-label {
        padding: 0.5rem;
        color: var(--form-input-font-color--gs-neumorphic-login-signup);
        font-size: 2.2rem;
        font-weight: 500;
        align-self: flex-start;
        padding-bottom: 0;
    }

    .btn-cont {
        padding-top: 2rem;
        display: flex;
        gap: 3rem;
        align-items: center;
        justify-content: center;
    }

    .gs-neumorphic-button {
        width: max-content;
        padding: var(--form-input-padding-gs-neumorphic-login-signup)
            calc(var(--form-input-padding-gs-neumorphic-login-signup) * 2.5);
        margin-top: var(--form-input-margin-gs-neumorphic-login-signup);
        margin-bottom: var(--form-input-margin-gs-neumorphic-login-signup);
        border: none;
        border-radius: var(
            --form-input-border-radius-gs-neumorphic-login-signup
        );
        box-shadow: 0.3rem 0.3rem 0.6rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 0.5rem white;
        cursor: pointer;
        transition: var(
                --card-open-close-tansition-time-gs-neumorphic-login-signup
            )
            ease;
        color: var(--form-input-font-color--gs-neumorphic-login-signup);
        background-color: var(--lightGrey2-gs-neumorphic-login-signup);
        font-size: var(--form-input-font-size-gs-neumorphic-login-signup);
    }

    .gs-neumorphic-button:hover.confim-btn {
        font-weight: bold;
        color: #55efc4;
    }
    .gs-neumorphic-button:hover {
        font-weight: bold;
        color: #d63031;
    }

    .gs-neumorphic-button:active {
        box-shadow: inset 0.2rem 0.2rem 0.5rem
                var(--lightGrey-gs-neumorphic-login-signup),
            inset -0.2rem -0.2rem 0.5rem white;
    }

    .gs-neumorphic-button:focus {
        outline: none;
        color: var(--header-colors-gs-neumorphic-login-signup);
    }
</style>
