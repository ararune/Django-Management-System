function showContent(event, tabId) {
    event.preventDefault(); // Prevent the default behavior of link click

    var contentDivs = document.getElementsByClassName("tab-content");
    for (var i = 0; i < contentDivs.length; i++) {
      contentDivs[i].style.display = "none";
    }

    var selectedContent = document.getElementById(tabId);
    selectedContent.style.display = "block";
  }