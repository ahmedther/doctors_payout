<script>
    import { onMount } from "svelte";
    import { fetchFiles } from "../js/helper.js";
    import Spinner from "../UI/Spinner.svelte";
    import Overlay from "../UI/Overlay.svelte";
    import excelLogo from "../images/excel_logo.png";

    let isLoading = true;
    let files = [];
    let currentPage = 1;
    let numPages = 1;
    let error = "No Files found";

    async function goToPage(page) {
        isLoading = true;
        const data = await fetchFiles(page);
        if (data.error) {
            error = data.error;
            isLoading = false;
        }
        currentPage = data.current_page;
        numPages = data.num_pages;
        files = data.files;
        isLoading = false;
    }

    onMount(async () => {
        const data = await fetchFiles(1);
        if (data.error) {
            error = data.error;
            isLoading = false;
        }
        if (data.files) {
            currentPage = data.current_page;
            numPages = data.num_pages;
            files = data.files;
            isLoading = false;
        }
        isLoading = false;
    });
</script>

<div class="gs-neumorphic-main-card-outer-container">
    <div class="gs-neumorphic-main-card-container">
        {#if isLoading}
            <Overlay /><Spinner />
        {:else if files.length > 0}
            <div class="container">
                <div
                    class="gs-neumorphic-signup-login-header"
                    data-button="gs-neumorphic-signup"
                >
                    Download Old Files
                </div>
                <ul class="file-list">
                    {#each files as file}
                        <li>
                            <a
                                href={file.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                class="file-info"
                            >
                                <div class="file-icon">
                                    <img src={excelLogo} alt="File Icon" />
                                </div>
                                <div class="file-name">{file.name}</div>
                                <button class="download-button">Download</button
                                >
                            </a>
                        </li>
                    {/each}
                </ul>
                <div class="pagination">
                    <button
                        type="button"
                        class="download-button pagi"
                        on:click={() => goToPage(currentPage - 1)}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </button>

                    <!-- Page Numbers -->
                    {#each Array.from({ length: numPages }) as _, index}
                        {#if index + 1 >= currentPage - 2 && index + 1 <= currentPage + 2}
                            <button
                                type="button"
                                class={index + 1 === currentPage
                                    ? "active pagi"
                                    : "download-button pagi"}
                                on:click={() => goToPage(index + 1)}
                            >
                                {index + 1}
                            </button>
                        {/if}
                    {/each}

                    <!-- Next Button -->
                    <button
                        type="button"
                        class="download-button pagi"
                        on:click={() => goToPage(currentPage + 1)}
                        disabled={currentPage === numPages}
                    >
                        Next
                    </button>
                </div>
            </div>
        {:else}
            <div class="error-container">
                <p class="error">{error}</p>
            </div>
        {/if}
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
    a {
        text-decoration: none; /* Removes underline */
        color: inherit; /* Inherits the color from its parent */
    }
    img {
        max-height: 4rem;
    }
    .gs-neumorphic-main-card-outer-container {
        height: max-content;
        background-color: #e4ebf5;
        display: flex;
        padding: 10rem;
        width: 100%;
    }

    .gs-neumorphic-main-card-container {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: auto;
    }

    .error-container {
        height: 100%;
        max-width: 60vw;
    }

    .error {
        color: #d63031;
        font-size: 3rem;
    }

    .gs-neumorphic-signup-login-header {
        width: 100%;
        text-transform: uppercase;
        color: var(--header-colors-gs-neumorphic-login-signup);
        cursor: pointer;
        font-size: 1.6rem;
        font-weight: bold;
        transition: var(
                --card-open-close-tansition-time-gs-neumorphic-login-signup
            )
            ease-in-out;
        padding: 3rem;
        text-align: center;
    }

    .container {
        margin-top: 8vh;
        background-color: #e4ebf5;
        width: max-content;
        min-width: 50rem;
        max-width: 50rem;
        box-shadow: 0.8rem 0.8rem 1.4rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 1.8rem #ffffff;
        border-radius: 1rem;
        font-weight: bold;
        background-color: var(--lightGrey2-gs-neumorphic-login-signup);
        padding: 20px;
        font-size: 6.8rem;
    }

    .file-list {
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .file-list li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        border-radius: 10px;
        background-color: #e4ebf5;
        margin-bottom: 10px;
        box-shadow: 0.3rem 0.3rem 0.6rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 0.5rem white;
        width: 100%;
    }

    .file-list li .file-info {
        display: flex;
        align-items: center;
        gap: 2rem;
        width: 100%;
    }

    .file-list li .file-info .file-icon {
        height: 5rem;
        width: 5rem;
        background-color: #e4ebf5;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        box-shadow: 0.3rem 0.3rem 0.6rem
                var(--lightGrey-gs-neumorphic-login-signup),
            -0.2rem -0.2rem 0.5rem white;
    }

    .file-list li .file-info .file-name {
        color: var(--form-input-font-color--gs-neumorphic-login-signup);
        font-weight: bold;
        font-size: 1.4rem;
        transition: all 300ms;
    }
    .file-list li .file-info .file-name:hover {
        color: #00b894;
        font-weight: bold;
        font-size: 1.6rem;
    }

    .download-button,
    .active {
        margin-left: auto;
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
    .active {
        color: var(--header-colors-gs-neumorphic-login-signup);
        font-weight: 600;
        font-size: 1.6rem;
    }

    .download-button:hover {
        color: var(--header-colors-gs-neumorphic-login-signup);
    }

    .download-button:active {
        box-shadow: inset 0.2rem 0.2rem 0.5rem
                var(--lightGrey-gs-neumorphic-login-signup),
            inset -0.2rem -0.2rem 0.5rem white;
    }

    .download-button:focus {
        outline: none;
        color: var(--header-colors-gs-neumorphic-login-signup);
    }

    .pagination {
        margin-top: 2rem;
        width: 100%;
        display: flex;
        align-items: center;
        justify-items: center;
        justify-content: center;
        gap: 1rem;
    }
    .pagi {
        margin: 0;
    }
</style>
