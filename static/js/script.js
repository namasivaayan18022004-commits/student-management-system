document.addEventListener("DOMContentLoaded", function () {
    // Sidebar Toggle
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');

    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function () {
            sidebar.classList.toggle('active');
            if (window.innerWidth <= 768) {
                content.classList.toggle('active');
            }
        });
    }

    // Dark Mode Toggle
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme');
    const themeIcon = document.getElementById('themeIcon');

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark' && themeIcon) {
            themeIcon.classList.replace('bi-moon', 'bi-sun');
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            let theme = document.documentElement.getAttribute('data-theme');
            if (theme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                themeIcon.classList.replace('bi-sun', 'bi-moon');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeIcon.classList.replace('bi-moon', 'bi-sun');
            }
            
            // Re-render charts if they exist on the page to update font colors
            if (typeof renderCharts === "function") {
                renderCharts();
            }
        });
    }

    // Initialize Bootstrap Toasts
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, { delay: 3000 });
    });
    toastList.forEach(toast => toast.show());

    // Auto-hide flash messages after 5 seconds if not using toasts
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert:not(.toast)');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

function confirmDelete(event) {
    if(!confirm("Are you sure you want to delete this student?")) {
        event.preventDefault();
    }
}

// PDF Export logic using html2pdf
function exportPDF() {
    const element = document.getElementById('report-content');
    if (!element) {
        alert("No content to export.");
        return;
    }
    
    // Add temporary styling for PDF export
    const originalTheme = document.documentElement.getAttribute('data-theme');
    document.documentElement.setAttribute('data-theme', 'light'); // Force light mode for PDF
    
    const opt = {
        margin:       0.5,
        filename:     'students_report.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
    };

    html2pdf().set(opt).from(element).save().then(() => {
        // Restore theme
        document.documentElement.setAttribute('data-theme', originalTheme);
    });
}

function printReport() {
    const originalTheme = document.documentElement.getAttribute('data-theme');
    document.documentElement.setAttribute('data-theme', 'light');
    window.print();
    setTimeout(() => {
        document.documentElement.setAttribute('data-theme', originalTheme);
    }, 100);
}

// Appearance Customization Helper
function applyAppearanceSettings(themeMode, fontSize, sidebarColor, accentColor) {
    if (themeMode) {
        if (themeMode === 'system') {
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            themeMode = prefersDark ? 'dark' : 'light';
        }
        document.documentElement.setAttribute('data-theme', themeMode);
        localStorage.setItem('theme', themeMode);
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            themeIcon.classList.replace(themeMode === 'dark' ? 'bi-moon' : 'bi-sun', themeMode === 'dark' ? 'bi-sun' : 'bi-moon');
        }
    }
    if (fontSize) {
        document.documentElement.style.fontSize = fontSize === 'small' ? '14px' : (fontSize === 'large' ? '18px' : '16px');
        localStorage.setItem('fontSize', fontSize);
    }
    if (sidebarColor && document.getElementById('sidebar')) {
        document.getElementById('sidebar').style.backgroundColor = sidebarColor;
        localStorage.setItem('sidebarColor', sidebarColor);
    }
    if (accentColor) {
        document.documentElement.style.setProperty('--primary-color', accentColor);
        localStorage.setItem('accentColor', accentColor);
    }
}

// Apply stored font size and accent colors on load
document.addEventListener("DOMContentLoaded", function () {
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.documentElement.style.fontSize = savedFontSize === 'small' ? '14px' : (savedFontSize === 'large' ? '18px' : '16px');
    }
    const savedAccent = localStorage.getItem('accentColor');
    if (savedAccent) {
        document.documentElement.style.setProperty('--primary-color', savedAccent);
    }
    const savedSidebar = localStorage.getItem('sidebarColor');
    if (savedSidebar && document.getElementById('sidebar')) {
        document.getElementById('sidebar').style.backgroundColor = savedSidebar;
    }
});

