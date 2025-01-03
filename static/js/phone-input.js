document.addEventListener('DOMContentLoaded', function () {
    const phoneInput = document.getElementById('phoneInput');

    phoneInput.addEventListener('input', function () {
        // Якщо значення не починається з +380, виправляємо його
        if (!this.value.startsWith('+380')) {
            this.value = '+380';
        }

        // Видаляємо всі символи, окрім цифр
        this.value = this.value.replace(/[^+\d]/g, '');

        // Забезпечуємо коректний формат +380 і не більше 9 цифр після нього
        this.value = this.value.replace(/(\+380)(\d{0,9}).*/, '+380$2');
    });

    phoneInput.addEventListener('focus', function () {
        if (this.value === '') {
            this.value = '+380'; // Встановлюємо значення за замовчуванням
        }
        this.setSelectionRange(4, 4); // Переміщуємо курсор після +380
    });

    phoneInput.addEventListener('keydown', function (event) {
        const allowedKeys = ['Backspace', 'ArrowLeft', 'ArrowRight', 'Delete', 'Tab'];
        const isNumberKey = event.key >= '0' && event.key <= '9';
        const isControlKey = allowedKeys.includes(event.key);

        // Забороняємо введення, якщо кількість цифр досягла 9
        const currentValue = phoneInput.value.replace(/\+380/, '');
        if (currentValue.length >= 9 && isNumberKey) {
            event.preventDefault();
        }

        if (!isNumberKey && !isControlKey) {
            event.preventDefault();
        }
    });
});
