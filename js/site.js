(function () {
  // mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "閉じる" : "メニュー";
    });
  }

  // contact form: show the Google Form only when a URL is configured
  var cfg = window.CRAFTFLOW_CONFIG || {};
  var holder = document.getElementById("form-holder");
  if (holder) {
    var url = (cfg.formUrl || "").trim();
    if (/^https:\/\/docs\.google\.com\/forms\//.test(url)) {
      var params = new URLSearchParams(location.search);
      var iframe = document.createElement("iframe");
      iframe.className = "form-frame";
      iframe.src = url;
      iframe.title = "CRAFTFLOW お問い合わせフォーム";
      iframe.loading = "lazy";
      holder.innerHTML = "";
      holder.appendChild(iframe);
      var open = (cfg.formOpenUrl || "").trim();
      if (open) {
        var p = document.createElement("p");
        p.className = "note";
        p.innerHTML = 'フォームが表示されない場合は <a href="' + open + '" target="_blank" rel="noopener">こちらから新しいタブで開いてください</a>。';
        holder.appendChild(p);
      }
      if (params.get("product")) {
        var hint = document.getElementById("product-hint");
        if (hint) { hint.hidden = false; hint.querySelector("strong").textContent = params.get("product"); }
      }
    }
  }
})();
