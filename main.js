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
  const updateVideo = () => {
    const play = !reduced.matches && !userPaused && inView && !document.hidden;
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
