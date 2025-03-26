// Cart data structure
let cart = {
    plates: [
        {
            plateId: 1,
            items: {}  // This will hold the items for plate 1
        }
    ],
    currentPlateId: 1  // Track which plate we're currently adding to
};

// Function to update the cart display
function updateCart() {
    let cartList = document.getElementById("cart-items");
    let emptyCartMessage = document.getElementById("empty-cart-message");
    cartList.innerHTML = "";
    
    let subtotal = 0;
    let totalItems = 0;
    let hasItems = false;
    
    // Check if we have any items across all plates
    cart.plates.forEach(plate => {
        if (Object.keys(plate.items).length > 0) {
            hasItems = true;
        }
    });
    
    emptyCartMessage.style.display = hasItems ? "none" : "block";
    
    // For each plate in the cart
    cart.plates.forEach(plate => {
        // Create a plate header if the plate has items
        if (Object.keys(plate.items).length > 0) {
            let plateHeader = document.createElement("li");
            plateHeader.className = "bg-gray-100 p-2 rounded-md mb-2";
            plateHeader.innerHTML = `
                <div class="flex justify-between items-center">
                    <div class="font-bold text-pily-dark">Platillo ${plate.plateId}</div>
                    <div>
                        <button class="edit-plate text-blue-500 hover:text-blue-700 mr-2" data-plate-id="${plate.plateId}">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                        </button>
                        <button class="remove-plate text-red-500 hover:text-red-700" data-plate-id="${plate.plateId}">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                            </svg>
                        </button>
                    </div>
                </div>
            `;
            cartList.appendChild(plateHeader);
            
            // Add event listener for edit plate button
            plateHeader.querySelector(".edit-plate").addEventListener("click", function() {
                const plateId = parseInt(this.getAttribute("data-plate-id"));
                cart.currentPlateId = plateId;
                // Update active plate indicator
                updateActivePlateIndicator();
                document.getElementById("cart-modal").classList.add("hidden");
            });
            
            // Add event listener for remove plate button
            plateHeader.querySelector(".remove-plate").addEventListener("click", function() {
                const plateId = parseInt(this.getAttribute("data-plate-id"));
                removePlate(plateId);
            });
        }
        
        // Now list all items in this plate
        Object.keys(plate.items).forEach(itemId => {
            let item = plate.items[itemId];
            let itemTotal = item.price * item.quantity;
            subtotal += itemTotal;
            totalItems += item.quantity;
            
            let li = document.createElement("li");
            li.className = "flex justify-between items-start border-b border-gray-200 pb-3 cart-item-animation ml-4"; // Added margin-left
            
            // Generate modification text if any
            let modificationsHtml = '';
            if (item.modifications && item.modifications.length > 0) {
                modificationsHtml = '<div class="text-xs text-gray-400 mt-1">';
                item.modifications.forEach(mod => {
                    let modText = '';
                    switch(mod.type) {
                        case 'add':
                            modText = `+ ${mod.name}`;
                            break;
                        case 'remove':
                            modText = `- ${mod.name}`;
                            break;
                        case 'substitute':
                            modText = `${mod.name}`;
                            break;
                    }
                    modificationsHtml += `<div>${modText}</div>`;
                });
                modificationsHtml += '</div>';
            }
            
            // Add special instructions if any
            let instructionsHtml = '';
            if (item.special_instructions) {
                instructionsHtml = `<div class="text-xs italic text-gray-500 mt-1">"${item.special_instructions}"</div>`;
            }
            
            li.innerHTML = `
                <div class="flex-1">
                    <div class="font-medium">${item.name}</div>
                    <div class="text-sm text-gray-500">$${item.price.toFixed(2)} × ${item.quantity}</div>
                    ${modificationsHtml}
                    ${instructionsHtml}
                </div>
                <div class="font-medium text-pily-dark">$${itemTotal.toFixed(2)}</div>
                <button class="remove-item ml-2 text-red-500 hover:text-red-700" data-plate-id="${plate.plateId}" data-id="${itemId}">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                </button>
            `;
            cartList.appendChild(li);
            
            // Add click event for remove button
            li.querySelector(".remove-item").addEventListener("click", function() {
                let itemId = this.getAttribute("data-id");
                let plateId = parseInt(this.getAttribute("data-plate-id"));
                
                // Find the plate and remove the item
                const plateIndex = cart.plates.findIndex(p => p.plateId === plateId);
                if (plateIndex !== -1) {
                    delete cart.plates[plateIndex].items[itemId];
                    document.getElementById(`qty-${itemId}`).textContent = "0";
                    document.getElementById(`badge-${itemId}`).classList.add("hidden");
                    document.querySelector(`.menu-item[data-id="${itemId}"]`).classList.remove("selected");
                    updateCart();
                }
            });
        });
    });
    
    // Calculate tax and total
    let tax = subtotal * 0.16; // 16% tax
    let total = subtotal + tax;
    
    // Update the display
    document.getElementById("subtotal").textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById("tax").textContent = `$${tax.toFixed(2)}`;
    document.getElementById("total-cost").textContent = `$${total.toFixed(2)}`;
    
    // Enable/disable checkout button
    document.getElementById("submit-cart").disabled = !hasItems;
    
    // Update quantity badges for all items across all plates
    // This part is tricky since we need to consolidate quantities across plates
    let combinedQuantities = {};
    
    cart.plates.forEach(plate => {
        Object.keys(plate.items).forEach(itemId => {
            if (!combinedQuantities[itemId]) {
                combinedQuantities[itemId] = 0;
            }
            combinedQuantities[itemId] += plate.items[itemId].quantity;
        });
    });
    
    // Now update the badges
    Object.keys(combinedQuantities).forEach(itemId => {
        let badge = document.getElementById(`badge-${itemId}`);
        badge.textContent = combinedQuantities[itemId];
        badge.classList.remove("hidden");
        document.querySelector(`.menu-item[data-id="${itemId}"]`).classList.add("selected");
    });
    
    // Update cart counter
    const cartCounter = document.getElementById("cart-counter");
    const mobileCartCounter = document.getElementById("mobile-cart-counter");
    
    if (totalItems > 0) {
        cartCounter.textContent = totalItems;
        cartCounter.classList.remove("hidden");
        mobileCartCounter.textContent = totalItems;
        mobileCartCounter.classList.remove("hidden");
    } else {
        cartCounter.classList.add("hidden");
        mobileCartCounter.classList.add("hidden");
    }
    
    // Update add new plate button visibility
    const addNewPlateBtn = document.getElementById("add-new-plate");
    if (addNewPlateBtn) {
        // Only show if at least one plate has items
        addNewPlateBtn.style.display = hasItems ? "block" : "none";
    }
    
    // Call extras suggestion if implemented
    if (typeof suggestExtrasAfterGorditaAdded === "function") {
        suggestExtrasAfterGorditaAdded();
    }
}

