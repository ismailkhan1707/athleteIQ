/* ============================================================
   AthleteIQ — Application JavaScript
   Modern ES6+ with null-safe access and graceful degradation.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ──────────────────────────────────────────────────────────
     1. SIDEBAR TOGGLE  (mobile / tablet)
     ────────────────────────────────────────────────────────── */
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
      document.body.classList.toggle('sidebar-open');
    });

    // Close sidebar when clicking the overlay (the ::after pseudo-element)
    document.addEventListener('click', (e) => {
      if (
        document.body.classList.contains('sidebar-open') &&
        !e.target.closest('.sidebar') &&
        !e.target.closest('.sidebar-toggle')
      ) {
        document.body.classList.remove('sidebar-open');
      }
    });
  }

  /* ──────────────────────────────────────────────────────────
     2. DELETE CONFIRMATIONS  (custom modal)
     ────────────────────────────────────────────────────────── */
  const confirmForms = document.querySelectorAll('form[data-confirm]');
  let activeConfirmForm = null;

  // Build modal once if any confirm forms exist
  if (confirmForms.length > 0) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'confirmModal';
    overlay.innerHTML = `
      <div class="modal">
        <h3 class="modal-title">Confirm Action</h3>
        <p class="modal-body" id="confirmModalMessage">Are you sure?</p>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" id="confirmCancel">Cancel</button>
          <button type="button" class="btn btn-danger" id="confirmOk">Delete</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    const modalMessage = document.getElementById('confirmModalMessage');
    const confirmCancel = document.getElementById('confirmCancel');
    const confirmOk = document.getElementById('confirmOk');

    const openModal = (message) => {
      modalMessage.textContent = message;
      overlay.classList.add('is-visible');
    };

    const closeModal = () => {
      overlay.classList.remove('is-visible');
      activeConfirmForm = null;
    };

    confirmCancel.addEventListener('click', closeModal);

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && overlay.classList.contains('is-visible')) {
        closeModal();
      }
    });

    confirmOk.addEventListener('click', () => {
      if (activeConfirmForm) {
        activeConfirmForm.submit();
      }
      closeModal();
    });

    confirmForms.forEach((form) => {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        activeConfirmForm = form;
        const message = form.dataset.confirm || 'Are you sure you want to proceed?';
        openModal(message);
      });
    });
  }

  /* ──────────────────────────────────────────────────────────
     3. TABLE SEARCH
     ────────────────────────────────────────────────────────── */
  const tableSearchInputs = document.querySelectorAll('.table-search');

  tableSearchInputs.forEach((input) => {
    // The search input may be in a .filter-bar sibling to the .card containing the table
    let table = null;
    const card = input.closest('.card');
    if (card) {
      table = card.querySelector('.data-table');
    }
    if (!table) {
      // Search in parent scope — walk up to the main content wrapper and find the table
      const wrapper = input.closest('.main-content') || input.closest('main') || document.body;
      table = wrapper.querySelector('.data-table');
    }
    if (!table) return;

    input.addEventListener('input', () => {
      const query = input.value.toLowerCase().trim();
      const rows = table.querySelectorAll('tbody tr');

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });
  });

  /* ──────────────────────────────────────────────────────────
     4. TOAST AUTO-DISMISS
     ────────────────────────────────────────────────────────── */
  const toasts = document.querySelectorAll('.toast');

  toasts.forEach((toast) => {
    // Close button
    const closeBtn = toast.querySelector('.toast-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => dismissToast(toast));
    }

    // Auto-dismiss after 5 seconds
    setTimeout(() => dismissToast(toast), 5000);
  });

  function dismissToast(toast) {
    if (!toast || toast.classList.contains('slide-out')) return;
    toast.classList.add('slide-out');
    toast.addEventListener('animationend', () => {
      toast.remove();
    }, { once: true });
  }

  /* ──────────────────────────────────────────────────────────
     5. ANIMATED COUNTERS
     ────────────────────────────────────────────────────────── */
  const counters = document.querySelectorAll('.counter');

  counters.forEach((counter) => {
    const target = parseInt(counter.dataset.target, 10);
    if (isNaN(target)) return;

    const duration = 1500; // ms
    let startTime = null;

    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Ease-out curve
      const eased = 1 - Math.pow(1 - progress, 3);
      counter.textContent = Math.floor(eased * target);

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        counter.textContent = target;
      }
    };

    // Observe element to start counting when visible
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            requestAnimationFrame(animate);
            observer.unobserve(counter);
          }
        });
      },
      { threshold: 0.3 }
    );

    observer.observe(counter);
  });

  /* ──────────────────────────────────────────────────────────
     6. CHART.JS INITIALIZATION
     ────────────────────────────────────────────────────────── */
  const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#f1f5f9',
          font: { family: "'Inter', sans-serif", size: 12 },
          padding: 16,
          usePointStyle: true,
          pointStyleWidth: 10,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#f1f5f9',
        bodyColor: '#94a3b8',
        borderColor: 'rgba(255,255,255,0.08)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        titleFont: { family: "'Inter', sans-serif", weight: '600' },
        bodyFont: { family: "'Inter', sans-serif" },
      },
    },
    scales: {}, // overridden per chart
  };

  function parseDataAttr(canvas, attr) {
    try {
      const raw = canvas.getAttribute(attr);
      return raw ? JSON.parse(raw) : [];
    } catch {
      console.warn(`AthleteIQ: Could not parse ${attr} on #${canvas.id}`);
      return [];
    }
  }

  // ─── Nationality Chart (Horizontal Bar) ──────────────────
  const nationalityCanvas = document.getElementById('nationalityChart');
  if (nationalityCanvas && typeof Chart !== 'undefined') {
    const labels = parseDataAttr(nationalityCanvas, 'data-labels');
    const values = parseDataAttr(nationalityCanvas, 'data-values');

    new Chart(nationalityCanvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Athletes',
            data: values,
            backgroundColor: 'rgba(6, 182, 212, 0.7)',
            borderColor: '#06b6d4',
            borderWidth: 1,
            borderRadius: 6,
            barThickness: 18,
          },
        ],
      },
      options: {
        ...chartDefaults,
        indexAxis: 'y',
        scales: {
          x: {
            grid: { color: 'rgba(148,163,184,0.1)', drawBorder: false },
            ticks: { color: '#94a3b8', font: { family: "'Inter', sans-serif" } },
          },
          y: {
            grid: { display: false },
            ticks: { color: '#94a3b8', font: { family: "'Inter', sans-serif" } },
          },
        },
      },
    });
  }

  // ─── Severity Chart (Doughnut) ────────────────────────────
  const severityCanvas = document.getElementById('severityChart');
  if (severityCanvas && typeof Chart !== 'undefined') {
    const labels = parseDataAttr(severityCanvas, 'data-labels');
    const values = parseDataAttr(severityCanvas, 'data-values');

    new Chart(severityCanvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [
          {
            data: values,
            backgroundColor: ['#f43f5e', '#f59e0b', '#06b6d4'],
            borderColor: 'transparent',
            borderWidth: 2,
            hoverOffset: 6,
          },
        ],
      },
      options: {
        ...chartDefaults,
        cutout: '65%',
        plugins: {
          ...chartDefaults.plugins,
          legend: {
            ...chartDefaults.plugins.legend,
            position: 'bottom',
          },
        },
      },
    });
  }

  // ─── Sport Chart (Polar Area) ─────────────────────────────
  const sportCanvas = document.getElementById('sportChart');
  if (sportCanvas && typeof Chart !== 'undefined') {
    const labels = parseDataAttr(sportCanvas, 'data-labels');
    const values = parseDataAttr(sportCanvas, 'data-values');

    const accentColors = [
      'rgba(6, 182, 212, 0.7)',
      'rgba(139, 92, 246, 0.7)',
      'rgba(16, 185, 129, 0.7)',
      'rgba(245, 158, 11, 0.7)',
      'rgba(244, 63, 94, 0.7)',
      'rgba(99, 102, 241, 0.7)',
      'rgba(236, 72, 153, 0.7)',
      'rgba(34, 211, 238, 0.7)',
    ];

    new Chart(sportCanvas, {
      type: 'polarArea',
      data: {
        labels,
        datasets: [
          {
            data: values,
            backgroundColor: accentColors.slice(0, labels.length),
            borderColor: 'transparent',
            borderWidth: 1,
          },
        ],
      },
      options: {
        ...chartDefaults,
        scales: {
          r: {
            grid: { color: 'rgba(148,163,184,0.1)' },
            ticks: { display: false },
          },
        },
        plugins: {
          ...chartDefaults.plugins,
          legend: {
            ...chartDefaults.plugins.legend,
            position: 'right',
          },
        },
      },
    });
  }

  /* ──────────────────────────────────────────────────────────
     7. PROFILE TABS
     ────────────────────────────────────────────────────────── */
  const profileTabs = document.querySelectorAll('.profile-tab');

  if (profileTabs.length > 0) {
    profileTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const targetId = tab.dataset.tab;
        if (!targetId) return;

        // Deactivate all tabs
        profileTabs.forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');

        // Show target content, hide others
        const allContents = document.querySelectorAll('.tab-content');
        allContents.forEach((content) => {
          content.classList.toggle('active', content.id === targetId);
        });
      });
    });
  }

  /* ──────────────────────────────────────────────────────────
     8. FORM VALIDATION
     ────────────────────────────────────────────────────────── */
  const validatedForms = document.querySelectorAll('form[data-validate]');

  validatedForms.forEach((form) => {
    form.addEventListener('submit', (e) => {
      let isValid = true;

      // Clear previous errors
      form.querySelectorAll('.is-invalid').forEach((el) => {
        el.classList.remove('is-invalid');
      });
      form.querySelectorAll('.form-error').forEach((el) => el.remove());

      // Check required fields
      const requiredFields = form.querySelectorAll('[required]');
      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add('is-invalid');

          const errorMsg = document.createElement('span');
          errorMsg.className = 'form-error';
          errorMsg.textContent = 'This field is required';
          field.parentElement.appendChild(errorMsg);
        }
      });

      // Check email fields
      const emailFields = form.querySelectorAll('input[type="email"]');
      emailFields.forEach((field) => {
        if (field.value.trim() && !isValidEmail(field.value)) {
          isValid = false;
          field.classList.add('is-invalid');

          const errorMsg = document.createElement('span');
          errorMsg.className = 'form-error';
          errorMsg.textContent = 'Please enter a valid email address';
          field.parentElement.appendChild(errorMsg);
        }
      });

      if (!isValid) {
        e.preventDefault();
        // Scroll to first error
        const firstError = form.querySelector('.is-invalid');
        if (firstError) {
          firstError.focus();
          firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    });

    // Clear error on input
    form.addEventListener('input', (e) => {
      if (e.target.classList.contains('is-invalid')) {
        e.target.classList.remove('is-invalid');
        const errorEl = e.target.parentElement.querySelector('.form-error');
        if (errorEl) errorEl.remove();
      }
    });
  });

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  /* ──────────────────────────────────────────────────────────
     9. FADE-IN ON SCROLL  (IntersectionObserver)
     ────────────────────────────────────────────────────────── */
  const fadeElements = document.querySelectorAll('.fade-in-up');

  if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
    const fadeObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            fadeObserver.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    fadeElements.forEach((el) => fadeObserver.observe(el));
  }

  /* ──────────────────────────────────────────────────────────
     10. MISC UTILITIES
     ────────────────────────────────────────────────────────── */

  // Escape key closes any open modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.is-visible').forEach((overlay) => {
        overlay.classList.remove('is-visible');
      });
    }
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

}); /* end DOMContentLoaded */
