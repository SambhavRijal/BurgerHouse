window.onscroll = function() {scrollFunction()};
        function scrollFunction() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                document.getElementById("navbar").style.background = "#EEEEEC";
            } 
            else {
                document.getElementById("navbar").style.background = "none";
            }
        }
console.log("JS Testing correct");