// Function to add a new plate to the order
function addNewPlate() {
    const newPlateId = cart.plates.length > 0 ? 
        Math.max(...cart.plates.map(plate => plate.plateId)) + 1 : 1;
        
    cart.plates.push({
        plateId: newPlateId,
        items: {}
    });
    
    // Set as current active plate
    cart.currentPlateId = newPlateId;
    
    // Update UI
    updateCart();
    updateActivePlateIndicator();
    
    // Close the cart modal
    document.getElementById("cart-modal").classList.add("hidden");
}

// Function to remove a plate
function removePlate(plateId) {
    // Find and remove the plate
    const plateIndex = cart.plates.findIndex(plate => plate.plateId === plateId);
    
    if (plateIndex !== -1) {
        // Reset any UI elements for items in this plate
        const plate = cart.plates[plateIndex];
        Object.keys(plate.items).forEach(itemId => {
            // This part is tricky - only reset UI if this item isn't in any other plate
            let itemInOtherPlates = false;
            cart.plates.forEach((p, idx) => {
                if (idx !== plateIndex && p.items[itemId]) {
                    itemInOtherPlates = true;
                }
            });
            
            if (!itemInOtherPlates) {
                document.getElementById(`qty-${itemId}`).textContent = "0";
                document.getElementById(`badge-${itemId}`).classList.add("hidden");
                document.querySelector(`.menu-item[data-id="${itemId}"]`).classList.remove("selected");
            }
        });
        
        // Remove the plate from the array
        cart.plates.splice(plateIndex, 1);
        
        // If no plates left, add a new empty one
        if (cart.plates.length === 0) {
            cart.plates.push({
                plateId: 1,
                items: {}
            });
            cart.currentPlateId = 1;
        } else {
            // Set current plate to the first one
            cart.currentPlateId = cart.plates[0].plateId;
        }
        
        updateCart();
        updateActivePlateIndicator();
    }
}

// Function to update the active plate indicator in the UI
function updateActivePlateIndicator() {
    const plateIndicator = document.getElementById("current-plate-indicator");
    if (plateIndicator) {
        plateIndicator.textContent = `Platillo ${cart.currentPlateId}`;
    }
}

// Submit the cart function
document.getElementById("submit-cart").addEventListener("click", () => {
    if (cart.plates.length === 0 || !cart.plates.some(plate => Object.keys(plate.items).length > 0)) {
        alert("No hay productos en tu orden!");
        return;
    }
    
    let tableNumber = document.getElementById("table-number").value;
    
    // Transform cart plates to array of order items
    const orderItems = [];
    
    cart.plates.forEach(plate => {
        if (Object.keys(plate.items).length === 0) return;
        
        const plateItems = Object.keys(plate.items).map(id => {
            const item = plate.items[id];
            return {
                menu_item_id: parseInt(id),
                quantity: item.quantity,
                modifications: item.modifications || [],
                special_instructions: item.special_instructions || "",
                plate_id: plate.plateId
            };
        });
        
        orderItems.push(...plateItems);
    });
    
    fetch("/api/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            table_number: tableNumber,
            branch_id: "1", // Default branch ID
            items: orderItems
        })
    })
    .then(response => response.json())
    .then(data => {
        // Hide cart modal
        document.getElementById("cart-modal").classList.add("hidden");
        
        // Show success modal
        document.getElementById("modal-order-number").textContent = `Orden #${data.order_id}`;
        document.getElementById("success-modal").classList.remove("hidden");
        
        // Reset cart
        cart = {
            plates: [
                {
                    plateId: 1,
                    items: {}
                }
            ],
            currentPlateId: 1
        };
        
        document.querySelectorAll(".item-qty").forEach(span => span.textContent = "0");
        document.querySelectorAll(".quantity-badge").forEach(badge => badge.classList.add("hidden"));
        document.querySelectorAll(".menu-item").forEach(item => item.classList.remove("selected"));
        updateCart();
        updateActivePlateIndicator();
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Hubo un error al procesar tu orden. Por favor intenta de nuevo.");
    });
});

// Add new plate button event listener
document.getElementById("add-new-plate").addEventListener("click", function() {
    addNewPlate();
});

// Store the original updateCart function reference for potential overrides
const originalUpdateCart = updateCart;

// Initialize cart display
document.addEventListener('DOMContentLoaded', function() {
    updateCart();
    updateActivePlateIndicator();
});