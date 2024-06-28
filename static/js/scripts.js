function openTab(tabId, element) {
    // Get all elements with class="tab-content" and hide them
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
        tabContents[i].classList.remove('active');
    }

    // Get all elements with class="tab-button" and remove the class "active"
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabId).style.display = "block";
    document.getElementById(tabId).classList.add('active');
    element.classList.add('active');
}

// Initialize the first tab as active
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('offline-tab').style.display = "block";
});
