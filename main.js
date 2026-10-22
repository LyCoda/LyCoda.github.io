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
const revealTargets = document.querySelectorAll(".reveal, .evolution");
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

// TL;DR: one reading preference shared by the archive and every case study.
const readKey = "readMode";
const savedMode = () => {
  try {
    return localStorage.getItem(readKey);
  } catch (e) {
    return null;
  }
};
const saveMode = (m) => {
  try {
    localStorage.setItem(readKey, m);
  } catch (e) {}
};
const tldrBtn = document.querySelector(".vault-tldr");
if (tldrBtn && vaultGrid) {
  const setArchive = (on) => {
    tldrBtn.setAttribute("aria-pressed", String(on));
    vaultGrid.classList.toggle("is-tldr", on);
    // In TL;DR the card button opens the case study's TL;DR too.
    vaultGrid.querySelectorAll(".vc-btn").forEach((a) => {
      a.href = a.getAttribute("href").split("#")[0] + (on ? "#tldr" : "");
    });
  };
  setArchive(savedMode() === "tldr");
  tldrBtn.addEventListener("click", () => {
    const on = tldrBtn.getAttribute("aria-pressed") !== "true";
    setArchive(on);
    saveMode(on ? "tldr" : "full");
  });
}
const modeBtns = document.querySelectorAll(".read-mode button");
if (modeBtns.length) {
  const setMode = (m) => {
    document.body.classList.toggle("is-tldr", m === "tldr");
    modeBtns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.mode === m)));
  };
  setMode(location.hash === "#tldr" || savedMode() === "tldr" ? "tldr" : "full");
  modeBtns.forEach((b) =>
    b.addEventListener("click", () => {
      setMode(b.dataset.mode);
      saveMode(b.dataset.mode);
    }),
  );
  // A part link in the TL;DR opens the full story at that section.
  document.querySelectorAll(".tldr-parts a").forEach((a) =>
    a.addEventListener("click", () => {
      setMode("full");
      saveMode("full");
    }),
  );
}

// 3D cards: move the pointer across a card to turn the object.
// Frames live in one sprite that only loads when a mouse user first hovers.
if (tiltOK) {
  document.querySelectorAll(".vc-spin").forEach((cv) => {
    const card = cv.closest(".vc");
    const still = card.querySelector(".vc-img");
    const n = Number(cv.dataset.frames);
    const mid = (n - 1) / 2;
    const pos = ((still && still.style.objectPosition) || "50% 50%").split(" ").map((v) => parseFloat(v) / 100);
    let img = null;
    let frame = mid;
    let target = mid;
    let raf = 0;
    const draw = () => {
      const r = cv.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = Math.round(r.width * dpr);
      const h = Math.round(r.height * dpr);
      if (cv.width !== w || cv.height !== h) {
        cv.width = w;
        cv.height = h;
      }
      const fw = img.naturalWidth / n;
      const fh = img.naturalHeight;
      const s = Math.max(w / fw, h / fh);
      const ctx = cv.getContext("2d");
      ctx.drawImage(img, Math.round(frame) * fw, 0, fw, fh, (w - fw * s) * pos[0], (h - fh * s) * pos[1], fw * s, fh * s);
    };
    const tick = () => {
      frame += (target - frame) * 0.16;
      if (Math.abs(target - frame) < 0.05) frame = target;
      draw();
      raf = frame === target ? 0 : requestAnimationFrame(tick);
    };
    const go = () => {
      if (img && img.complete && !raf) raf = requestAnimationFrame(tick);
    };
    card.addEventListener("pointerenter", () => {
      if (img) return;
      img = new Image();
      img.decoding = "async";
      img.onload = () => {
        draw();
        cv.classList.add("is-ready");
        go();
      };
      img.src = cv.dataset.src;
    });
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      target = Math.max(0, Math.min(n - 1, ((e.clientX - r.left) / r.width) * (n - 1)));
      go();
    });
    card.addEventListener("pointerleave", () => {
      target = mid;
      go();
    });
  });
}
