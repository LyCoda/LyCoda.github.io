(function () {
  const projects = window.PORTFOLIO_PROJECTS || [];
  const slug = document.body.dataset.projectSlug;
  const project = projects.find((item) => item.slug === slug);

  const resolveAsset = (assetPath) => `../${assetPath}`;
  const getProjectUrl = (item) => `${item.slug}.html`;
  const shouldContainImage = (item) =>
    item.slug === "fnirs-classification" || item.slug === "redcap-feedback-workflow";

  if (!project) {
    const title = document.querySelector("[data-project-title]");
    if (title) title.textContent = "Project not found";
    return;
  }

  const currentIndex = projects.findIndex((item) => item.slug === slug);
  const nextProject = projects[(currentIndex + 1) % projects.length];
  const counter = `${String(currentIndex + 1).padStart(2, "0")} / ${String(projects.length).padStart(2, "0")}`;

  document.title = `${project.title} | Nate Chu's Portfolio`;

  const setText = (selector, value) => {
    const element = document.querySelector(selector);
    if (element) element.textContent = value;
  };

  setText("[data-project-counter]", counter);
  setText("[data-project-title]", project.title);
  setText("[data-project-status]", project.status);
  document
    .querySelector("[data-project-status]")
    ?.classList.toggle("is-live", /in progress/i.test(project.status));
  setText("[data-project-intro]", project.intro);
  setText("[data-project-description]", project.description);
  setText("[data-project-role]", project.role);
  setText("[data-project-focus]", project.focus);
  setText("[data-project-tools]", project.tools);
  setText("[data-project-outcome]", project.outcome);

  const heroImage = document.querySelector("[data-project-image]");
  if (heroImage) {
    heroImage.src = resolveAsset(project.image);
    heroImage.alt = project.imageAlt;
    heroImage
      .closest(".case-hero-visual")
      ?.classList.toggle("case-hero-visual-contain", shouldContainImage(project));
  }

  const createElement = (tag, className, text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text) element.textContent = text;
    return element;
  };

  const createBlock = (eyebrow, title, className = "") => {
    const section = createElement("section", `case-block section-reveal ${className}`.trim());
    const header = createElement("div", "case-block-header");
    header.append(createElement("p", "case-block-kicker", eyebrow), createElement("h2", "", title));
    section.append(header);
    return section;
  };

  const createCards = (items, className = "case-card-grid") => {
    const grid = createElement("div", className);
    items.forEach((item) => {
      const card = createElement("article", "case-info-card");
      card.append(createElement("h3", "", item.label), createElement("p", "", item.value));
      grid.append(card);
    });
    return grid;
  };

  const createWorkflow = (steps) => {
    const list = createElement("ol", "case-workflow");
    list.style.setProperty("--workflow-count", steps.length);
    steps.forEach((step) => {
      const item = createElement("li", "");
      item.append(createElement("span", "", step));
      list.append(item);
    });
    return list;
  };

  const createTable = (items) => {
    const table = createElement("div", "case-compact-table");
    items.forEach((item) => {
      const row = createElement("div", "case-table-row");
      row.append(createElement("strong", "", item.label), createElement("p", "", item.value));
      table.append(row);
    });
    return table;
  };

  const createBulletList = (items) => {
    const list = createElement("ul", "case-bullet-list");
    items.forEach((item) => {
      list.append(createElement("li", "", item));
    });
    return list;
  };

  const sectionsContainer = document.querySelector("[data-project-sections]");
  const caseStudy = project.caseStudy;
  if (sectionsContainer && caseStudy) {
    sectionsContainer.innerHTML = "";

    const snapshot = createBlock("Project Snapshot", "The case in five moves", "case-snapshot");
    snapshot.append(createCards(caseStudy.snapshot));
    sectionsContainer.append(snapshot);

    const context = createBlock("Context / Problem", "Why this project mattered", "case-context");
    const contextCopy = createElement("div", "case-copy");
    caseStudy.context.forEach((paragraph) => contextCopy.append(createElement("p", "", paragraph)));
    context.append(contextCopy);
    sectionsContainer.append(context);

    const contribution = createBlock("What I Worked On", "Personal contribution", "case-contribution");
    contribution.append(createCards(caseStudy.built, "case-card-grid case-card-grid-compact"));
    sectionsContainer.append(contribution);

    const workflow = createBlock("Process / Workflow", caseStudy.workflowTitle, "case-process");
    workflow.append(createWorkflow(caseStudy.workflow));
    sectionsContainer.append(workflow);

    if (caseStudy.table?.length) {
      const tableBlock = createBlock("Technical Structure", caseStudy.tableTitle, "case-table-block");
      tableBlock.append(createTable(caseStudy.table));
      sectionsContainer.append(tableBlock);
    }

    const decisions = createBlock("Key Decisions", "Choices that shaped the work", "case-decisions");
    decisions.append(createCards(caseStudy.decisions, "case-card-grid case-card-grid-compact"));
    sectionsContainer.append(decisions);

    const outcomes = createBlock("Outcomes", "What the project produced", "case-outcomes");
    outcomes.append(createCards(caseStudy.outcomes, "case-card-grid case-outcome-grid"));
    sectionsContainer.append(outcomes);

    const reflection = createBlock("Reflection / Next Steps", "What this project demonstrates", "case-reflection");
    const reflectionLayout = createElement("div", "case-reflection-grid");
    const demonstrates = createElement("div", "case-demonstrates");
    caseStudy.demonstrates.forEach((item) => demonstrates.append(createElement("span", "", item)));
    const reflections = createElement("div", "case-reflection-notes");
    reflections.append(createBulletList(caseStudy.reflection));
    reflectionLayout.append(demonstrates, reflections);
    reflection.append(reflectionLayout);
    sectionsContainer.append(reflection);
  }

  const nextLink = document.querySelector("[data-next-project]");
  if (nextLink && nextProject) {
    nextLink.href = getProjectUrl(nextProject);
    nextLink.querySelector("span").textContent = "Next Project";
    nextLink.querySelector("strong").textContent = nextProject.title;
  }

  const revealSections = document.querySelectorAll(".section-reveal");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const revealVisibleSectionsNow = () => {
    revealSections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.94 && rect.bottom > 0) {
        section.classList.add("is-visible");
      }
    });
  };

  if ("IntersectionObserver" in window && !reduceMotion.matches) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.08,
        rootMargin: "0px 0px -8% 0px",
      },
    );

    revealSections.forEach((section) => observer.observe(section));
    revealVisibleSectionsNow();
    window.addEventListener("scroll", revealVisibleSectionsNow, { passive: true });
    window.addEventListener("resize", revealVisibleSectionsNow);
  } else {
    revealSections.forEach((section) => section.classList.add("is-visible"));
  }
})();
