const myform = document.getElementById("loginform");
myform.addEventListener('submit',async (event)=>{
    event.preventDefault();
    const formData = new FormData(event.target);
    const usertype = formData.get('typeofuser');
    const emailid = formData.get('email');
    const emailpassword = formData.get('emailpassword');
    const loginbutton = document.getElementById('login-btn');
    const responsetohtml = document.getElementById('response_login');
    loginbutton.innerHTML = '<strong>Logging in...</strong>';
    loginbutton.disabled = true;

    try {
        const flaskResponse = await fetch("/login",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                email:emailid,
                password:emailpassword,
                role:usertype
            })
        })

        const data = await flaskResponse.json();

        if(data.success){
            const loggedInRole = data.user.ROLE;
            console.log("Logged in as:", loggedInRole);
            responsetohtml.innerText = "Login successful as " + loggedInRole;
            responsetohtml.style.color = "green";
            if(loggedInRole === "CUSTOMER"){
                window.location.href = "/customer";
            }
            else if(loggedInRole === "VENDOR"){
                window.location.href = "/vendor";
            }
        }
        else{
            responsetohtml.innerText = data.message;
            responsetohtml.style.color = "red";
        }
        loginbutton.innerText = 'Login';
        loginbutton.disabled = false;
    }
    catch(error){
        console.error(error);
        responsetohtml.innerText = "Could not connect to the server";
        responsetohtml.style.color = "red";
    }
        loginbutton.innerText = 'Login';
        loginbutton.disabled = false;
});