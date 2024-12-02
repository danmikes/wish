document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.querySelectorAll('.tab-link');
  const tabContents = document.querySelectorAll('.tab-content');

  function setActiveTab(tabId) {
    tabs.forEach(tab => tab.classList.remove('is-active'));
    tabContents.forEach(content => content.classList.remove('is-active'));

    const selectedTab = document.querySelector(`.tab-link[data-tab="${tabId}"]`);
    const selectedContent = document.getElementById(tabId);

    if (selectedTab && selectedContent) {
      selectedTab.classList.add('is-active');
      selectedContent.classList.add('is-active');
      localStorage.setItem('activeTab', tabId);
    } else {
      console.error(`Could not find tab with id: ${tabId}`);
    }
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', function(e) {
      e.preventDefault();
      const tabId = this.getAttribute('data-tab');
      setActiveTab(tabId);
    });
  });

  const savedTab = localStorage.getItem('activeTab');
  if (savedTab && document.getElementById(savedTab)) {
    setActiveTab(savedTab);
  } else {
    setActiveTab('current-user');
  }

  document.addEventListener('click', function(event) {
    if (!event.target.closest('.card-image')) {
    }
  });

  document.addEventListener('keydown', function(event) {
    if (event.key == 'Escape') {
    }
  });
});
