let goldNisab = 85
let silverNisab = 595


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("zakatForm");
    const zakatAmountDisplay = document.getElementById("zakatAmount");
    const zakatAmountDisplayInput = document.getElementById("zakatAmountInput");
    const zakatAssetDisplay = document.getElementById("totelAsset");
    const totelAssetInput = document.getElementById("totelAssetInput");

    // Zakat rate
    const zakatRate = 0.025;
    const zakatNIRate = 0.1;
    const zakatAIRate = 0.05;
    const zakatTMRate = 0.2;

    // Function to calculate Zakat
    function calculateZakat() {
        // Get the values from the input fields
        const inputs = form.querySelectorAll("input[type='number']");
        let asset = 0;
        let zakatAmount = 0;

        let goldGramPrice = 7000
        let silverGramPrice = 100
        

        inputs.forEach(input => {
            const value = parseFloat(input.value) || 0;
            // asset += value;
            
            
            switch (input.className) {
                case 'gold':
                    if (value >  85) {
                        rupa = value * goldGramPrice
                        asset += rupa;
                        zakatAmount += rupa * zakatRate;
                    }
                    break;

                case 'silver':
                    if (value >  595) {
                        rupa = value * silverGramPrice
                        asset += rupa;
                        zakatAmount += rupa * zakatRate;
                    }
                    break;

                case 'ni':
                    if (value > 672) {
                        asset += value;
                        zakatAmount += value * zakatNIRate;
                    }
                    break;

                case 'ai':
                    if (value > 2) {
                        asset += value;
                        zakatAmount += value * zakatAIRate;
                    }
                    break;

                case 'tm':
                    if (value > 0) {
                        asset += value;
                        zakatAmount += value * zakatTMRate;
                    }
                    break;
            
                default:
                    asset += value;
                    zakatAmount += value * zakatRate;
                    break;
            }
        });

        // Calculate Zakat
        // const zakatAmount = zakathAssets * zakatRate;

        // Display the result
        zakatAmountDisplay.textContent = zakatAmount.toFixed(2);
        zakatAssetDisplay.textContent = asset.toFixed(2);
        zakatAmountDisplayInput.value = zakatAmount.toFixed(2);
        totelAssetInput.value = asset.toFixed(2);
    }

    // Add an event listener to the form submission
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission
        calculateZakat(); // Call the Zakat calculation function
    });
});




let calculateBtn = document.getElementById('calculateZakat')
let submitBtn = document.getElementById('submitZakat')
let zakatForm = document.getElementById('zakatForm')


calculateBtn.addEventListener('click', () => {
    submitBtn.style.display = 'block'
})



submitBtn.addEventListener('click', () => {
    zakatForm.submit()
})












