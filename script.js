const revealShell = document.querySelector("[data-reveal-shell]");
const revealZone = document.querySelector("[data-reveal-zone]");
const revealSections = document.querySelectorAll(".section-reveal");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const coarsePointer = window.matchMedia("(hover: none), (pointer: coarse)");
const projectsData = window.PORTFOLIO_PROJECTS || [];

const projectCarousel = document.querySelector("[data-project-carousel]");
const projectVisual = document.querySelector("[data-active-project-visual]");
const projectImage = document.querySelector("[data-active-project-image]");
const projectCounter = document.querySelector("[data-active-project-counter]");
const projectStatus = document.querySelector("[data-active-project-status]");
const projectTitle = document.querySelector("[data-active-project-title]");
const projectDescription = document.querySelector("[data-active-project-description]");
const projectRole = document.querySelector("[data-active-project-role]");
const projectFocus = document.querySelector("[data-active-project-focus]");
const projectTools = document.querySelector("[data-active-project-tools]");
const projectOutcome = document.querySelector("[data-active-project-outcome]");
const projectLink = document.querySelector("[data-active-project-link]");
const projectIndicators = document.querySelector("[data-project-indicators]");
const projectMobileList = document.querySelector("[data-project-mobile-list]");

let activeProjectIndex = 0;
let projectTransitionTimer = null;

function getProjectHref(project) {
  return `projects/${project.slug}.html`;
}

function shouldContainProjectImage(project) {
  return project.slug === "fnirs-classification" || project.slug === "redcap-feedback-workflow";
}

function renderActiveProject(index, immediate = false) {
  if (!projectsData.length || !projectCarousel) return;
  const project = projectsData[index];
  const displayTitle = project.shortTitle || project.title;
  const total = String(projectsData.length).padStart(2, "0");
  const nextCounter = `${String(index + 1).padStart(2, "0")} / ${total}`;

  window.clearTimeout(projectTransitionTimer);

  const applyProject = () => {
    projectCounter.textContent = nextCounter;
    projectStatus.textContent = project.status;
    projectStatus.classList.toggle("is-live", /in progress/i.test(project.status));
    projectTitle.textContent = displayTitle;
    projectDescription.textContent = project.description;
    projectRole.textContent = project.role;
    projectFocus.textContent = project.focus;
    projectTools.textContent = project.tools;
    projectOutcome.textContent = project.outcome;
    projectLink.href = getProjectHref(project);
    projectImage.src = project.image;
    projectImage.alt = project.imageAlt;
    projectVisual.classList.toggle("project-carousel-visual-contain", shouldContainProjectImage(project));

    projectIndicators
      ?.querySelectorAll("button")
      .forEach((button, buttonIndex) => {
        const isActive = buttonIndex === index;
        button.classList.toggle("is-active", isActive);
        button.setAttribute("aria-pressed", String(isActive));
      });

    projectCarousel.classList.remove("is-switching");
  };

  if (immediate) {
    applyProject();
    return;
  }

  projectCarousel.classList.add("is-switching");
  projectTransitionTimer = window.setTimeout(applyProject, 130);
}

function setActiveProject(index, immediate = false) {
  if (index === activeProjectIndex && !immediate) return;
  activeProjectIndex = index;
  renderActiveProject(index, immediate);
}

function selectProject(index) {
  setActiveProject(index);
}

function createProjectIndicator(project, index) {
  const button = document.createElement("button");
  button.type = "button";

  const num = document.createElement("span");
  num.className = "step-num";
  num.textContent = String(index + 1).padStart(2, "0");

  const label = document.createElement("span");
  label.className = "step-label";
  label.textContent = project.navLabel || project.shortTitle || project.title;

  button.append(num, label);
  button.setAttribute("aria-label", `Show ${project.title}`);
  button.addEventListener("click", () => selectProject(index));
  return button;
}

function renderMobileProjectCards() {
  if (!projectMobileList || !projectsData.length) return;
  projectMobileList.innerHTML = "";

  projectsData.forEach((project, index) => {
    const article = document.createElement("article");
    article.className = "project-mobile-card";

    const figure = document.createElement("figure");
    figure.className = shouldContainProjectImage(project)
      ? "project-mobile-visual project-mobile-visual-contain"
      : "project-mobile-visual";

    const image = document.createElement("img");
    image.src = project.image;
    image.alt = project.imageAlt;
    image.loading = "lazy";
    figure.append(image);

    const content = document.createElement("div");
    content.className = "project-mobile-content";

    const headline = document.createElement("div");
    headline.className = "project-headline";

    const counter = document.createElement("p");
    counter.className = "project-counter";
    counter.textContent = `${String(index + 1).padStart(2, "0")} / ${String(projectsData.length).padStart(2, "0")}`;

    const status = document.createElement("p");
    status.className = "project-status";
    status.textContent = project.status;
    status.classList.toggle("is-live", /in progress/i.test(project.status));

    headline.append(counter, status);

    const heading = document.createElement("h3");
    heading.textContent = project.shortTitle || project.title;

    const description = document.createElement("p");
    description.className = "project-description";
    description.textContent = project.description;

    const link = document.createElement("a");
    link.className = "project-explore-link";
    link.href = getProjectHref(project);
    link.textContent = "Explore Project";

    content.append(headline, heading, description, link);
    article.append(figure, content);
    projectMobileList.append(article);
  });
}

