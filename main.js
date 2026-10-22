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

// Logic-gate sandbox on the heart monitor card: toggle A and B, cycle the gate, watch the output.
const GATES = { AND: (a, b) => a && b, OR: (a, b) => a || b, XOR: (a, b) => a !== b, NOR: (a, b) => !(a || b) };
const GATE_NAMES = Object.keys(GATES);
document.querySelectorAll(".vc-gates").forEach((box) => {
  const ins = [...box.querySelectorAll(".vc-in")];
  const gate = box.querySelector(".vc-gate");
  const lamp = box.querySelector(".vc-lamp");
  const update = () => {
    const [a, b] = ins.map((i) => i.getAttribute("aria-pressed") === "true");
    const on = GATES[gate.textContent](a, b);
    lamp.classList.toggle("is-on", on);
    lamp.querySelector("b").textContent = on ? "1" : "0";
  };
  ins.forEach((btn) => btn.addEventListener("click", () => {
    const on = btn.getAttribute("aria-pressed") !== "true";
    btn.setAttribute("aria-pressed", String(on));
    btn.querySelector("b").textContent = on ? "1" : "0";
    update();
  }));
  gate.addEventListener("click", () => {
    const next = GATE_NAMES[(GATE_NAMES.indexOf(gate.textContent) + 1) % GATE_NAMES.length];
    gate.textContent = next;
    gate.setAttribute("aria-label", `Gate: ${next}. Click to change.`);
    update();
  });
  update();
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

// 3D cards: hovering a card plays its turntable loop; otherwise the still image shows.
// Touch screens and reduced-motion settings keep the still and never download the clip.
const loops = document.querySelectorAll(".vc-loop");
const finePointer = matchMedia("(hover: hover) and (pointer: fine)");
if (loops.length && finePointer.matches && !reduced.matches) {
  // VP9 WebM where supported (smaller, plays in open-source Chromium), H.264 MP4 otherwise (Safari).
  const webm = document.createElement("video").canPlayType('video/webm; codecs="vp9"') !== "";
  const load = (v) => {
    if (v.src) return;
    v.preload = "auto";
    v.src = webm ? v.dataset.src.replace(/\.mp4$/, ".webm") : v.dataset.src;
  };
  // Fetch each clip as its card nears the screen, so the first hover starts at once.
  const io =
    "IntersectionObserver" in window
      ? new IntersectionObserver(
          (entries) =>
            entries.forEach(({ target, isIntersecting }) => {
              if (isIntersecting) {
                load(target);
                io.unobserve(target);
              }
            }),
          { rootMargin: "300px 0px" },
        )
      : null;
  loops.forEach((v) => {
    if (io) io.observe(v);
    const card = v.closest(".vc");
    card.addEventListener("pointerenter", () => {
      load(v);
      v.currentTime = 0;
      v.play().then(() => {
        if (card.matches(":hover")) v.classList.add("is-playing");
      }).catch(() => {});
    });
    card.addEventListener("pointerleave", () => v.classList.remove("is-playing"));
    // Pause once the fade back to the still has finished.
    v.addEventListener("transitionend", (e) => {
      if (e.propertyName === "opacity" && !v.classList.contains("is-playing")) v.pause();
    });
  });
}
