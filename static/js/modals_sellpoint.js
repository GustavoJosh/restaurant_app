// DOM elements for the modals - with safety checks
let extrasModal, closeExtrasBtn, closeExtrasContinueBtn, extrasList;

// Modal setup function - called on DOMContentLoaded to ensure elements exist
function setupModals() {
    // Get the extras modal elements
    extrasModal = document.getElementById('extras-modal');
    closeExtrasBtn = document.getElementById('close-extras');
    closeExtrasContinueBtn = document.getElementById('close-extras-continue');
    extrasList = document.getElementById('extras-list');
    
    // Close item modification modal
    const closeModalBtn = document.getElementById('close-modal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            const itemModificationModal = document.getElementById('item-modification-modal');
            if (itemModificationModal) {
                itemModificationModal.classList.add('hidden');
            }
        });
    }
    
    // Close extras modal
    if (closeExtrasBtn) {
        closeExtrasBtn.addEventListener('click', () => {
            if (extrasModal) {
                extrasModal.classList.add('hidden');
            }
        });
    }
    
    if (closeExtrasContinueBtn) {
        closeExtrasContinueBtn.addEventListener('click', () => {
            if (extrasModal) {
                extrasModal.classList.add('hidden');
            }
        });
    }
    
    // Close success modal
    const closeSuccessBtn = document.getElementById("close-success");
    if (closeSuccessBtn) {
        closeSuccessBtn.addEventListener("click", () => {
            const successModal = document.getElementById("success-modal");
            if (successModal) {
                successModal.classList.add("hidden");
            }
        });
    }
    
    // Set up quantity handlers in the modification modal
    const itemQuantityInput = document.getElementById('item-quantity');
    if (itemQuantityInput) {
        itemQuantityInput.addEventListener('change', updateModalPrice);
        
        const increaseQuantityBtn = document.getElementById('increase-quantity');
        if (increaseQuantityBtn) {
            increaseQuantityBtn.addEventListener('click', function() {
                if (parseInt(itemQuantityInput.value) < 99) {
                    itemQuantityInput.value = parseInt(itemQuantityInput.value) + 1;
                    updateModalPrice();
                }
            });
        }
        
        const decreaseQuantityBtn = document.getElementById('decrease-quantity');
        if (decreaseQuantityBtn) {
            decreaseQuantityBtn.addEventListener('click', function() {
                if (parseInt(itemQuantityInput.value) > 1) {
                    itemQuantityInput.value = parseInt(itemQuantityInput.value) - 1;
                    updateModalPrice();
                }
            });
        }
    }
    
    // Set up add-to-order button
    const addToOrderBtn = document.getElementById('add-to-order');
    if (addToOrderBtn) {
        addToOrderBtn.addEventListener('click', addItemFromModalToOrder);
    }
}

// Function to open the item modification modal
function openItemModal(itemId) {
    const modalElement = document.getElementById('item-modification-modal');
    if (!modalElement) return;
    
    // Find the menu item
    const menuItem = document.querySelector(`.menu-item[data-id="${itemId}"]`);
    if (!menuItem) return;
    
    const itemName = menuItem.querySelector('h3').textContent;
    const itemPrice = parseFloat(menuItem.querySelector('.text-pily-orange').textContent.replace('$', ''));
    
    // Update modal with item info
    const modalItemName = document.getElementById('modal-item-name');
    const modalItemId = document.getElementById('modal-item-id');
    const modalItemPrice = document.getElementById('modal-item-price');
    const totalPriceElement = document.getElementById('total-price');
    const specialInstructions = document.getElementById('special-instructions');
    const itemQuantity = document.getElementById('item-quantity');
    
    if (modalItemName) modalItemName.textContent = itemName;
    if (modalItemId) modalItemId.value = itemId;
    if (modalItemPrice) modalItemPrice.value = itemPrice;
    if (totalPriceElement) totalPriceElement.textContent = itemPrice.toFixed(2);
    
    // Reset special instructions field
    if (specialInstructions) specialInstructions.value = '';
    
    // Reset quantity to 1
    if (itemQuantity) itemQuantity.value = '1';
    
    // Show the modal
    modalElement.classList.remove('hidden');
}

// Function to update the price in the modal based on quantity
function updateModalPrice() {
    const basePrice = parseFloat(document.getElementById('modal-item-price').value || 0);
    const quantity = parseInt(document.getElementById('item-quantity').value || 1);
    const totalPrice = basePrice * quantity;
    
    const totalPriceElement = document.getElementById('total-price');
    if (totalPriceElement) {
        totalPriceElement.textContent = totalPrice.toFixed(2);
    }
}

// Function to add item from modal to cart
function addItemFromModalToOrder() {
    const itemId = document.getElementById('modal-item-id').value;
    const itemName = document.getElementById('modal-item-name').textContent;
    const itemPrice = parseFloat(document.getElementById('modal-item-price').value);
    const quantity = parseInt(document.getElementById('item-quantity').value);
    const specialInstructions = document.getElementById('special-instructions').value;
    
    // Check if this is a gordita for extras suggestion (if lastAddedItem exists in the scope)
    if (typeof lastAddedItem !== 'undefined' && itemName.toLowerCase().includes('gordita')) {
        lastAddedItem = {
            name: itemName,
            isGordita: true
        };
    }
    
    // Make sure cart exists
    if (typeof cart === 'undefined') {
        console.error('Cart is not defined. Make sure cart.js is loaded first.');
        return;
    }
    
    // Collect modifications
    const modifications = [];
    
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
    
    // Add the item to the current plate
    currentPlate.items[itemId] = {
        name: itemName,
        price: itemPrice,
        quantity: quantity,
        modifications: modifications,
        special_instructions: specialInstructions
    };
    
    // Update quantity display if it exists
    const quantityElement = document.getElementById(`qty-${itemId}`);
    if (quantityElement) {
        // We need to sum across all plates
        let totalQuantity = 0;
        cart.plates.forEach(plate => {
            if (plate.items[itemId]) {
                totalQuantity += plate.items[itemId].quantity;
            }
        });
        
        quantityElement.textContent = totalQuantity;
    }
    
    // Close the modal
    const modalElement = document.getElementById('item-modification-modal');
    if (modalElement) {
        modalElement.classList.add('hidden');
    }
    
    // Update the cart if function exists
    if (typeof updateCart === 'function') {
        updateCart();
    } else {
        console.error('updateCart function is not defined. Make sure cart.js is loaded first.');
    }
}

// Initialize modals when DOM is loaded
document.addEventListener('DOMContentLoaded', setupModals);