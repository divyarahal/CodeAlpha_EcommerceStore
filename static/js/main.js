// Auto-dismiss flash messages after a few seconds.
document.querySelectorAll('.messages .msg').forEach(function (el) {
  setTimeout(function () { el.style.display = 'none'; }, 5000);
});
