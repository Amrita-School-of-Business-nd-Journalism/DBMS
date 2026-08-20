const navCustomerName = document.getElementById("nav-customer-name");
const dashboardName = document.getElementById("dashboard-name");
const firstNameInput = document.getElementById("first-name");
const lastNameInput = document.getElementById("last-name");
const emailInput = document.getElementById("email");
const phoneInput = document.getElementById("phone");

document.getElementById("logout-btn").addEventListener("click", logout);

async function loadProfile(){
    try{
        const response = await fetch("/profile");
        const data = await response.json();

        if(!data.success){
            alert(data.message);
            window.location.href = "/";
            return;
        }
        const user = data.user
        navCustomerName.innerText = user.FIRST_NAME + " " + user.LAST_NAME;
        dashboardName.innerText = " " + user.FIRST_NAME;
        
        firstNameInput.value = user.FIRST_NAME;
        lastNameInput.value = user.LAST_NAME;
        emailInput.value = user.EMAIL;
        phoneInput.value = user.PHONE_NO;
    }
    catch(error){
        console.log(error);
        alert("Could not load Profile!!!")
    }
}
loadProfile();

const profileForm = document.getElementById("profile-form");
profileForm.addEventListener("submit",async (event)=>{
    event.preventDefault();
    const data = {
        first_name : firstNameInput.value,
        last_name : lastNameInput.value,
        phone_no : phoneInput.value
    }
    try {
        const response = await fetch("/profile",{
            method:"PUT",
            headers:{
                "Content-type":"application/json"
            },
            body:JSON.stringify(data)
        });

        const result = await response.json();

        if(result.success){
            alert(result.message);
            navCustomerName.innerText = data.first_name + " " +data.last_name;
            dashboardName.innerText = data.first_name;
        }
        else{
            alert(result.message);
        }
    }
    catch(error){
        console.error(error);
        alert("Could not update profile!");
    }
});

const deleteAccButton = document.getElementById("delete-account-btn");
deleteAccButton.addEventListener("click",async() => {
    const confirmed = confirm(
        "Are you sure to Delete this Account?\n\n"+
        "This Action cannot be Undone!"
    );
    if (!confirmed){
        return;
    }

    deleteAccButton.innerText = "Deleting";
    deleteAccButton.disabled = true;

    try {
        const response = await fetch("/profile",{
            method:"DELETE"
        });
        const data = await response.json();

        if(data.success){
            alert(data.message);
            window.location.href = "/";
        }
        else{
            alert(data.message);
            deleteAccButton.innerText = "Delete Account";
            deleteAccButton.disabled = false;
        }
    }
    catch(error){
        console.error(error);
        alert("Could not delete the Account");
        deleteAccButton.innerText = "Delete Account";
        deleteAccButton.disabled = false;
    }
})