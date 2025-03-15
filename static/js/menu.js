// Filter and category settings
let filterType = 'all'; // Default filter
let currentCategory = 'all'; // Default category
let lastAddedItem = null; // Last added item tracking

// Function to update menu items based on filter and category
function updateMenuDisplay() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        const itemType = item.getAttribute('data-type');
        
        // First filter by category
        let showByCategory = (currentCategory === 'all') || 
                            (currentCategory === itemType) || 
                            (currentCategory === 'regular' && itemType === 'customizable');
        
        // Then filter by type if visible by category
        let showByType = (filterType === 'all') || (filterType === itemType);
        
        if (showByCategory && showByType) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
    
    // Update category title
    const categoryTitles = {
        'all': 'Todos los Productos',
        'regular': 'Nuestras Gorditas',
        'extra': 'Extras',
        'bebidas': 'Bebidas',
        'postres': 'Postres',
        'complementos': 'Complementos'
    };
    
    document.getElementById('current-category-title').textContent = categoryTitles[currentCategory] || 'Todos los Productos';
}

// Function to populate extras modal
function populateExtrasModal() {
    const extrasList = document.getElementById('extras-list');
    // Clear the current list
    extrasList.innerHTML = '';
    
    // Find all menu items with type 'extra'
    const extras = document.querySelectorAll('.menu-item[data-type="extra"]');
    
    if (extras.length === 0) {
        extrasList.innerHTML = '<p class="col-span-2 text-center text-gray-500 py-4">No hay extras disponibles.</p>';
        return;
    }
    
    extras.forEach(extra => {
        const id = extra.getAttribute('data-id');
        const name = extra.querySelector('h3').textContent;
        const description = extra.querySelector('p').textContent;
        const price = extra.querySelector('.text-pily-orange').textContent;
        
        const extraItem = document.createElement('div');
        extraItem.className = 'bg-white rounded-lg shadow-md p-4 flex flex-col h-full';
        extraItem.innerHTML = `
            <div class="flex-1">
                <h4 class="font-bold text-pily-dark">${name}</h4>
                <p class="text-sm text-gray-600 mb-2">${description}</p>
                <div class="font-medium text-pily-orange">${price}</div>
            </div>
            <div class="flex justify-end mt-2">
                <button class="add-extra-btn bg-pily-orange text-white px-3 py-1 rounded-full text-sm" data-id="${id}">
                    Añadir
                </button>
            </div>
        `;
        extrasList.appendChild(extraItem);
        
        // Add click event for the add button
        extraItem.querySelector('.add-extra-btn').addEventListener('click', function() {
            const itemId = this.getAttribute('data-id');
            const menuItem = document.querySelector(`.menu-item[data-id="${itemId}"]`);
            const itemName = menuItem.querySelector('h3').textContent;
            const itemPrice = parseFloat(menuItem.querySelector('.text-pily-orange').textContent.replace('$', ''));
            
            // Find the current plate
            const plateIndex = cart.plates.findIndex(p => p.plateId === cart.currentPlateId);
            if (plateIndex === -1) {
                // If plate doesn't exist, create it
                cart.plates.push({
                    plateId: cart.currentPlateId,
                    items: {}
                });
            }
            
            // Get the current plate
            const currentPlate = cart.plates.find(p => p.plateId === cart.currentPlateId);
            
            // Add or increment the item in the current plate
            if (!currentPlate.items[itemId]) {
                currentPlate.items[itemId] = { name: itemName, price: itemPrice, quantity: 0 };
            }
            
            currentPlate.items[itemId].quantity++;
            
            // Show a success message
            const addBtn = this;
            addBtn.textContent = '¡Añadido!';
            addBtn.classList.remove('bg-pily-orange');
            addBtn.classList.add('bg-green-500');
            
            setTimeout(() => {
                addBtn.textContent = 'Añadir';
                addBtn.classList.remove('bg-green-500');
                addBtn.classList.add('bg-pily-orange');
            }, 1000);
            
            updateCart();
        });
    });
}

