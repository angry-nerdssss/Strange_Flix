window.addEventListener("scroll", function(event) { 
  
    var scroll_y = this.scrollY; 

    // console.log(scroll_y);
    
    if(scroll_y < 100){
        document.querySelector(".dark-bar").style.backgroundColor = "black";
    }else{
        document.querySelector(".dark-bar").style.backgroundColor = "rgba(0, 0, 0, 0.4)";
    }
}); 


