let quantity_number = document.querySelector("#quantity_number");
let plus = document.querySelector(".plus");
let minus = document.querySelector(".minus");
let hldr = 1;

plus.addEventListener("click", ()=>{
    hldr++
    quantity_number.innerText = hldr;
});

minus.addEventListener("click", ()=>{
    hldr--;
    if( hldr <= 1){
        hldr = 1;
    }
    quantity_number.innerText = hldr;
});