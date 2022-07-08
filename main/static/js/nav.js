window.onscroll = function() {scrollFunction()};
        function scrollFunction() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                document.getElementById("navbar").style.background = "#1a1a1a";
                document.getElementById("url1").style.color = "white";
                document.getElementById("url2").style.color = "white";
                document.getElementById("url3").style.color = "white";
            } 
            else {
                document.getElementById("navbar").style.background = "none";
                document.getElementById("url1").style.color = "#1a1a1a";
                document.getElementById("url2").style.color = "#1a1a1a";
                document.getElementById("url3").style.color = "#1a1a1a";

            }
        }
console.log("JS Testing correct");