// Set up increase-quantity button functionality
document.querySelectorAll(".increase-qty").forEach(button => {
    // Remove the existing event listener first if possible
    const oldClickHandler = button._clickHandler;
    if (oldClickHandler) {
        button.removeEventListener("click", oldClickHandler);
    }
    
    // Add the new event handler
    const newClickHandler = () => {
        let itemId = button.getAttribute("data-id");
        let menuItem = button.closest(".menu-item");
        let itemName = menuItem.querySelector("h3").textContent;
        let itemPrice = parseFloat(menuItem.querySelector(".text-pily-orange").textContent.replace("$", ""));
        
        // Track this as the last added item
        lastAddedItem = {
            id: itemId,
            name: itemName,
            isGordita: itemName.toLowerCase().includes('gordita') || 
                      (currentCategory === 'regular' && !menuItem.getAttribute('data-type').includes('extra'))
        };
        
        // Find the current plate
        const plateIndex = cart.plates.findIndex(p => p.plateId === cart.currentPlateId);
        if (plateIndex === -1) {
            // If plate doesn't exist, create it
            cart.plates.push({
                plateId: cart.currentPlateId,
                items: {}
            });
        }
        
        // Get the current plate
        const currentPlate = cart.plates.find(p => p.plateId === cart.currentPlateId);
        
        // Add item to the current plate
        if (!currentPlate.items[itemId]) {
            currentPlate.items[itemId] = { name: itemName, price: itemPrice, quantity: 0 };
        }
        
        currentPlate.items[itemId].quantity++;
        const quantityElement = document.getElementById(`qty-${itemId}`);
        quantityElement.textContent = currentPlate.items[itemId].quantity;
        
        updateCart();
    };
    
    // Store the handler so we can remove it later if needed
    button._clickHandler = newClickHandler;
    
    button.addEventListener("click", newClickHandler);
});

// Set up decrease-quantity button functionality
document.querySelectorAll(".decrease-qty").forEach(button => {
    // Remove the existing event listener first if possible
    const oldClickHandler = button._clickHandler;
    if (oldClickHandler) {
        button.removeEventListener("click", oldClickHandler);
    }
    
    // Add the new event handler
    const newClickHandler = () => {
        let itemId = button.getAttribute("data-id");
        let quantityElement = document.getElementById(`qty-${itemId}`);
        
        // Find the current plate
        const plateIndex = cart.plates.findIndex(p => p.plateId === cart.currentPlateId);
        if (plateIndex !== -1) {
            const currentPlate = cart.plates[plateIndex];
            
            if (currentPlate.items[itemId] && currentPlate.items[itemId].quantity > 0) {
                currentPlate.items[itemId].quantity--;
                
                if (currentPlate.items[itemId].quantity === 0) {
                    delete currentPlate.items[itemId];
                    
                    // Check if item exists in any other plate
                    let itemInOtherPlates = false;
                    cart.plates.forEach(plate => {
                        if (plate.plateId !== cart.currentPlateId && plate.items[itemId]) {
                            itemInOtherPlates = true;
                        }
                    });
                    
                    if (!itemInOtherPlates) {
                        document.querySelector(`.menu-item[data-id="${itemId}"]`).classList.remove("selected");
                        document.getElementById(`badge-${itemId}`).classList.add("hidden");
                    }
                }
            }
        }
        
        // Update the quantity display
        // We need to sum across all plates
        let totalQuantity = 0;
        cart.plates.forEach(plate => {
            if (plate.items[itemId]) {
                totalQuantity += plate.items[itemId].quantity;
            }
        });
        
        quantityElement.textContent = totalQuantity;
        updateCart();
    };
    
    // Store the handler so we can remove it later if needed
    button._clickHandler = newClickHandler;
    
    button.addEventListener("click", newClickHandler);
});

// Function to suggest extras after a gordita is added
function suggestExtrasAfterGorditaAdded() {
    if (lastAddedItem && lastAddedItem.isGordita) {
        // Reset the tracking to prevent showing this again for the same item
        const itemName = lastAddedItem.name;
        lastAddedItem = null;
        
        // Show the extras modal
        setTimeout(() => {
            // Use the existing extrasModal functionality
            populateExtrasModal();
            
            // Customize the modal for this specific gordita
            const modalTitle = document.querySelector('#extras-modal .gradient-header h2');
            if (modalTitle) {
                modalTitle.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                    </svg>
                    ¿Deseas añadir extras a tu ${itemName}?
                `;
            }
            
            // Change the description text
            const modalDesc = document.querySelector('#extras-modal .p-6 > p');
            if (modalDesc) {
                modalDesc.textContent = `Complementa tu ${itemName} con estos deliciosos extras:`;
            }
            
            // Show the modal
            document.getElementById('extras-modal').classList.remove('hidden');
        }, 300); // Small delay for better UX
    }
}

// Initialize the menu when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    updateMenuDisplay();
});