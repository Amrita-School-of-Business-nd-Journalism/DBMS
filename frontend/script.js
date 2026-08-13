const myform = document.getElementById("loginform");
myform.addEventListener('submit',(event)=>{
    event.preventDefault();
    const formData = new FormData(event.target);
    const usertype = formData.get('typeofuser');
    const emailid = formData.get('email');
    const emailpassword = formData.get('emailpassword');
    const loginbutton = document.getElementById('login-btn');
    const response = document.getElementById('response_login');
    console.log(usertype,emailid,emailpassword);
    loginloadingstate(loginbutton,response,usertype);
});

function loginloadingstate(element,response,usertype){
    element.innerHTML = '<strong>Logging in...</strong>';
    element.disabled = true;
    // simulating a response 
    const fakeResponse = {
        success: true,
        message: "Login successful",
        userType: usertype
    };
    if (fakeResponse.success) {
        response.innerText = fakeResponse.message;
        response.style.color = "green";
    } else {
        response.innerText = fakeResponse.message;
        response.style.color = "red";
    }
    element.innerText = 'Login';
    element.disabled = false;
}