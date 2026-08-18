const registerForm = document.getElementById("register-form")
const responseMessage = document.getElementById("responder")
registerForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const formData = new FormData(event.target);

    const data = {
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        phone_no: formData.get("phone_no"),
        password: formData.get("password"),
        role: formData.get("role")
    };

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    console.log("Flask response:", result);

    if(result.success){
        alert(result.message);
        window.location.href = "/";
    }
    else{
        responseMessage.innerText = result.message;
        responseMessage.style.color = "red";
    }

});