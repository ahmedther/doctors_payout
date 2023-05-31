<script>
    import { Feather } from "sveltekit-feather-icons";
    import { createEventDispatcher } from "svelte";
    import { getUserID } from "../js/helper.js";
    export let error = false;
    export let errorMessage = null;

    let from_date;
    let to_date;
    let rhData;
    let rhDataFileName;
    let transplantData;
    let transplantFileName;

    const dispatch = createEventDispatcher();

    function handleFileChange(event) {
        if (event.target.id === "rh_data") {
            const file = event.target.files[0];
            rhData = file;
            rhDataFileName = file ? file.name : "";
        }

        if (event.target.id === "transplantData") {
            const file1 = event.target.files[0];
            transplantData = file1;
            transplantFileName = file1 ? file1.name : "";
        }
    }

    function inputValidation() {
        if (
            !from_date ||
            !to_date ||
            isNaN(Date.parse(from_date)) ||
            isNaN(Date.parse(to_date))
        ) {
            errorMessage = "Dates Are Left Empty. Please Select Valid Dates.";
            error = true;
            return false;
        }

        // Check if rhData is an Excel file
        if (!rhData) {
            errorMessage =
                "Please attach a valid Excel file for RH Navi Mumbai Data.";
            error = true;
            return false;
        }

        // Check if transplantData is an Excel file
        if (!transplantData) {
            errorMessage =
                "Please attach a valid Excel file for Transplant Data.";
            error = true;
            return false;
        }
        const userID = getUserID();
        dispatch("submit", {
            from_date,
            to_date,
            rhData,
            transplantData,
            userID,
        });
    }
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
        }, 9000);
    }

    $: if (error) {
        errordisplay();
    }
</script>

