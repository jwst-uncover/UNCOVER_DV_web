/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2024 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 * Building off of Bootstrap script, and modified to work with DBC
 */

"use strict"

const getStoredTheme = () => localStorage.getItem('theme');
const setStoredTheme = theme => localStorage.setItem('theme', theme);


const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    // console.log("storedTheme", storedTheme)
    if (storedTheme) {
        return storedTheme;
    } else {
        return "auto";
    }
};

const setTheme = theme => {
    // console.log("running setTheme")
    if (theme === 'auto') {
    document.documentElement.setAttribute(
        'data-bs-theme',
        window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
    );
    } else {
    document.documentElement.setAttribute('data-bs-theme', theme);
    }
};


const showActiveTheme = (theme, focus = false) => {
    // console.log("running showActiveTheme")
    const themeSwitcher = document.querySelector(
    `div#bd-theme button[class*="dropdown-toggle"]`
);
    // console.log("themeSwitcher", themeSwitcher)
    if (!themeSwitcher) {
    return;
    }

    const themeSwitcherText = document.getElementById('bd-theme-text');
    const activeThemeIcon = document.getElementById('theme-icon-active');

    // 
    const btnToActive = document.querySelector(
    `div#bd-theme #select-${theme}`
    );
    const classOfActiveBtn = btnToActive
    .querySelector('i')
    .getAttribute('class');

    document.querySelectorAll(
    `#bd-theme .dropdown-item`
).forEach(element => {
    element.classList.remove('active');
    element.setAttribute('aria-pressed', 'false'); 
    });

    btnToActive.classList.add('active');
    btnToActive.setAttribute('aria-pressed', 'true');
    activeThemeIcon.setAttribute('class', classOfActiveBtn);
    const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`;
    themeSwitcher.setAttribute('aria-label', themeSwitcherLabel);

    if (focus) {
    themeSwitcher.focus();
    }
};


setTheme(getPreferredTheme());

// showActiveTheme(getPreferredTheme());



// window.addEventListener('DOMContentLoaded', () => {
//     console.log("in DOMContentLoaded listener ")
//     showActiveTheme(getPreferredTheme());
// }); 

  
window
    .matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', () => {
    const storedTheme = getStoredTheme();
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
        setTheme(getPreferredTheme());
    }
});


window.toggle_theme = function(theme) {
    setStoredTheme(theme);
    setTheme(theme);
    showActiveTheme(theme, true);
}; 


window.show_active_theme = function() {
    // console.log("in window.show_active_theme ")
    showActiveTheme(getPreferredTheme());
};