<div class="wrapper">
    <span />
</div>

<style>
    .wrapper {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 10rem;
        width: 10rem;
        border-radius: 50%;
        box-shadow: inset -10px -10px 15px rgba(255, 255, 255, 1),
            inset 10px 10px 10px rgba(0, 0, 0, 0.1);
    }
    .wrapper::before {
        content: "";
        position: absolute;
        height: 7rem;
        width: 7rem;
        border-radius: 50%;
        box-shadow: -10px -10px 15px rgba(255, 255, 255, 1),
            10px 10px 10px rgba(0, 0, 0, 0.1);
    }
    span {
        height: 10rem;
        width: 1rem;
        position: absolute;
        animation: rotate 5s linear infinite;
    }
    @keyframes rotate {
        100% {
            transform: rotate(360deg);
        }
    }
    span::before {
        content: "";
        position: absolute;
        height: 1.5rem;
        border-radius: 50%;
        width: 1.5rem;
        background: linear-gradient(45deg, #336dff, #5c89ff);
        box-shadow: 0 5px 10px rgb(0 0 0 / 30%);
    }
</style>
