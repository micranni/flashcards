
function toggleClass(el, c_name){
    el.classList.toggle(`${c_name}`);
}

function add_class(el, c_name){
    el.classList.add(`${c_name}`);
}

function remove_class(el, c_name){
    el.classList.remove(`${c_name}`)
}

let vocab_card = document.querySelector('.vocab-card');
let def_card = document.querySelector('.definition-card');

vocab_card.addEventListener('click', (e)=>{
    add_class(e.currentTarget, 'hidden');
    remove_class(def_card, 'hidden');
})

def_card.addEventListener('click', (e)=>{
    add_class(e.currentTarget, 'hidden');
    remove_class(vocab_card, 'hidden');
})

let redefine_btn = document.getElementById('redefine-btn');
let redefine_pop = document.querySelector('.redefine-c');

redefine_btn.addEventListener('click', ()=>{
    console.log("clicked");
    toggleClass(redefine_pop, 'hidden');
})