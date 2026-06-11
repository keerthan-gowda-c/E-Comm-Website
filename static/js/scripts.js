const productSection = document.querySelector('#product-section');
const productDetailsPage = document.getElementById('product-detail-root');

// Safe dataset access
const addToCartURL =
    productSection?.dataset.addToCartUrl ||
    productDetailsPage?.dataset.addToCartUrl;

const csrf_token =
    productSection?.dataset.csrfToken ||
    productDetailsPage?.dataset.csrfToken;

// Safe target selection
const addCartTarget = productDetailsPage || productSection;

// Attach event only if element exists
if (addCartTarget) {
    addCartTarget.addEventListener('click', async function (event) {
        const btn = event.target;

        if (btn.classList.contains('add-to-cart')) {

            const productId = btn.dataset.productId;

            // Prevent double clicks
            btn.disabled = true;

            try {
                const response = await fetch(addToCartURL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrf_token
                    },
                    body: `product_id=${productId}`
                });

                if (!response.ok) {
                    throw new Error('Failed to add to cart');
                }

                const data = await response.json();

                // Show success toast
                showToast(data.message);

            } catch (error) {
                console.error(error);

                // Safe error toast
                showToast('Something went wrong!', 'danger');
            } finally {
                btn.disabled = false;
            }
        }
    });
} else {
    console.error('No valid add-to-cart container found!');
}


// Toast function 
function showToast(message, type = 'success') {
    const toastElement = document.querySelector('#cartToast');
    const toastBody = document.querySelector('#cartToastBody');

    if (!toastElement || !toastBody) {
        console.error('Toast elements not found!');
        return;
    }

    // Set message
    toastBody.textContent = message;

    // Update color
    toastElement.classList.remove('text-bg-success', 'text-bg-danger');
    toastElement.classList.add(`text-bg-${type}`);

    // Show toast
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
}


