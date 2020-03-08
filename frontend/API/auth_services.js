function do_login(type) {
  let username = "";
  let password = "";
  let errorDiv = "";
  let error_style = "";
  if (type === "form") {
    username = document.getElementById("login_username").value;
    password = document.getElementById("login_password").value;
    errorDiv = "error";
  } else {
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    errorDiv = "error1";
  }
  if (username != "" && password != "") {
    $.get(
      `http://localhost:5001/login?username=${username}&password=${password}`,
      function(data) {
        let res = JSON.parse(data);

        if (res.status === "error") {
          document.getElementById(errorDiv).style.display = "block";
          document.getElementById(errorDiv).innerHTML = res.message;
          document.getElementById(errorDiv).style.color = "red";
        } else {
          document.getElementById(errorDiv).style.display = "block";
          document.getElementById(errorDiv).innerHTML = "Login succesful";
          document.getElementById(errorDiv).style.color = "green";
          //We can also store the token for future use
          localStorage.setItem("token", res.message);
        }
      }
    );
  } else {
    document.getElementById(errorDiv).style.display = "block";
    document.getElementById(errorDiv).innerHTML =
      "Username and password are required!";
    document.getElementById(errorDiv).style.color = "red";
  }
}

function do_registration() {
  let username = document.getElementById("rUsername").value;
  let password = document.getElementById("rPassword").value;
  let errorDiv = "rError";
  if (username != "" && password != "") {
    $.get(
      `http://localhost:5001/registration?username=${username}&password=${password}&email=&address=&contactNo=0`,
      function(data) {
        let res = JSON.parse(data);

        if (res.status === "error") {
          document.getElementById(errorDiv).style.display = "block";
          document.getElementById(errorDiv).innerHTML = res.message;
          document.getElementById(errorDiv).style.color = "red";
        } else {
          document.getElementById(errorDiv).style.display = "block";
          document.getElementById(errorDiv).innerHTML = res.message;
          document.getElementById(errorDiv).style.color = "green";
          //We can also store the token for future use
          localStorage.setItem("token", res.message);
        }
      }
    );
  } else {
    document.getElementById(errorDiv).style.display = "block";
    document.getElementById(errorDiv).innerHTML =
      "Username and password are required!";
    document.getElementById(errorDiv).style.color = "red";
  }
}
