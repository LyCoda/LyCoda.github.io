// Progressive enhancement: project content and links are present in the HTML.
const menu = document.querySelector(".menu-toggle");
const nav = document.querySelector(".site-nav");
if (menu && nav) {
  menu.hidden = false;
  const closeMenu = () => {
    menu.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
  };
  menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  });
  nav.addEventListener("click", (e) => {
    if (e.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("is-open")) {
      closeMenu();
      menu.focus();
    }
  });
}
const shell = document.querySelector("[data-reveal-shell]");
const reveal = document.querySelector("[data-reveal-zone]");
const reduced = matchMedia("(prefers-reduced-motion: reduce)");
const hover = matchMedia("(hover: hover) and (pointer: fine)");
if (shell && reveal) {
  reveal.hidden = false;
  let pinned = false;
  const video = shell.querySelector("video");
  const motion = document.querySelector(".motion-toggle");
  const setPinned = (value) => {
    pinned = value;
    shell.classList.toggle("is-pinned", value);
    reveal.setAttribute("aria-pressed", String(value));
    reveal.setAttribute(
      "aria-label",
      value ? "Show skeletal portrait" : "Show colour portrait",
    );
  };
  reveal.addEventListener("click", () => setPinned(!pinned));
  reveal.addEventListener("pointermove", (e) => {
    if (!hover.matches || reduced.matches || pinned) return;
    const box = shell.getBoundingClientRect();
    shell.style.setProperty("--cursor-x", `${e.clientX - box.left}px`);
    shell.style.setProperty("--cursor-y", `${e.clientY - box.top}px`);
    shell.classList.add("is-revealing");
  });
  reveal.addEventListener("pointerleave", () =>
    shell.classList.remove("is-revealing"),
  );
  reveal.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      setPinned(false);
      shell.classList.remove("is-revealing");
    }
  });
  let userPaused = false;
  let inView = true;
  // Start the portrait video only after the page has loaded, so it never delays first paint.
  let ready = false;
  const updateVideo = () => {
    const play = ready && !reduced.matches && !userPaused && inView && !document.hidden;
    motion.hidden = reduced.matches;
    motion.textContent = userPaused ? "Play animation" : "Pause animation";
    if (play)
      video.play().catch(() => {
        userPaused = true;
        motion.textContent = "Play animation";
      });
    else video.pause();
  };
  motion.addEventListener("click", () => {
    userPaused = !userPaused;
    updateVideo();
  });
  reduced.addEventListener("change", () => {
    shell.classList.remove("is-revealing");
    updateVideo();
  });
  document.addEventListener("visibilitychange", updateVideo);
  if ("IntersectionObserver" in window)
    new IntersectionObserver((entries) => {
      inView = entries[0].isIntersecting;
      updateVideo();
    }).observe(shell);
  updateVideo();
  const start = () => setTimeout(() => {
    ready = true;
    updateVideo();
  }, 1200);
  if (document.readyState === "complete") start();
  else addEventListener("load", start, { once: true });
}
const toc = document.querySelector(".article-nav");
if (toc && "IntersectionObserver" in window) {
  const links = [...toc.querySelectorAll("a")];
  const observer = new IntersectionObserver(
    (entries) => {
      const entry = entries.find((item) => item.isIntersecting);
      if (!entry) return;
      links.forEach((link) => {
        if (link.hash === "#" + entry.target.id)
          link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    },
    { rootMargin: "-15% 0px -65% 0px" },
  );
  document
    .querySelectorAll(".article-section")
    .forEach((section) => observer.observe(section));
}
// Scroll reveal for the work sections. Content stays visible without JavaScript.
const revealTargets = document.querySelectorAll(".reveal, .evolution, .trace-figure");
if (revealTargets.length && "IntersectionObserver" in window) {
  document.documentElement.classList.add("js");
  const revealer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        revealer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.08 },
  );
  revealTargets.forEach((el) => revealer.observe(el));
}

// Archive cards: a slight tilt and glare that follow the pointer.
const tiltOK =
  window.matchMedia("(hover: hover) and (pointer: fine)").matches &&
  !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
document.querySelectorAll(".vc").forEach((card) => {
  if (!tiltOK) return;
  card.addEventListener("pointermove", (e) => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    card.style.setProperty("--rx", ((x - 0.5) * 6).toFixed(2) + "deg");
    card.style.setProperty("--ry", ((0.5 - y) * 6).toFixed(2) + "deg");
    card.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
    card.style.setProperty("--my", (y * 100).toFixed(1) + "%");
  });
  card.addEventListener("pointerleave", () => {
    card.style.setProperty("--rx", "0deg");
    card.style.setProperty("--ry", "0deg");
  });
});

// Archive filter chips.
const vaultGrid = document.querySelector(".vault-grid");
document.querySelectorAll(".vault-filter button").forEach((btn, _, all) => {
  btn.addEventListener("click", () => {
    const f = btn.dataset.filter;
    all.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    vaultGrid.classList.toggle("is-filtered", f !== "all");
    vaultGrid.querySelectorAll(".vc").forEach((card) => {
      card.classList.toggle("is-hidden", f !== "all" && card.dataset.thread !== f);
    });
  });
});

// Guess-first project cards: pick an answer, see the result, then read how I found out.
const scoreEl = document.querySelector(".vault-score");
let guessed = 0;
let right = 0;
document.querySelectorAll(".vc").forEach((card) => {
  const opts = card.querySelectorAll(".vc-opt");
  const verdict = card.querySelector(".vc-verdict");
  opts.forEach((opt) => {
    opt.addEventListener("click", () => {
      if (card.classList.contains("is-answered")) return;
      const ok = opt.dataset.correct === "true";
      opts.forEach((o) => {
        o.disabled = true;
        if (o.dataset.correct === "true") o.classList.add("is-right");
      });
      if (!ok) opt.classList.add("is-wrong");
      opt.setAttribute("aria-pressed", "true");
      verdict.textContent = ok ? "Right." : "Not quite.";
      card.classList.add("is-answered");
      guessed += 1;
      if (ok) right += 1;
      if (scoreEl) {
        const [g, r] = scoreEl.querySelectorAll("b");
        g.textContent = guessed;
        r.textContent = right;
        scoreEl.hidden = false;
      }
      card.querySelector(".vc-btn").focus({ preventScroll: true });
    });
  });
});
