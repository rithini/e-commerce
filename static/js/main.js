// Simple E-commerce Store - Interactive Client-Side Logic

document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  // 1. Auto-dismiss Bootstrap alert toasts after 4 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      } catch (e) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 400);
      }
    }, 4500);
  });

  // 2. Quantity Picker Helper (for Product Details & Cart)
  document.querySelectorAll('.btn-qty-minus').forEach(function (button) {
    button.addEventListener('click', function () {
      const input = this.closest('.qty-controller').querySelector('input');
      let val = parseInt(input.value) || 1;
      if (val > 1) {
        input.value = val - 1;
        // If within a form that submits on change
        if (this.dataset.autoSubmit === 'true') {
          this.closest('form').submit();
        }
      }
    });
  });

  document.querySelectorAll('.btn-qty-plus').forEach(function (button) {
    button.addEventListener('click', function () {
      const input = this.closest('.qty-controller').querySelector('input');
      const maxStock = parseInt(input.getAttribute('max')) || 999;
      let val = parseInt(input.value) || 1;
      if (val < maxStock) {
        input.value = val + 1;
        if (this.dataset.autoSubmit === 'true') {
          this.closest('form').submit();
        }
      } else {
        showToast('Maximum available stock reached (' + maxStock + ')');
      }
    });
  });

  // 3. Demo Credential Quick-Fill Helpers (Convenient for examiners and testing)
  window.fillAdminCredentials = function () {
    const emailField = document.getElementById('login-email');
    const pwField = document.getElementById('login-password');
    if (emailField && pwField) {
      emailField.value = 'admin@ecommerce.com';
      pwField.value = 'admin123';
      showToast('Populated Administrator credentials');
    }
  };

  window.fillCustomerCredentials = function () {
    const emailField = document.getElementById('login-email');
    const pwField = document.getElementById('login-password');
    if (emailField && pwField) {
      emailField.value = 'john@example.com';
      pwField.value = 'password123';
      showToast('Populated Demo Customer credentials');
    }
  };

  // 4. Form Validation Helper
  const forms = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });

  // 5. Password Confirmation Validator on Register Form
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', function (e) {
      const pw = document.getElementById('register-password');
      const confirmPw = document.getElementById('register-confirm-password');
      if (pw && confirmPw && pw.value !== confirmPw.value) {
        e.preventDefault();
        alert('Passwords do not match. Please verify your password entry.');
        confirmPw.focus();
      }
    });
  }

  // 6. Delete Action Confirmation
  document.querySelectorAll('.btn-confirm-delete').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      const itemName = this.dataset.itemName || 'this item';
      if (!confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });

  // 7. Light Floating Toast Notification
  function showToast(message) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'position-fixed bottom-0 end-0 p-3';
      container.style.zIndex = '1100';
      document.body.appendChild(container);
    }

    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-white bg-dark border-0 show shadow-lg';
    toastEl.role = 'alert';
    toastEl.innerHTML = `
      <div class="d-flex">
        <div class="toast-body"><i class="bi bi-info-circle me-2 text-info"></i>${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    `;
    container.appendChild(toastEl);

    setTimeout(() => {
      toastEl.classList.remove('show');
      setTimeout(() => toastEl.remove(), 400);
    }, 3000);
  }
});
