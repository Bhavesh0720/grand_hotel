        // Function to show the pop-up
        function showPopup(popupId) {
            var popup = document.getElementById(popupId);
            popup.style.display = 'block';
        }

        // Function to close the pop-up
        function closePopup(popupId) {
            var popup = document.getElementById(popupId);
            popup.style.display = 'none';
        }

        // Event listener to close the pop-up when clicking outside the pop-up
        window.onclick = function(event) {
            var overlays = document.getElementsByClassName('overlay');
            for (var i = 0; i < overlays.length; i++) {
                if (event.target == overlays[i]) {
                    overlays[i].style.display = 'none';
                }
            }
        };