<div class="gs-neumorphic-main-card-outer-container">
    <div class="gs-neumorphic-main-card-container">
        <div class="gs-neumorphic-main-card">
            <div class="gs-neumorphic-signup gs-form-open">
                <div
                    class="gs-neumorphic-signup-login-header gs-open"
                    data-button="gs-neumorphic-signup"
                >
                    Request For Doctor's Payout K.D
                </div>
                <div class="gs-neumorphic-form-container">
                    <form on:submit|preventDefault={inputValidation}>
                        <div class="with-label">
                            <label for="from_date" class="date-label"
                                >From Date <Feather
                                    icon="calendar"
                                    size="13"
                                /></label
                            >
                            <input
                                type="date"
                                name="from_date"
                                id="from_date"
                                class="gs-neumorphic-input date-input"
                                placeholder="First Name"
                                bind:value={from_date}
                            />
                        </div>
                        <div class="with-label">
                            <label for="to_date" class="date-label"
                                >To Date <Feather icon="calendar" size="13" />
                            </label>
                            <input
                                type="date"
                                name="to_date"
                                id="to_date"
                                class="gs-neumorphic-input date-input"
                                placeholder="First Name"
                                bind:value={to_date}
                            />
                        </div>

                        <input
                            type="file"
                            name="rh_data"
                            id="rh_data"
                            bind:value={rhData}
                            style="display: none;"
                            on:change={handleFileChange}
                        />
                        <label for="rh_data" class="gs-neumorphic-input">
                            {rhData
                                ? rhDataFileName + " "
                                : "RH Navi Mumbai Excel File"}
                            <Feather icon="upload" size="11" />
                        </label>

                        <input
                            type="file"
                            name="transplantData"
                            id="transplantData"
                            bind:value={transplantData}
                            style="display: none;"
                            on:change={handleFileChange}
                        />
                        <label for="transplantData" class="gs-neumorphic-input">
                            {transplantData
                                ? transplantFileName + " "
                                : "Transplant Excel File "}
                            <Feather icon="upload" size="11" />
                        </label>

                        {#if errorMessage}
                            <p class="error-message">{errorMessage}</p>
                        {/if}

                        <button class="gs-neumorphic-button">Request</button>
                    </form>
                </div>
            </div>
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

    * {
        margin: 0;
    }

    .with-label {
        display: flex;
        flex-direction: column;
        margin: auto;
        max-width: var(--form-input-max-width-gs-neumorphic-login-signup);
    }

    .date-label {
        padding: 0.5rem;
        color: var(--form-input-font-color--gs-neumorphic-login-signup);
        font-size: 1.4rem;
        font-weight: 500;
        align-self: flex-start;
        padding-bottom: 0;
    }

    .date-input {
        min-width: var(--form-input-max-width-gs-neumorphic-login-signup);
        margin-top: 0.5rem !important;
    }

    .gs-neumorphic-main-card-outer-container {
        height: 95vh;
        background-color: #e4ebf5;
        display: flex;
        margin-top: 3vh;
    }

    .gs-neumorphic-main-card-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: auto;
    }

    .gs-neumorphic-main-card-container .gs-neumorphic-main-card {
        width: 100%;
        height: 80%;
        position: relative;
        overflow: hidden;
        box-shadow: 0.8rem 0.8rem 1.4rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 1.8rem #ffffff;
        border-radius: 1rem;
        font-weight: bold;
        background-color: var(--lightGrey2-gs-neumorphic-login-signup);
    }

    @media only screen and (min-width: 320px) {
        .gs-neumorphic-main-card-container .gs-neumorphic-main-card {
            width: 90%;
        }
    }
    @media only screen and (min-width: 540px) {
        .gs-neumorphic-main-card-container .gs-neumorphic-main-card {
            width: 70%;
        }
    }
    @media only screen and (min-width: 800px) {
        .gs-neumorphic-main-card-container .gs-neumorphic-main-card {
            width: 60%;
        }
    }
    @media only screen and (min-width: 900px) {
        .gs-neumorphic-main-card-container .gs-neumorphic-main-card {
            width: 30%;
        }
    }
    @media only screen and (min-width: 1900px) {
        .gs-neumorphic-main-card-container .gs-neumorphic-main-card {
            width: 30%;
        }
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-signup {
        height: 85%;
        width: 100%;
        text-align: center;
        background-color: var(--lightGrey2-gs-neumorphic-login-signup);
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-signup-login-header {
        text-transform: uppercase;
        color: var(--header-colors-gs-neumorphic-login-signup);
        cursor: pointer;
        font-size: 1.4rem;
        font-weight: bold;
        transition: var(
                --card-open-close-tansition-time-gs-neumorphic-login-signup
            )
            ease-in-out;
        padding: 3rem;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-signup-login-header.gs-open {
        transform: scale(var(--header-scale-open-gs-neumorphic-login-signup));
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container {
        width: 100%;
        visibility: hidden;
        opacity: 0;
        transition: var(
                --card-open-close-tansition-time-gs-neumorphic-login-signup
            )
            ease-in-out;
        height: 80%;
        overflow: auto;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-form-open
        .gs-neumorphic-form-container {
        visibility: visible;
        opacity: 1;
        padding-bottom: 20px;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
        .gs-neumorphic-input {
        width: calc(100% - 50px);
        border: none;
        border-radius: var(
            --form-input-border-radius-gs-neumorphic-login-signup
        );
        padding: var(--form-input-padding-gs-neumorphic-login-signup);
        box-shadow: inset 0.1rem 0.1rem 0.3rem
                var(--lightGrey-gs-neumorphic-login-signup),
            inset -0.1rem -0.1rem 0.3rem white;
        background: none;
        color: var(--form-input-font-color--gs-neumorphic-login-signup);
        margin: var(--form-input-margin-gs-neumorphic-login-signup) auto;
        font-size: var(--form-input-font-size-gs-neumorphic-login-signup);
        max-width: var(--form-input-max-width-gs-neumorphic-login-signup);
        display: block;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
        .gs-neumorphic-input::placeholder {
        color: var(--form-input-font-color--gs-neumorphic-login-signup);
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
        .gs-neumorphic-input:focus {
        outline: none;
        box-shadow: 0.3rem 0.3rem 0.6rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 0.5rem white;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container::-webkit-scrollbar {
        width: 5px;
        -webkit-appearance: none;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container::-webkit-scrollbar-track {
        background: transparent;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container::-webkit-scrollbar-thumb {
        background-color: rgba(108, 121, 119, 0.44);
        border: 1px solid #fff;
        border-radius: 1rem;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
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

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
        .gs-neumorphic-button:hover {
        color: var(--header-colors-gs-neumorphic-login-signup);
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
        .gs-neumorphic-button:active {
        box-shadow: inset 0.2rem 0.2rem 0.5rem
                var(--lightGrey-gs-neumorphic-login-signup),
            inset -0.2rem -0.2rem 0.5rem white;
    }

    .gs-neumorphic-main-card-container
        .gs-neumorphic-main-card
        .gs-neumorphic-form-container
        .gs-neumorphic-button:focus {
        outline: none;
        color: var(--header-colors-gs-neumorphic-login-signup);
    }

    .error-message {
        color: red;
        font-size: 14px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