if (projectCarousel && projectsData.length) {
  projectCarousel.style.setProperty("--project-count", projectsData.length);
  projectsData.forEach((project, index) => {
    projectIndicators?.append(createProjectIndicator(project, index));
  });
  renderActiveProject(0, true);
  renderMobileProjectCards();
}

// Experience logos fall back to a monogram chip until the image files exist.
document.querySelectorAll(".experience-logo img").forEach((img) => {
  const markMissing = () => img.closest(".experience-logo")?.classList.add("logo-missing");
  if (img.complete && img.naturalWidth === 0) {
    markMissing();
  } else {
    img.addEventListener("error", markMissing);
  }
});

function setPressedState(isActive) {
  if (!revealZone) return;
  revealZone.setAttribute("aria-pressed", String(isActive));
}

function setRevealActive(isActive) {
  if (!revealShell) return;

  revealShell.classList.toggle("is-revealing", isActive);
  setPressedState(isActive || revealShell.classList.contains("is-touch-revealed"));

  if (!isActive && !revealShell.classList.contains("is-touch-revealed")) {
    revealShell.style.setProperty("--reveal-size", "0px");
  }
}

function updateRevealFromEvent(event, scale = 0.26) {
  if (!revealShell) return;

  const bounds = revealShell.getBoundingClientRect();
  const x = ((event.clientX - bounds.left) / bounds.width) * 100;
  const y = ((event.clientY - bounds.top) / bounds.height) * 100;
  const size = Math.max(bounds.width, bounds.height) * scale;

  revealShell.style.setProperty("--cursor-x", `${Math.max(0, Math.min(100, x))}%`);
  revealShell.style.setProperty("--cursor-y", `${Math.max(0, Math.min(100, y))}%`);
  revealShell.style.setProperty("--reveal-size", `${size}px`);
}

function toggleTouchReveal(event) {
  if (!revealShell) return;

  const nextState = !revealShell.classList.contains("is-touch-revealed");
  revealShell.classList.toggle("is-touch-revealed", nextState);

  if (nextState) {
    updateRevealFromEvent(event, 0.72);
  } else {
    revealShell.style.setProperty("--reveal-size", "0px");
  }

  setPressedState(nextState);
}

function revealVisibleSectionsNow() {
  revealSections.forEach((section) => {
    const rect = section.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.94 && rect.bottom > 0) {
      section.classList.add("is-visible");
    }
  });
}

if (revealShell && revealZone) {
  revealZone.addEventListener("pointerenter", (event) => {
    if (coarsePointer.matches || reduceMotion.matches) return;
    updateRevealFromEvent(event);
    setRevealActive(true);
  });

  revealZone.addEventListener("pointermove", (event) => {
    if (coarsePointer.matches || reduceMotion.matches) return;
    updateRevealFromEvent(event);
  });

  revealZone.addEventListener("pointerleave", () => {
    if (coarsePointer.matches || reduceMotion.matches) return;
    setRevealActive(false);
  });

  revealZone.addEventListener("pointerup", (event) => {
    if (!coarsePointer.matches || reduceMotion.matches) return;
    toggleTouchReveal(event);
  });

  revealZone.addEventListener("focus", () => {
    if (coarsePointer.matches || reduceMotion.matches) return;
    revealShell.style.setProperty("--cursor-x", "50%");
    revealShell.style.setProperty("--cursor-y", "44%");
    revealShell.style.setProperty("--reveal-size", "220px");
    setRevealActive(true);
  });

  revealZone.addEventListener("blur", () => {
    if (coarsePointer.matches || reduceMotion.matches) return;
    setRevealActive(false);
  });

  revealZone.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;

    event.preventDefault();
    const nextState = !revealShell.classList.contains("is-touch-revealed");
    revealShell.classList.toggle("is-touch-revealed", nextState);
    revealShell.style.setProperty("--cursor-x", "50%");
    revealShell.style.setProperty("--cursor-y", "46%");
    revealShell.style.setProperty("--reveal-size", nextState ? "72%" : "0px");
    setPressedState(nextState);
  });
}

if ("IntersectionObserver" in window && !reduceMotion.matches) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.04,
      rootMargin: "0px 0px -8% 0px",
    },
  );

  revealSections.forEach((section) => revealObserver.observe(section));
  revealVisibleSectionsNow();
  window.addEventListener("scroll", revealVisibleSectionsNow, { passive: true });
  window.addEventListener("resize", revealVisibleSectionsNow);
} else {
  revealSections.forEach((section) => section.classList.add("is-visible"));
}
