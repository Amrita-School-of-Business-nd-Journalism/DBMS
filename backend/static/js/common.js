async function logout() {

    const response = await fetch("/logout");

    const data = await response.json();

    console.log(data);

    if (data.success) {
        window.location.href = "/";
    }
}