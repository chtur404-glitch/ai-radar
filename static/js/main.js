/* AI Radar — 少量互動：滾動進場、標頭收縮、手機導覽。
   沒有外部依賴；所有效果都在 prefers-reduced-motion 下自動關閉。 */

(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- 標頭：捲動後加上細邊框 ---- */
  var header = document.querySelector("[data-header]");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- 手機導覽 ---- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* ---- 滾動進場：同一容器內每張卡片錯開 60ms ---- */
  var items = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
  if (!items.length) return;

  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var siblings = Array.prototype.slice.call(
        el.parentElement ? el.parentElement.querySelectorAll("[data-reveal]") : []
      );
      var index = Math.max(0, siblings.indexOf(el));
      el.style.transitionDelay = Math.min(index * 60, 300) + "ms";
      el.classList.add("is-visible");
      observer.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

  items.forEach(function (el) { observer.observe(el); });

  /* ---- 圖片載入失敗時保留漸層底，不留破圖 ---- */
  document.querySelectorAll(".card-media img, .card-thumb img").forEach(function (img) {
    img.addEventListener("error", function () { img.style.opacity = "0"; });
  });
})();
