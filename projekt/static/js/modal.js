 // Open the modal
 function openModal(contentId) {
    var modal = document.getElementById("myModal");
    var modalContents = document.getElementsByClassName("modal-content");
    for (var i = 0; i < modalContents.length; i++) {
      modalContents[i].style.display = "none";
    }

    var modalContent = document.getElementById(contentId);
    modalContent.style.display = "block";
    modal.style.display = "block";
  }

  // Close the modal
  function closeModal() {
    var modal = document.getElementById("myModal");
    var modalContents = document.getElementsByClassName("modal-content");
    for (var i = 0; i < modalContents.length; i++) {
      modalContents[i].style.display = "none";
    }
    modal.style.display = "none";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.addEventListener("click", closeModal);
  });