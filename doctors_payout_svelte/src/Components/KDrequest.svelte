<script>
    import { sendExcelAndForms } from "../js/helper.js";
    import KHForm from "./KDForm.svelte";
    import Spinner from "../UI/Spinner.svelte";
    import Overlay from "../UI/Overlay.svelte";
    import SuccessPage from "./SuccessPage.svelte";

    let isLoading = false;
    let error = false;
    let errorMessage = null;
    let successPage = false;
    let emailId = null;

    async function submitRequest(e) {
        isLoading = true;
        error = false;
        errorMessage = null;
        const formData = new FormData();
        formData.append("rh_data", e.detail.rhData);
        formData.append("transplantData", e.detail.transplantData);
        formData.append("from_date", e.detail.from_date);
        formData.append("to_date", e.detail.to_date);
        formData.append("userID", e.detail.userID);
        const message = await sendExcelAndForms(formData);
        console.log(message);
        if (message.error) {
            errorMessage = message.error;
            error = true;
        }
        if (message.success) {
            emailId = message.email_Id;
            successPage = true;
        }
        isLoading = false;
    }
</script>

{#if isLoading}
    <div class="gs-neumorphic-main-card-outer-container">
        <div class="gs-neumorphic-main-card-container">
            <Overlay />
            <Spinner />
        </div>
    </div>
{:else if successPage}
    <SuccessPage on:logout {emailId} />
{:else}
    <KHForm on:submit={submitRequest} {errorMessage} {error} />
{/if}

<style>
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
</style>
