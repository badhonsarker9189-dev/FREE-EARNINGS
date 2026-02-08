let balance = 0;

function completeTask() {
  balance += 10;
  document.getElementById("balance").innerText = "৳" + balance.toFixed(2);
}

function withdraw() {
  let amount = document.getElementById("amount").value;
  let method = document.getElementById("method").value;
  let account = document.getElementById("account").value;

  if(amount && method && account){
    alert(`✅ Withdraw request submitted\nAmount: ${amount}\nMethod: ${method}\nAccount: ${account}`);
    document.getElementById("amount").value = "";
    document.getElementById("method").value = "";
    document.getElementById("account").value = "";
  } else {
    alert("❌ Fill all fields!");
  }
}
