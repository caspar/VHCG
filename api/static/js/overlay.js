var overlay = document.getElementById('overlay');
		var overlayContent = document.getElementById('overlay-content');

		// Get the close button and add a click event listener to hide the overlay
		var overlayClose = document.getElementById('overlay-close');
		overlayClose.addEventListener('click', function() {
			overlay.style.display = 'none';
		});

        //close overlay when click outside of it:
        window.addEventListener('click', function(event) {
            if (event.target == overlay) {
                overlay.style.display = 'none';
            }
        });


		// Get all bed elements and add a click event listener to show the overlay with the bed info
		var beds = document.querySelectorAll('.bed');
		for (var i = 0; i < beds.length; i++) {
			beds[i].addEventListener('click', function() {
				// Get the bed ID and owners
				var bedId = this.id;
				var owner = this.dataset.owner;

				// Set the overlay content
				document.getElementById('bed-id').textContent = bedId.substring(1); //substring(1) to remove the 'b' from the id
				document.getElementById('bed-owners').textContent = 'Owners: ' + owner;

                // Show the overlay
                overlay.style.display = 'flex';

                // Prevent the default click event
                return false;
                
            });
        }