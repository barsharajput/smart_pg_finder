let index = 0;

function slide(){

let images = document.querySelectorAll(".slider img")

images.forEach(img => img.style.display="none")

index++

if(index > images.length){index = 1}

images[index-1].style.display="block"

setTimeout(slide,3000)

}

slide()