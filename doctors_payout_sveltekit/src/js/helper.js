const DJANGO_BASE_URL = import.meta.env.VITE_DJANGO_BASE_URL;
console.log(DJANGO_BASE_URL);
export async function makeAuthRequest(detail) {
    const username = detail.username;
    const password = detail.password;

    try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(`${DJANGO_BASE_URL}/login/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                username,
                password,
            }),
            credentials: 'include', // Ensure cookies are sent with the request
        });

        if (!response.ok) {
            const data = await response.json();
            return data
        }

        const data = await response.json();
        return data
    } catch (error) {
        console.error(error)
        const data = { "error": `Connection Failed ! Error -- ${error.toString()}` }
        return data
    }
}


// Helper function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


export async function errordisplay(error, errorMessage) {
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
            const errorOBj = { "error": error }
            return errorOBj
        }
    };
    setTimeout(() => {
        removeErrorMessage();
    }, 5000);
}


export async function sendExcelAndForms(formData) {
    try {

        const response = await fetch(`${DJANGO_BASE_URL}/`, {
            method: 'POST',

            body: formData,
        });

        if (!response.ok) {
            const data = await response.json();
            return data
        }

        const data = await response.json();
        return data

    } catch (error) {
        const data = { "error": `Connection Failed ! Error -- ${error.toString()}` };
        return data;
    }
}


export function getCookieValue(serach_query) {
    const cookies = document.cookie.split(';');
    let query_value = null;

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(serach_query)) {
            query_value = cookie.substring(serach_query.length);
            break;
        }
    }
    return query_value;
}


export async function fetchFiles(page) {
    try {
        const response = await fetch(`${DJANGO_BASE_URL}/files/?page=${page}`, {
            method: "GET",
            credentials: "include", // Ensure cookies are sent with the request
        });
        if (!response.ok) {
            let data = await response.json();
            return data = { "error": `Connection Failed ! Error -- ${data.toString()}` };
        }

        const data = await response.json();
        return data

    } catch (error) {
        const data = { "error": `Connection Failed ! Error -- ${error.toString()}` };
        return data;
    }
}




export async function check_task_status() {
    try {
        const response = await fetch(`${DJANGO_BASE_URL}/check_task_status/`, {
            method: "GET",
            credentials: "include", // Ensure cookies are sent with the request
        });
        if (!response.ok) {
            let data = await response.json();
            return data = { "error": `Connection Failed ! Error -- ${data.toString()}` };
        }

        const data = await response.json();
        return data

    } catch (error) {
        const data = { "error": `Connection Failed ! Error -- ${error.toString()}` };
        return data;
    }
}

