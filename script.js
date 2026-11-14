(function () {
  'use strict';
  var menuToggle = document.getElementById('menu-toggle');
  var navigation = document.getElementById('primary-navigation');
  if (menuToggle && navigation) {
    menuToggle.addEventListener('click', function () {
      var isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
      menuToggle.setAttribute('aria-label', isOpen ? 'Open menu' : 'Close menu');
      navigation.classList.toggle('is-open', !isOpen);
    });
    navigation.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navigation.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.setAttribute('aria-label', 'Open menu');
      });
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
        navigation.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.setAttribute('aria-label', 'Open menu');
        menuToggle.focus();
      }
    });
  }

  var form = document.getElementById('planner-form');
  var result = document.getElementById('planner-result');
  var amount = document.getElementById('loan-amount');
  var amountError = document.getElementById('amount-error');
  var reset = document.getElementById('plan-again');
  var currency = new Intl.NumberFormat('en-ZA', { style: 'currency', currency: 'ZAR', maximumFractionDigits: 0 });
  if (form && result && amount && amountError) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var value = Number(amount.value);
      if (!amount.value || !Number.isFinite(value) || value < 1 || value > 999999) {
        amountError.textContent = 'Enter an amount between R1 and R999 999 to create your planning note.';
        amountError.hidden = false;
        amount.setAttribute('aria-invalid', 'true');
        amount.focus();
        return;
      }
      amountError.hidden = true;
      amount.removeAttribute('aria-invalid');
      var selected = form.querySelector('input[name="purpose"]:checked');
      var purpose = selected ? selected.value : 'a personal expense';
      document.getElementById('result-title').textContent = currency.format(value) + ' for ' + purpose.toLowerCase() + '.';
      document.getElementById('result-description').textContent = 'This is a personal planning summary, not an available loan amount, approval, cost estimate or offer. No information was saved or sent.';
      form.hidden = true;
      result.hidden = false;
      result.focus();
    });
    amount.addEventListener('input', function () {
      amountError.hidden = true;
      amount.removeAttribute('aria-invalid');
    });
    if (reset) reset.addEventListener('click', function () {
      result.hidden = true;
      form.hidden = false;
      form.reset();
      amount.focus();
    });
  }
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
