
        // Open cart modal
        document.getElementById('view-cart-btn').addEventListener('click', function() {
            document.getElementById('cart-modal').classList.remove('hidden');
        });
        
        // Mobile cart button
        document.getElementById('mobile-cart-btn').addEventListener('click', function() {
            document.getElementById('cart-modal').classList.remove('hidden');
        });
        
        // Close cart modal
        document.getElementById('close-cart').addEventListener('click', function() {
            document.getElementById('cart-modal').classList.add('hidden');
        });
        
        // Continue shopping button
        document.getElementById('continue-shopping').addEventListener('click', function() {
            document.getElementById('cart-modal').classList.add('hidden');
        });
        
        // Add click handlers for sidebar category buttons
        document.querySelectorAll('.sidebar-category').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Update active state
                document.querySelectorAll('.sidebar-category').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
                
                // Set current category
                currentCategory = this.getAttribute('data-category');
                
                // Update menu display
                updateMenuDisplay();
            });
        });
        // Add click handlers for filter buttons
        document.querySelectorAll('.filter-btn').forEach(button => {
            button.addEventListener('click', function() {
                // Update active state
                document.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
                
                // Set filter type
                filterType = this.getAttribute('data-filter');
                
                // Update menu display
                updateMenuDisplay();
            });
        });
        
        // Click handler for customize buttons
        document.querySelectorAll('.customize-btn').forEach(button => {
            button.addEventListener('click', function() {
                const itemId = this.getAttribute('data-id');
                openItemModal(itemId);
            });
        });
