document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("zakatForm");
    const resultDisplay = document.getElementById("zakatResult");

    const totelGoatInput = document.getElementById("totelGoatInput");
    const totelCowInput = document.getElementById("totelCowInput");
    const totelCamelInput = document.getElementById("totelCamelInput");

    const totelGoat = document.getElementById("totelGoat");
    const totelCow = document.getElementById("totelCow");
    const totelCamel = document.getElementById("totelCamel");



    // Function to calculate Zakat
    function calculateZakat() {
        let goatZakat = 0;
        let cowZakat = "";
        let camelZakat = "";

        // Get the values from the input fields
        const inputs = form.querySelectorAll("input[type='number']");

        inputs.forEach(input => {
            const value = parseFloat(input.value) || 0;

            switch (input.className) {
                case 'goat':
                    if (value >= 40 && value < 120) {
                        goatZakat = '1 goat or sheep ';
                    } else if (value >= 120 && value < 200) {
                        goatZakat = '2 goat or sheep';
                    } else if (value >= 200) {
                        goatZakat = Math.floor(value / 100);
                    }
                    break;

                case 'cow':
                    if (value > 30 && value <= 40) {
                        cowZakat = '1 one year old calf';
                    } else if (value > 40 && value <= 60) {
                        cowZakat = '1 two year old calf';
                    } else if (value > 60 && value <= 70) {
                        cowZakat = '2 one year old calves';
                    } else if (value > 70 && value <= 80) {
                        cowZakat = '2 one year old calves and 1 two-year-old calf';
                    } else if (value > 80) {
                        cowZakat = `${Math.floor(value / 20)} two-year-old calves`;
                    }
                    break;

                case 'camel':
                    if (value >= 5 && value < 25) {
                        camelZakat = `${Math.floor(value / 5)} goat(s) of one year or sheep of two years`;
                    } else if (value >= 25 && value < 75) {
                        const num = value - 25;
                        camelZakat = `1 and ${Math.floor(num / 10)} year-old female camels`;
                    }
                    else if (value > 75 && value <= 90) {
                        camelZakat = `2 two-year-old female camels`;
                    }
                    else if (value > 90 && value <= 120) {
                        camelZakat = `2 three-year-old female camels`;
                    }
                    else if (value > 120) {
                        value = Math.ceil(value / 10) * 10;

                        const cows = Math.floor(surplusCamels / 40); // 1 cow for every 40 surplus camels
                        const goats = Math.floor(surplusCamels / 50); // 1 goat for every 50 surplus camels

                        // if (value % 40 === 0 ) {
                        //     ` ${value / 40} year old femail camel `nmj,
                        // }
                        // else if(value % 50 === 0) {
                        //     ` ${value / 50} year old femail camel `
                        // }
                    }
                    break;

                default:
                    break;
            }
        });

        // Display the results in the respective elements
        totelCowInput.value = cowZakat;
        totelGoatInput.value = goatZakat;
        totelCamelInput.value = camelZakat;

        totelCow.textContent = cowZakat;
        totelGoat.textContent = goatZakat;
        totelCamel.textContent = camelZakat;
    }

    // Add an event listener to the form submission
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission
        calculateZakat(); // Call the Zakat calculation function
    });

    // Button controls
    let calculateBtn = document.getElementById('calculateZakat');
    let submitBtn = document.getElementById('submitZakat');
    let p1 = document.getElementById('p1') 
    let p2 = document.getElementById('p2') 
    let p3 = document.getElementById('p3') 

    calculateBtn.addEventListener('click', () => {
        submitBtn.style.display = 'block';
        p1.classList.remove('hide')
        p2.classList.remove('hide')
        p3.classList.remove('hide')
    });

    submitBtn.addEventListener('click', () => {
        calculateZakat();
    });
});

