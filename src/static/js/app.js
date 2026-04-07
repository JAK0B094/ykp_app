// PWA Service Worker kaydı
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/js/sw.js')
      .catch(() => {});
  });
}
