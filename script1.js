let users=[];
document.getElementById("detailform").addEventListener("submit", function(event) {
      event.preventDefault();
      let latitude=document.getElementById("lat");
      let longitude=document.getElementById("long");
      let age=document.getElementById("age");
      let room=document.getElementById("room");
      let bedroom=document.getElementById("bedroom");
      let household=document.getElementById("household");
      let income=document.getElementById("income");
      let user={
        latitude:latitude,
        longitude:longitude,
        age:age,
        room:room,
        bedroom:bedroom,
        household:household,
        income:income
      }
      users.push(user);
      document.getElementById("output").textContent = JSON.stringify(users, null, 2);
      document.getElementById("loginForm").reset();

})
