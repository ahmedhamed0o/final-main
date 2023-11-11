document.addEventListener("DOMContentLoaded", function() {
  // Get the element you want to show/hide
  var elementToToggler = document.getElementById("loader");
  var elementToToggle = document.getElementById("openloader");
  var navbar = document.getElementById("nav");
  // Use setTimeout to hide the element after a delay (e.g., 5 seconds)
    document.onreadystatechange = () => {
      if (document.readyState !== "complete") {
        elementToToggle.style.visibility = "hidden";
        elementToToggler.style.visibility = "visible";
        
      } else{
        elementToToggle.style.visibility = "visible";
        elementToToggler.style.display = "none";
        navbar.style.position = "sticky"
      }
    }
  



  const viewBtn = document.querySelector(".shareNews"),
    popup = document.querySelector(".popup"),
    close = popup.querySelector(".close"),
    field = popup.querySelector(".field"),
    input = field.querySelector("input"),
    copy = field.querySelector("button");
    // const scrollTop = indow.pageYOffset || document.documentElement.scrollTop;

    viewBtn.onclick = ()=>{ 
      
      popup.classList.toggle("show");
      // window.onscroll = function() {
      //   window.scrollTo(scrollTop);
      // };
    }
    close.onclick = ()=>{
      viewBtn.click();
    }

    copy.onclick = ()=>{
      input.select(); //select input value
      if(document.execCommand("copy")){ //if the selected text is copied
        field.classList.add("active");
        copy.innerText = "Copied";
        setTimeout(()=>{
          window.getSelection().removeAllRanges(); //remove selection from page
          field.classList.remove("active");
          copy.innerText = "Copy";
        }, 3000);
      }
    }
});

const image_input = document.getElementById('uploadlogo');
var uploaded_image = "";
image_input.addEventListener("change", function(){
  const reader = new FileReader();
  reader.addEventListener("load", function(){
    uploaded_image = reader.result;
    document.querySelector('#newavatar').style.backgroundImage = `url(${uploaded_image})`;
  })
  reader.readAsDataURL(this.files[0]);
})

