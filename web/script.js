function loadTasks(){
 fetch("/admin/pending-tasks")
 .then(r=>r.json())
 .then(d=>{
  let h=""
  d.forEach(x=>{
    h+=`<p>${x[1]} | ${x[2]} | ৳${x[3]}
    <button onclick="approveTask(${x[0]})">Approve</button></p>`
  })
  document.getElementById("tasks").innerHTML=h
 })
}

function approveTask(id){
 fetch("/admin/approve-task/"+id)
 .then(()=>loadTasks())
}

function loadWithdraw(){
 fetch("/admin/pending-withdraw")
 .then(r=>r.json())
 .then(d=>{
  let h=""
  d.forEach(x=>{
    h+=`<p>${x[1]} | ৳${x[2]} | ${x[3]} | ${x[4]}
    <button onclick="approveWithdraw(${x[0]})">Pay</button></p>`
  })
  document.getElementById("withdraws").innerHTML=h
 })
}

function approveWithdraw(id){
 fetch("/admin/approve-withdraw/"+id)
 .then(()=>loadWithdraw())
}
